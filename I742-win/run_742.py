#!/usr/bin/env python3
"""#742: the full system from D 113 to 120 with the octo-double corrector, from I739-win/B/anm_pin13_D113.0000.npz (eight parts, M = 32).
usage: python run_742.py M                      (the resumption after the crawl: from I742-win/L/anm_pin13_D117.0000.npz, --steps 6 --h_max 0.5 --a0 0.5, the default own test, anm_run's stop rule; D 117.5, 118, ..., 120)
       python run_742.py --selftest            (the crawl rule of N on planted lines)
       python run_742.py N                      (D 117 to 120 with --od_accept natural, one flag changed from L, from I742-win/L/anm_pin13_D117.0000.npz; --steps 3; stops after the fourth crawling step in a row)
       python run_742.py P                      (the pilot: one step a = 1 from D 113 to D 114, --save_base 1, so its base polish is the control (a))
       python run_742.py L [STATE [STEPS]]      (the chain: default STATE I742-win/P/anm_pin13_D114.0000.npz, default 6 steps; --h_max 1.0 --a0 1.0)
Each run: logs/<name>.log, logs/<name>.exit, logs/run_742.log, output in <name>/. The stop rule is anm_run's own (four refused attempts at one D, the first plus three halvings, then
"stopped: no convergence after three halvings"). Each run is capped (CAP seconds), the cap kills the tree and is logged.
Flags, #739's (#682's plus --elim_switch 0 --corrector od --tol_od 1e-60 --reseed_o 3): --kfreeze 13 --N 24 --eps 1e-14 --D_max 400 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1
          --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --threads 4, cwd = the worktree's hp/, OPENBLAS_NUM_THREADS=1, BelowNormal."""
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
HP = r"C:\Users\nathan\Source\choptuik-i710\hp"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
FLAGS = ["--kfreeze", "13", "--N", "24", "--eps", "1e-14", "--D_max", "400", "--corrector", "od", "--tol_od", "1e-60", "--qd_it", "12", "--jet_q", "1", "--pred_q", "1",
         "--reseed", "2", "--reseed_q", "1", "--reseed_o", "3", "--save_pred", "1", "--a_grow", "1.25", "--a_hold", "1", "--lam_stall", "0.04", "--elim_switch", "0"]
START = "I739-win/B/anm_pin13_D113.0000.npz"
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_742.log"), "a").write(line + "\n")


CRAWL_N = 4          # job N stops after this many crawling steps (lam below 1) in a row within one attempt (the coordinator's message 1794624207651-0)
STEP_LAM = re.compile(r"^\s+on \d+(?: \[full\])?: \|F\| .* lam ([0-9.]+), dDelta")


def crawl_scan(lines, run):
    """the number of crawling steps in a row in the current attempt: a lam 1 step or the end of an attempt resets it"""
    for ln in lines:
        m = STEP_LAM.match(ln)
        if m:
            run = run + 1 if float(m.group(1)) < 1 else 0
        elif ln.startswith("    a ") and "->" in ln:
            run = 0
    return run


def selftest():
    step = lambda n, lam: f"  on {n} [full]: |F| 1.39e-15 -> 6.94e-16, |dz| 1.68e-15 -> 8.42e-16, lam {lam}, dDelta +1.37e-23, piv 1.2e-15..5.0e+15, 239.61 s"
    trial = "    on 1 trial lam 1: max|F| 1.39e-28; raw |dz_t| 2.977e-15 vs |dz| 1.683e-15 (not <); refused, 112.8 s"
    end = "    a 1.000 -> D 118.0: predicted |F| 1.0e-14, od 5 steps -> 1.0e-14"
    cases = [("0 then three crawling steps", [step(0, 1)] + [step(i, 0.5) for i in (1, 2, 3)], 3),
             ("0 then four crawling steps", [step(0, 1)] + [step(i, 0.5) for i in (1, 2, 3, 4)], 4),
             ("a lam 1 step in between resets", [step(1, 0.5), step(2, 0.5), step(3, 1), step(4, 0.5)], 1),
             ("the end of an attempt resets", [step(1, 0.5), step(2, 0.5), end, step(1, 0.5)], 1),
             ("trial lines are not steps", [trial, step(1, 0.5), trial, step(2, 0.5)], 2)]
    bad = 0
    for label, lines, want in cases:
        got = crawl_scan(lines, 0)
        print(f"  {label}: count {got} (expected {want}) {'ok' if got == want else 'WRONG'}")
        bad += got != want
    run = crawl_scan(cases[1][1][:3], 0)
    run = crawl_scan(cases[1][1][3:], run)
    print(f"  four crawling steps in two reads: count {run} {'ok' if run == 4 else 'WRONG'}")
    bad += run != 4
    print("selftest", "FAILED" if bad else "passed")
    return bad


if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
    sys.exit(selftest())
name = sys.argv[1]
if name == "M":
    state, extra, cap = "I742-win/L/anm_pin13_D117.0000.npz", ["--steps", "6", "--h_max", "0.5", "--a0", "0.5"], 21600
elif name == "N":
    state, extra, cap = "I742-win/L/anm_pin13_D117.0000.npz", ["--steps", "3", "--h_max", "1.0", "--a0", "1.0", "--od_accept", "natural"], 18000
elif name == "P":
    state, extra, cap = START, ["--steps", "1", "--h_max", "1.0", "--a0", "1.0", "--save_base", "1"], 7200
elif name == "L":
    state = sys.argv[2] if len(sys.argv) > 2 else "I742-win/P/anm_pin13_D114.0000.npz"
    steps = sys.argv[3] if len(sys.argv) > 3 else "6"
    extra, cap = ["--steps", steps, "--h_max", "1.0", "--a0", "1.0"], 18000
else:
    raise SystemExit("name is P, L, N or M")
out = os.path.join(HERE, name)
os.makedirs(out, exist_ok=True)
cmd = [PY, "-u", "anm_run.py", RAW, out, "--state", state, *FLAGS, *extra, "--threads", "4"]
t0 = time.time()
p = subprocess.Popen(cmd, cwd=HP, stdout=open(os.path.join(HERE, "logs", f"{name}.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
say(f"start {name} (pid {p.pid}) from {state}: {' '.join(extra)}")
reason = None
seen, run = 0, 0
while p.poll() is None:
    time.sleep(5)
    if name == "N":
        with open(os.path.join(HERE, "logs", f"{name}.log"), "rb") as f:
            f.seek(seen)
            data = f.read()
        seen += len(data)
        run = crawl_scan(data.decode("utf-8", "replace").splitlines(), run)
        if run >= CRAWL_N:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
            reason = f"{CRAWL_N} crawling steps in a row (lam below 1), the coordinator's rule for N"
            say(f"{name}: killed the tree, {reason}")
            break
    if time.time() - t0 > cap:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
        reason = f"the {cap} s cap"
        say(f"{name}: killed the tree, {reason}")
        break
rc = p.wait()
open(os.path.join(HERE, "logs", f"{name}.exit"), "w").write(f"{rc}\n")
say(f"{name} exit {rc} after {time.time() - t0:.0f} s" + (f" ({reason})" if reason else ""))
sys.exit(0 if rc == 0 and not reason else 2)
