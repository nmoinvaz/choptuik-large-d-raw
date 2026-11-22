#!/usr/bin/env python3
"""#1070 macm3b: the parent chain of the run's processes and the watcher up to pid 1, from one `ps -axo pid,ppid,pgid,sess,tt,command` snapshot.
Usage: session_check_1070.py LABEL  (reads wrapper_pid_LABEL.txt, watcher_pid_LABEL.txt, run_LABEL.log) -> session_check_LABEL.txt. Fails (exit 1) if 'claude' is in any chain."""
import os, re, subprocess, sys, datetime
O = os.path.dirname(os.path.abspath(__file__)); lab = sys.argv[1]
T = {}
for l in subprocess.run(["ps", "-axo", "pid,ppid,pgid,sess,tt,command"], capture_output=True, text=True).stdout.splitlines()[1:]:
    f = l.split(None, 5)
    if len(f) == 6: T[int(f[0])] = f
child = int(re.search(r"child pid (\d+)", open(f"{O}/run_{lab}.log").readline()).group(1))
wp = int(open(f"{O}/wrapper_pid_{lab}.txt").read()); wa = int(open(f"{O}/watcher_pid_{lab}.txt").read())
def descendants(pid):
    kids = [p for p, f in T.items() if int(f[1]) == pid and p != pid]
    return kids + [d for k in kids for d in descendants(k)]
run_tree = [wp] + sorted(descendants(wp))
def chain(pid):
    out = []
    while pid in T:
        out.append(T[pid])
        if pid == 1: break
        pid = int(T[pid][1])
    return out
L = [f"# session check, {datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}: parent chain of each pid up to pid 1 (pid ppid pgid sess tty command); fails if 'claude' is in a chain"]
bad = False
for name, pid in [(f"run process {p} ({'wrapper' if p == wp else 'lowD_gamma.py, the child pid in the log' if p == child else 'caffeinate' if T[p][5].startswith('caffeinate') else 'capped_run.py' if 'capped_run' in T[p][5] else 'other'})", p) for p in run_tree] + [("watcher (watch_1070.py)", wa)]:
    ch = chain(pid); L.append(f"\n{name}:")
    for r in ch:
        L.append(f"  {r[0]:>6} ppid {r[1]:>6} pgid {r[2]:>6} sess {r[3]:>4} tty {r[4]:>3}  {r[5][:110]}")
        bad |= "claude" in r[5].lower()
    L.append(f"  chain ends at pid {ch[-1][0]} ({ch[-1][5][:24]}), {len(ch)} processes")
me = chain(os.getpid())
L.append(f"\nfor comparison, this checker's own chain: " + " <- ".join(f"{r[0]}:{r[5][:14]}" for r in me[:7]) + " ...; its tty " + T[os.getpid()][4])
L.append(f"claude in any chain of the run or the watcher: {bad}")
L.append(f"tty of the run's processes: {T[child][4]} and of the watcher: {T[wa][4]} (?? = no controlling terminal); pgid of the child {T[child][2]}, sess {T[child][3]}")
open(f"{O}/session_check_{lab}.txt", "w").write("\n".join(L) + "\n"); print("\n".join(L)); sys.exit(1 if bad else 0)
