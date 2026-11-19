"""#1028 (the coordinator's hc, 2026-11-19 ~14:19 UTC): four M = 9 centre solves at (A 2.719219, w/w_inf 1.000022) side by side, seeded from Z's harmonics as #1012's stage 1 with
those six harmonics (B3 C3 B5 C5 B7 C7) scaled by 1 + 1e-9 (p1), 1 - 1e-9 (m1), 1 + 3e-9 (p3) and 1 - 3e-9 (m3). Settings as stage 1 (#1012's logs; code D:/choptuik-h9b = main 299c4eb9, which differs from
stage 1's 23844822 only in the --h9 plumbing, diffed): --xi1=0.15 --pretune --fixA --schur --predict --procs 2 --h3=1e-4 --h5=1e-4 --floor_max=1e-4 --verbose=2 --approach=5:0.105 --polish=5:0.11,
INNER_NB_RTOL=1e-13, BelowNormal, 3 h caps.

    python chain1028.py [--selftest [--mutate=nofactor|nokill|badreadback]]          (from this folder)

Logs logs/hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-4_seed_<name>_win2.log, .exit files, driver log logs/run1028.driver.log. The driver reads each log back as it runs: the `pretuned x` line's harmonics x[2:8]
must equal Z x (1 + eps) of that run (|ratio - 1 - eps| < 1e-14) and (A, w) = (2.719219, 1.000022); the K line must say 10 residuals (--predict); each level-5 solve's end is logged. A mismatch is logged as PLUMBING MISMATCH.
--selftest: checks each command's --x= against Z x (1 + eps), runs four stubs (cap 3 s; they print a pretuned-x line and a K line) that the readback must accept and that must leave no process;
--mutate=nofactor builds p1 without its factor (the command check must fail), --mutate=nokill leaves the stubs (must fail), --mutate=badreadback makes m3's stub print unscaled harmonics (the readback must flag it)."""
import os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("RUN_PY", "C:/Users/nathan/Source/venv-i962/Scripts/python.exe")
SRC = os.environ.get("RUN_SRC", "D:/choptuik-h9b/solver/inner_stokes")
Z = [0.148977988, 0.014770713, 0.008424206, 0.001511189, 0.000474205, 0.00012168]
A0, W0 = "2.719219", "1.000022"
BELOW_NORMAL, NEW_GROUP = 0x00004000, 0x00000200
ENV = dict(os.environ, INNER_NB_RTOL="1e-13", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
LOGS = os.path.join(HERE, "logs")
SELF = "--selftest-inner" in sys.argv
CAP = 3.0 if SELF else 10800.0
os.makedirs(LOGS, exist_ok=True)
drv = open(os.path.join(LOGS, "run1028.selftest.driver.log" if SELF else "run1028.driver.log"), "a")
RUNS = [dict(name="p1", eps=1e-9), dict(name="m1", eps=-1e-9), dict(name="p3", eps=3e-9), dict(name="m3", eps=-3e-9)]


def say(s):
    line = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " " + s
    print(line, flush=True)
    drv.write(line + "\n")
    drv.flush()


def xs_of(r, mut=False):
    eps = 0.0 if (mut and r["name"] == "p1") else r["eps"]          # --mutate=nofactor: p1 loses its factor
    return [repr(z * (1.0 + eps)) for z in Z]


def command(r, mut=False):
    c = [PY, "-u", "hier_nb.py", "9", A0, W0, "--x=" + ",".join(xs_of(r, mut))]
    return c + ["--xi1=0.15", "--pretune", "--fixA", "--schur", "--predict", "--procs", "2", "--h3=1e-4", "--h5=1e-4", "--floor_max=1e-4", "--verbose=2", "--approach=5:0.105", "--polish=5:0.11"]


def check_commands(mut=False):
    ok = True
    for r in RUNS:
        c = command(r, mut)
        xs = [float(t) for t in [a for a in c if a.startswith("--x=")][0][4:].split(",")]
        dev = max(abs(x / z - 1 - r["eps"]) for x, z in zip(xs, Z))
        good = dev < 1e-14 and c[4:6] == [A0, W0] and all(k in c for k in ("--predict", "--h5=1e-4", "--floor_max=1e-4", "--schur", "--fixA", "--pretune", "--approach=5:0.105", "--polish=5:0.11"))
        say(f"command check {r['name']}: eps {r['eps']:+.0e}, max |x/Z - 1 - eps| {dev:.1e} -> {'ok' if good else 'FAIL'}")
        ok = ok and good
    return ok


def read(path):
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def readback(t, eps):
    m = re.search(r"^pretuned x \[(.*?)\]", t, re.M)
    if not m:
        return None
    x = [float(v) for v in m.group(1).split(",")]
    dev = max(abs(a / z - 1 - eps) for a, z in zip(x[2:8], Z))
    return abs(x[0] - float(A0)) < 1e-12 and abs(x[1] - float(W0)) < 1e-12 and dev < 1e-14, dev


def main():
    runs = {}
    for r in RUNS:
        tag = f"hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-4_seed_{r['name']}_win2" + ("_selftest" if SELF else "")
        if SELF:
            xs = [z * (1.0 + (0.0 if (r["name"] == "m3" and "--mutate=badreadback" in sys.argv) else r["eps"])) for z in Z]
            code = ("import time\nprint('pretuned x ' + repr([%s, %s] + %r + [1e-5, 1e-6]), flush=True)\nprint('   Jacobian K computed (10 residuals) [5 s]', flush=True)\ntime.sleep(60)" % (A0, W0, xs))
            cmd = [PY, "-c", code]
        else:
            cmd = command(r)
        f = open(os.path.join(LOGS, tag + ".log"), "w", encoding="utf-8", newline="\n")
        p = subprocess.Popen(cmd, cwd=SRC, env=ENV, stdout=f, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL | NEW_GROUP)
        runs[tag] = dict(p=p, f=f, t0=time.time(), r=r, seen=0, k=False, rb=False)
        say(f"start ({r['name']}, harmonics x (1 {r['eps']:+.0e})) pid {p.pid}: {' '.join(cmd[2:]) if not SELF else 'stub'} > logs/{tag}.log")
    mismatches = 0
    while runs:
        time.sleep(0.5 if SELF else 10)
        for tag in list(runs):
            x = runs[tag]
            p, r = x["p"], x["r"]
            t = read(os.path.join(LOGS, tag + ".log"))
            if not x["rb"]:
                rb = readback(t, r["eps"])
                if rb is not None:
                    x["rb"] = True
                    say(f"({r['name']}) readback of the pretuned x line: harmonics / Z - 1 - eps max {rb[1]:.1e}, (A, w) ok: " + ("ok" if rb[0] else "PLUMBING MISMATCH"))
                    mismatches += 0 if rb[0] else 1
            sol = [float(v) for v in re.findall(r"level 5 solved: \|r_5\| (\S+)", t)]
            while x["seen"] < len(sol):
                v = sol[x["seen"]]
                x["seen"] += 1
                say(f"({r['name']}) level-5 solve {x['seen']} ended " + (f"below 1e-6 ({v:.2e})" if v < 1e-6 else f"at {v:.2e}"))
            m = re.search(r"Jacobian K computed \((\d+) residuals\)", t)
            if m and not x["k"]:
                x["k"] = True
                say(f"({r['name']}) K line: {m.group(1)} residuals (want 10 with --predict): " + ("ok" if m.group(1) == "10" else "PLUMBING MISMATCH"))
                mismatches += 0 if m.group(1) == "10" else 1
            rc, note = p.poll(), ""
            if rc is None and time.time() - x["t0"] > CAP:
                if "--mutate=nokill" not in sys.argv:
                    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
                    p.wait()
                rc, note = "capped", f" (killed the process tree at the {CAP:g} s cap, taskkill /T /F /PID {p.pid})"
            if rc is not None:
                x["f"].close()
                msg = f"exit {rc}{note} after {time.time() - x['t0']:.0f} s, ended {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC"
                open(os.path.join(LOGS, tag + ".exit"), "w").write(msg + "\n")
                say(f"({r['name']}) {msg}")
                del runs[tag]
    say(f"driver done; plumbing mismatches: {mismatches}")


def selftest():
    try:
        os.remove(os.path.join(LOGS, "run1028.selftest.driver.log"))
    except OSError:
        pass
    mut = [a for a in sys.argv if a.startswith("--mutate=")]
    cmd_ok = check_commands("--mutate=nofactor" in sys.argv)
    subprocess.run([sys.executable, os.path.abspath(__file__), "--selftest-inner"] + mut, capture_output=True, text=True)
    log = open(os.path.join(LOGS, "run1028.selftest.driver.log"), encoding="utf-8").read()
    pids = [int(x) for x in re.findall(r"pid (\d+):", log)]
    alive = [pid for pid in pids if subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout.split().count(str(pid))]
    nrb_ok, nrb_bad, nk_ok = len(re.findall(r"readback .*: ok$", log, re.M)), log.count("PLUMBING MISMATCH"), len(re.findall(r"K line: 10 residuals .*: ok$", log, re.M))
    ok = cmd_ok and not alive and len(pids) == 4 and nrb_ok == 4 and nrb_bad == 0 and nk_ok == 4
    print(f"commands carry the right factors: {cmd_ok}; stubs {len(pids)} (want 4); readbacks ok {nrb_ok} (want 4), flagged {nrb_bad} (want 0), K lines ok {nk_ok} (want 4); alive after the cap {alive} -> selftest {'PASS' if ok else 'FAIL'}", flush=True)
    for fn in os.listdir(LOGS):
        if fn.endswith("_selftest.log") or fn.endswith("_selftest.exit"):
            try:
                os.remove(os.path.join(LOGS, fn))
            except OSError:
                pass
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
    sys.exit(0)
