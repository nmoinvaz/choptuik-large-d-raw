"""#981: #976's run_job976.py (#975's run_job.py with perturbed repeats; the Windows copy of #965's, itself #964's) with the
level-3 finite-difference step as an option: RUN_H3 (default 1e-4, the S of #964) is passed as --h3=RUN_H3. The four fixed-(A, w)
solves of proof/B_tail_M7.md 3.1 at one matching radius, then m7_outer.py --local.

    python run_job981.py XI1 TAG [--cap_h 3] [--dry]       e.g.  RUN_H3=1e-5 python run_job981.py 0.14 rtol14_h3e5_xi014
    python run_job981.py --selftest [--mutate=r3|endstate|pert]

Windows changes against #965's copy: no `nice` (BelowNormal priority class instead), the solve's process tree is killed with
`taskkill /T /F` at the cap, the interpreter is venv-i962's (RUN_PY), the solves run in RUN_SRC (solver/inner_stokes of the code
worktree) and their logs go to this folder's logs/ (RUN_LOGS) as hier_nb_M7_win2_<TAG>_<name>.log.

Change against #975's copy: a solve with |r_3| not under 1e-6 is NOT repeated from its own end state (a fixed point, #974 run 3)
but from that end state (the first attempt's, the 9-decimal x of its last `level 3 it` line) with every harmonic times 1 + REL*u,
u uniform in (-1, 1) from random.Random(RNGSEED) (REL 1e-7, RNGSEED 976, one generator per job drawn in solve order), up to
MAXREP repeats (3) per solve, stopping at the first one under the bar. Logs: <name>.log, <name>_pert1.log, ...; when none passes
all of the role's logs get `_r3high`. RUN_REL, RUN_RNGSEED, RUN_MAXREP override the defaults. A Traceback before the FIXED-A line
stops the job (the BytesIO one at exit is harmless); 3 h cap per job (the running solve is killed with its workers).
"""
import os, random, re, subprocess, sys, time, json

Z_A, Z_W = 2.719219, 1.000022
Z_X = "0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168"
H3 = os.environ.get("RUN_H3", "1e-4")
S = ["--pretune", "--fixA", "--schur", "--predict", "--floor", "--procs", "2", f"--h3={H3}"]
PY = os.environ.get("RUN_PY", "C:/Users/nathan/Source/venv-i962/Scripts/python.exe")
SRC = os.environ.get("RUN_SRC", "D:/choptuik-i962/solver/inner_stokes")
LOGS = os.environ.get("RUN_LOGS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"))
BELOW_NORMAL, NEW_GROUP = 0x00004000, 0x00000200
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
BAR = 1e-6
REL = float(os.environ.get("RUN_REL", "1e-7"))
RNGSEED = int(os.environ.get("RUN_RNGSEED", "976"))
MAXREP = int(os.environ.get("RUN_MAXREP", "3"))


