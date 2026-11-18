"""#964 Jobs A and B: the four fixed-(A, w) solves of proof/B_tail_M7.md 3.1 at one matching radius, with its stop
conditions, then m7_outer.py --local.

    python3 run_job.py XI1 TAG [--cap_h 6] [--dry]       e.g.  python3 run_job.py 0.14 xi014
    python3 run_job.py --selftest [--mutate=r3|endstate]

Run from solver/inner_stokes/ of the code worktree; logs go to logs/hier_nb_M7_rpi5_<TAG>_<name>.log. Stop rules (the issue):
a solve with |r_3| > 1e-6 is repeated once from its own end state (the 9-decimal x of its last `level 3 it` line); if the repeat
stays above, both logs get `_r3high`; a Traceback before the FIXED-A line stops the job (the BytesIO one at exit is harmless);
6 h cap per job (the running solve is killed with its workers).
"""
import os, re, signal, subprocess, sys, time, json

Z_A, Z_W = 2.719219, 1.000022
Z_X = "0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168"
S = ["--pretune", "--fixA", "--schur", "--predict", "--floor", "--procs", "2", "--h3=1e-4"]
PY = os.environ.get("RUN_PY", "/home/nathan/Source/venv-choptuik/bin/python")
BAR = 1e-6
SOLVES = [  # name, A, w, seeded with Z's harmonics
    ("zero", Z_A, Z_W, True),
    ("dA", round(Z_A + 2e-4, 9), Z_W, True),
    ("dw", Z_A, round(Z_W + 1e-4, 9), True),
    ("zero_repeat", Z_A, Z_W, False),
]


def parse(txt):
    """(r1 complex, r3 float, end-state harmonics string) from a log; None if no FIXED-A line"""
    m = re.findall(r"FIXED-A M (\d+): A ([0-9.]+)\s+w/w_inf ([0-9.]+).*?r_1 ([+-][0-9.]+e[+-]\d+)([+-][0-9.]+e[+-]\d+)i", txt)
    if not m:
        return None
    r3 = re.findall(r"F_3/F_1 = .*? r_3 ([0-9.]+e[+-]\d+)", txt)
    xs = re.findall(r"^level 3 it \d+: .*? x \[([^\]]*)\]", txt, re.M)
    end = ",".join(t.strip() for t in xs[-1].split(",")[2:]) if xs else None
    M, A, w, a, b = m[-1]
    return complex(float(a), float(b)), (float(r3[-1]) if r3 else float("nan")), end


def crashed(txt):
    """a Traceback before the FIXED-A line (the BytesIO one at interpreter exit comes after it)"""
    i = txt.find("FIXED-A M")
    head = txt if i < 0 else txt[:i]
    return "Traceback" in head


