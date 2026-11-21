#!/usr/bin/env python3
"""#1025 winb follow-on, row B's dd sign check (the coordinator's order after Amendment 1): when the hybrid row B (D 17.75) has its root, run
ell_ddm.py det on the row's state at root - 0.02 and root + 0.02, two processes in parallel, --noise 1e-24,1e-20,1e-16, each capped at 3 h and killed
at the cap by its exact pid (taskkill /PID <pid> /T /F on the process this driver started, never by name). Then read_ddB_1025.py gives the reading.
A thin driver: it runs xfkappa's ell_ddm.py unchanged (worktree choptuik-i1025d at wip/ell1-highD 48c36355).
usage: ddB_driver_1025.py           (waits for 'row B D 17.75: hybrid done' in p4hi_w.log)
       ddB_driver_1025.py --selftest   (the pair runner with dummy commands: one ends, one is killed at a 6 s cap)"""
import datetime, json, os, re, subprocess, sys, time

OUT = "C:/Users/nathan/Source/p4hi_1025/I1025-win/p4_highD"
HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
WT = "C:/Users/nathan/Source/choptuik-i1025d"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
STATE = "C:/Users/nathan/Source/p4hi_1025/raw/I1025-win/out/sol_l1kc63W1025_D17.750000.npy"
STATE_BLOB = "de9fc3e55aa46bafd4ef62536861f94aed9e3035"
D, KC = "17.75", "63"
P4LOG, JS = OUT + "/p4hi_w.log", OUT + "/ell_p4_hybrid_1025_w_highD.jsonl"
LOG = OUT + "/ddB_w.log"
CAP = 10800


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def pids_below(pid):
    r = subprocess.run(["powershell", "-NoProfile", "-Command",
                        f"(Get-CimInstance Win32_Process -Filter 'ParentProcessId={pid}' | ForEach-Object {{ $_.ProcessId }}) -join ','"],
                       capture_output=True, text=True)
    return r.stdout.strip()


def run_pair(cmds, logs, cap, cwd, env):
    """start both, poll, kill any still running at the cap by exact pid; returns the exit codes (None = killed at the cap)"""
    procs, t0 = [], time.time()
    for c, lg in zip(cmds, logs):
        f = open(lg, "w")
        p = subprocess.Popen(c, cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        procs.append((p, f, lg))
        say(f"started pid {p.pid}: {' '.join(c)} > {lg}")
    time.sleep(20)
    for p, f, lg in procs:
        say(f"pid {p.pid}: child pids {pids_below(p.pid)}")
    rcs = [None] * len(procs)
    while any(r is None for r in rcs):
        for i, (p, f, lg) in enumerate(procs):
            if rcs[i] is None:
                rc = p.poll()
                if rc is not None:
                    rcs[i] = rc
                    say(f"pid {p.pid} ended with exit {rc} after {time.time() - t0:.0f} s")
                elif time.time() - t0 > cap:
                    r = subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True, text=True)
                    say(f"CAP {cap} s: killed pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
                    p.wait()
                    rcs[i] = "killed at the cap"
        if any(r is None for r in rcs):
            time.sleep(10)
    return rcs


if "--selftest" in sys.argv:
    LOG = HERE + "/ddB_driver_selftest.log"
    open(LOG, "w").close()
    quick = [PY, "-c", "import time; print('quick child', flush=True); time.sleep(3)"]
    slow = [PY, "-c", "import time; print('slow child', flush=True); time.sleep(600)"]
    t = time.time()
    rcs = run_pair([quick, slow], [HERE + "/ddB_selftest_a.log", HERE + "/ddB_selftest_b.log"], 6, HERE, dict(os.environ))
    left = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'time.sleep\\(600\\)' } | Measure-Object | Select-Object -ExpandProperty Count"],
                          capture_output=True, text=True).stdout.strip()
    say(f"selftest: exit codes {rcs} in {time.time() - t:.0f} s; processes of the slow child still alive: {left}")
    sys.exit(0 if rcs[0] == 0 and rcs[1] == "killed at the cap" and left == "0" else 1)

say(f"ddB_driver_1025.py: waiting for 'row B D {D}: hybrid done' in {P4LOG}")
while True:
    txt = open(P4LOG, errors="replace").read()
    if f"row B D {D}: hybrid done" in txt:
        break
    if re.search(rf"row B D {re.escape(D)}: (TIMEOUT|CRASH)", txt) or "p4hi_driver_1025.sh done" in txt:
        say("row B has no hybrid root (timeout, crash or driver end): no dd check run")
        sys.exit(1)
    time.sleep(30)
blob = subprocess.run(["git", "hash-object", "--no-filters", STATE], capture_output=True, text=True).stdout.strip()
if blob != STATE_BLOB:
    say(f"REFUSE: {STATE} is blob {blob}, not {STATE_BLOB}")
    sys.exit(2)
rec = [json.loads(l) for l in open(JS) if l.strip() and abs(json.loads(l)["D"] - float(D)) < 1e-9][-1]
root = rec["lam"]
lo, hi = root - 0.02, root + 0.02
say(f"row B root {root!r} (bracket {rec['bracket']}); dd points {lo!r} and {hi!r}; state blob {blob}")
env = dict(os.environ, OPENBLAS_NUM_THREADS="4", OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", PYTHONDONTWRITEBYTECODE="1")
cwd = WT + "/solver/matter"
lojs, hijs = OUT + "/rows/ell_ddm_B_D17.75_lo.jsonl", OUT + "/rows/ell_ddm_B_D17.75_hi.jsonl"
cmds = [[PY, "-u", "ell_ddm.py", "det", STATE, D, KC, repr(x), "--noise", "1e-24,1e-20,1e-16", "--out", js] for x, js in ((lo, lojs), (hi, hijs))]
rcs = run_pair(cmds, [OUT + "/rows/ddB_lo.log", OUT + "/rows/ddB_hi.log"], CAP, cwd, env)
say(f"both ended: {rcs}")
r = subprocess.run([PY, HERE + "/read_ddB_1025.py", lojs, hijs, repr(root)], capture_output=True, text=True)
open(OUT + "/rows/ddB_reading.log", "w").write(r.stdout + r.stderr)
for l in r.stdout.splitlines():
    say(l)
say("ddB_driver_1025.py done")