def perturbed(end, rel, rng):
    """the end state's harmonics, each times 1 + rel*u, u uniform in (-1, 1), as a --x string (10 significant digits)"""
    return ",".join(f"{float(v) * (1 + rel * (2 * rng.random() - 1)):.10g}" for v in end.split(","))

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
    with open(log, "w", encoding="utf-8", newline="\n") as f:
        p = subprocess.Popen(cmd, cwd=SRC, env=ENV, stdout=f, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL | NEW_GROUP)
        log_driver(f"pid {p.pid}")
        try:
            p.wait(timeout=max(1.0, deadline - time.time()))
        except subprocess.TimeoutExpired:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
            p.wait()
            log_driver(f"cap reached: killed the solve's process tree (taskkill /T /F /PID {p.pid})")
            return None
    return p.returncode


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        return selftest(a)
    xi1, tag = a[0], a[1]
    cap_h = float(a[a.index("--cap_h") + 1]) if "--cap_h" in a else 3.0
    dry = "--dry" in a
    t0 = time.time()
    deadline = t0 + cap_h * 3600
    os.makedirs(LOGS, exist_ok=True)
    drv = open(os.path.join(LOGS, f"run981_{tag}.driver.log"), "a")
    drv.write(f"INNER_NB_RTOL={os.environ.get('INNER_NB_RTOL')} cap {cap_h:g} h, RUN_PY {PY}, RUN_SRC {SRC}, perturb REL {REL:g} "
              f"rngseed {RNGSEED} max {MAXREP} repeats per solve, S {' '.join(S)} (I981's copy of I976's run_job976.py)\n")
    rng = random.Random(RNGSEED)

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
        base = os.path.join(LOGS, f"hier_nb_M7_win2_{tag}_{name}")
        x = Z_X if seeded else None
        tries = []
        first_end = None
        for k in range(1 + MAXREP):
            log = base + (".log" if k == 0 else f"_pert{k}.log")
            if dry:
                log_driver("dry: " + " ".join(cmd_for(A, w, x)) + f" > {log}")
                break
            rc = run(cmd_for(A, w, x), log, deadline, log_driver)
            txt = open(log, encoding="utf-8", errors="replace").read()
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
            if k == 0:
                first_end = end
            if r3 < BAR or k == MAXREP or first_end is None:
                break
            x = perturbed(first_end, REL, rng)  # a repeat from the first attempt's end state, perturbed
            log_driver(f"{name}: |r_3| {r3:.1e} not under {BAR:g}, repeat {k + 1} from its first end state perturbed by {REL:g}: x {x}")
        if dry:
            continue
        # |r_3| of each attempt
        good = [l for l in tries if (parse(open(l, encoding="utf-8", errors="replace").read()) or (0, 9, 0))[1] < BAR]
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
    out = subprocess.run(cmd, cwd=SRC, env=ENV, capture_output=True, text=True, encoding="utf-8", errors="replace",
                         creationflags=BELOW_NORMAL)
    txt = out.stdout + out.stderr + f"(exit {out.returncode})\n"
    with open(os.path.join(LOGS, f"m7_outer_win2_{tag}.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# xi1 {xi1}\n$ {' '.join(cmd)}\n" + txt)
    log_driver("m7_outer.py --local exit " + str(out.returncode) + "; output in logs/m7_outer_win2_" + tag + ".txt")
    print(txt)
    return 0


def selftest(a):
    """the parser and the stop rules on stored logs; --mutate=r3 breaks the r_3 reading, --mutate=endstate drops the harmonics"""
    mut = [t for t in a if t.startswith("--mutate=")]
    mut = mut[0].split("=")[1] if mut else ""
    d = os.path.join(SRC, "logs") + os.sep
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(("ok   " if cond else "FAIL ") + label); ok = ok and cond
    t = open(d + "hier_nb_M7_fixA_xi015_fit3_repeat.log", encoding="utf-8", errors="replace").read()
    r1, r3, end = parse(t)
    if mut == "r3":
        r3 = 1.0 / r3
    chk("fit3_repeat: r_3 1.2e-7, below the bar", abs(r3 - 1.2e-7) < 1e-9 and r3 < BAR)
    chk("fit3_repeat: r_1 -0.0225+0.0424i", abs(r1 - complex(-2.2497e-2, 4.2358e-2)) < 1e-9)
    if mut == "endstate":
        end = ",".join(end.split(",")[:3])
    chk("fit3_repeat: end state is the six 9-decimal harmonics", end is not None and len(end.split(",")) == 6 and end.split(",")[0] == "0.148977988")
    t2 = open(d + "hier_nb_M7_fixA_xi015_newton2_repeat_b.log", encoding="utf-8", errors="replace").read()
    r1b, r3b, endb = parse(t2)
    if mut == "r3":
        r3b = 1e-9
    chk("newton2_repeat_b: r_3 1.5e-5, above the bar (repeat rule fires)", r3b > BAR)
    e = "0.1489782,0.014770826,0.008424259,0.001511207,0.00047421,0.000121682"
    p1, p2 = perturbed(e, 1e-7, random.Random(976)), perturbed(e, 1e-7, random.Random(976))
    if mut == "pert":
        p2 = perturbed(e, 1e-7, random.Random(977))
    chk("perturbed start is reproducible from its rng seed", p1 == p2)
    chk("perturbed start differs from the end state, by at most 1e-7 relative",
        p1 != e and all(abs(float(u) / float(v) - 1) <= 1e-7 + 1e-10 for u, v in zip(p1.split(","), e.split(","))))
    r = random.Random(976)
    q = [perturbed(e, 1e-7, r) for _ in range(3)]
    chk("three repeats from one generator are three different starts", len(set(q)) == 3)
    chk("1.0e-06 as printed is not under the bar (m7_outer's rule)", not (float("1.0e-06") < BAR))
    chk("a log cut before FIXED-A is read as no result", parse("level 3 it 0: |r_3| 1e-3  x [1, 2, 3]\n") is None)
    chk("Traceback before FIXED-A is a crash, the exit BytesIO one is not",
        crashed("Traceback (most recent call last):\nValueError\n") and not crashed(t))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