def run(cmd, log, deadline, log_driver):
    log_driver(f"run: {' '.join(cmd)} > {log}")
    with open(log, "w") as f:
        p = subprocess.Popen(["nice", "-n", "10"] + cmd, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            p.wait(timeout=max(1.0, deadline - time.time()))
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()
            log_driver("cap reached: killed the solve's process group")
            return None
    return p.returncode


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        return selftest(a)
    xi1, tag = a[0], a[1]
    cap_h = float(a[a.index("--cap_h") + 1]) if "--cap_h" in a else 6.0
    dry = "--dry" in a
    t0 = time.time()
    deadline = t0 + cap_h * 3600
    drv = open(f"logs/run964_{tag}.driver.log", "a")
    drv.write(f"INNER_NB_RTOL={os.environ.get('INNER_NB_RTOL')} cap {cap_h:g} h (I965's copy of I964's run_job.py; this line is its only change)\n")

    def log_driver(s):
        line = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " " + s
        print(line, flush=True); drv.write(line + "\n"); drv.flush()

    def cmd_for(A, w, x):
        c = [PY, "-u", "hier_nb.py", "7", f"{A:.9g}", f"{w:.9g}"]
        if x:
            c.append(f"--x={x}")
        return c + [f"--xi1={xi1}"] + S

    best = {}      # name -> the attempt's log used for m7_outer
    attempts = {}  # name -> [logs]
    for name, A, w, seeded in SOLVES:
        base = f"logs/hier_nb_M7_rpi5_{tag}_{name}"
        x = Z_X if seeded else None
        tries = []
        for k in range(2):
            log = base + (".log" if k == 0 else "_endstate.log")
            if dry:
                log_driver("dry: " + " ".join(cmd_for(A, w, x)) + f" > {log}")
                break
            rc = run(cmd_for(A, w, x), log, deadline, log_driver)
            txt = open(log).read()
            if rc is None:
                log_driver(f"{name}: stopped by the {cap_h:g} h cap"); tries.append(log); break
            res = parse(txt)
            if crashed(txt) or res is None:
                log_driver(f"{name}: Traceback or no FIXED-A line (exit {rc}): the job stops"); tries.append(log)
                best[name] = log; attempts[name] = tries
                return finish(tag, xi1, attempts, best, log_driver, stopped=True)
            r1, r3, end = res
            tries.append(log)
            log_driver(f"{name} try {k}: r_1 {r1.real:+.4f}{r1.imag:+.4f}i  |r_3| {r3:.2e}  [{time.time()-t0:.0f} s since start]")
            if r3 <= BAR or k == 1 or end is None:
                break
            x = end  # repeat once from the solve's own end state
            log_driver(f"{name}: |r_3| above {BAR:g}, repeat from its end state x {end}")
        if dry:
            continue
        # |r_3| of each attempt
        good = [l for l in tries if (parse(open(l).read()) or (0, 9, 0))[1] < BAR]
        if not good and tries:
            for l in tries:
                new = l[:-4] + "_r3high.log"
                os.rename(l, new)
                tries[tries.index(l)] = new
            log_driver(f"{name}: stays above {BAR:g}, logs renamed _r3high")
        best[name] = good[-1] if good else tries[-1]
        attempts[name] = tries
        if time.time() > deadline:
            log_driver("cap reached: the job stops"); break
    if not dry:
        finish(tag, xi1, attempts, best, log_driver, stopped=False)


def finish(tag, xi1, attempts, best, log_driver, stopped):
    if stopped:
        log_driver("job stopped before m7_outer; see the driver log")
        return 1
    if "dA" not in best or "dw" not in best:
        log_driver("the cap stopped the job before dA and dw were solved; no m7_outer call")
        return 1
    cen = [l for n in ("zero", "zero_repeat") for l in attempts.get(n, [])]
    cmd = [PY, "m7_outer.py", "--local"] + cen + ["--", best["dA"], best["dw"]]
    log_driver("run: " + " ".join(cmd))
    out = subprocess.run(cmd, capture_output=True, text=True)
    txt = out.stdout + out.stderr + f"(exit {out.returncode})\n"
    open(f"logs/m7_outer_rpi5_{tag}.txt", "w").write(f"# xi1 {xi1}\n$ {' '.join(cmd)}\n" + txt)
    log_driver("m7_outer.py --local exit " + str(out.returncode) + "; output in logs/m7_outer_rpi5_" + tag + ".txt")
    print(txt)
    return 0


def selftest(a):
    """the parser and the stop rules on stored logs; --mutate=r3 breaks the r_3 reading, --mutate=endstate drops the harmonics"""
    mut = [t for t in a if t.startswith("--mutate=")]
    mut = mut[0].split("=")[1] if mut else ""
    d = "logs/"
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(("ok   " if cond else "FAIL ") + label); ok = ok and cond
    t = open(d + "hier_nb_M7_fixA_xi015_fit3_repeat.log").read()
    r1, r3, end = parse(t)
    if mut == "r3":
        r3 = 1.0 / r3
    chk("fit3_repeat: r_3 1.2e-7, below the bar", abs(r3 - 1.2e-7) < 1e-9 and r3 < BAR)
    chk("fit3_repeat: r_1 -0.0225+0.0424i", abs(r1 - complex(-2.2497e-2, 4.2358e-2)) < 1e-9)
    if mut == "endstate":
        end = ",".join(end.split(",")[:3])
    chk("fit3_repeat: end state is the six 9-decimal harmonics", end is not None and len(end.split(",")) == 6 and end.split(",")[0] == "0.148977988")
    t2 = open(d + "hier_nb_M7_fixA_xi015_newton2_repeat_b.log").read()
    r1b, r3b, endb = parse(t2)
    if mut == "r3":
        r3b = 1e-9
    chk("newton2_repeat_b: r_3 1.5e-5, above the bar (repeat rule fires)", r3b > BAR)
    chk("a log cut before FIXED-A is read as no result", parse("level 3 it 0: |r_3| 1e-3  x [1, 2, 3]\n") is None)
    chk("Traceback before FIXED-A is a crash, the exit BytesIO one is not",
        crashed("Traceback (most recent call last):\nValueError\n") and not crashed(t))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
