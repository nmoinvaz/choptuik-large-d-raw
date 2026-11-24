#!/usr/bin/env python3
"""dry_guard_pid.py: the macOS shims (shims_mac/, first on PATH) read and kill by EXACT pid with the pinned leap_guard.py (imported, unmodified), on the leg's wrapper chain
  nice -n 10 python in/capped_run.py 600 env OMP_NUM_THREADS=1 python -c 'sleep' ell_leap.py      (macOS has no timeout: capped_run.py is the cap by exact child pid)
Also a decoy (same command text, other pid). Checks: the guard's cmdline(root) holds ell_leap.py; stop_leap on a process without the key says 'left'; stop_leap(root) says
'killed', the root and its descendants are dead and the decoy is alive. --mutate=decoy asks the guard to kill the decoy's pid instead (the check must then fail)."""
import os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "in"))
import leap_guard as g
mut = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
py = sys.executable
code = "import time; time.sleep(300)"
procs = []
def spawn(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    procs.append(p)
    return p
def kids(pid):
    return [int(x) for x in subprocess.run(["pgrep", "-P", str(pid)], capture_output=True, text=True).stdout.split()]
bad = []
child = []; grand = []
try:
    decoy = spawn([py, "-c", code, "ell_leap.py"])
    root = spawn(["nice", "-n", "10", py, os.path.join(HERE, "in", "capped_run.py"), "600", "env", "OMP_NUM_THREADS=1", py, "-c", code, "ell_leap.py"])
    time.sleep(3)
    child = kids(root.pid)
    grand = [c for k in child for c in kids(k)]
    cl = g.cmdline(root.pid)
    print("root pid %d cmdline: %s" % (root.pid, (cl or "")[:200]))
    print("children of the root %s, grandchildren %s, decoy %d" % (child, grand, decoy.pid))
    if not cl or g.KEY not in cl: bad.append("the guard's cmdline() of the root does not hold ell_leap.py")
    if not child: bad.append("the root has no child process (the chain did not start)")
    r_self = g.stop_leap(os.getpid(), key="no-such-key-xyz")
    if r_self != "left": bad.append("a process without the key was not left (%s)" % r_self)
    target = decoy.pid if mut == "decoy" else root.pid
    r = g.stop_leap(target)
    time.sleep(1.5)
    print("stop_leap(%d) -> %s" % (target, r))
    if r != "killed": bad.append("stop_leap returned %s" % r)
    if g.alive(root.pid): bad.append("the root %d is alive" % root.pid)
    for c in child + grand:
        if g.alive(c): bad.append("a descendant %d is alive" % c)
    if not g.alive(decoy.pid): bad.append("the decoy %d (other pid, same text) was killed" % decoy.pid)
finally:
    for p in procs:
        if p.poll() is None: p.kill()
    for c in child + grand:                       # orphans of a root that was not the one killed (the mutation)
        try: os.kill(c, 9)
        except OSError: pass
for b in bad: print("DRY FAIL:", b)
print("dry run %s%s" % ("FAILS" if bad else "passes", " (mutate=%s)" % mut if mut else ""))
sys.exit(1 if bad else 0)
