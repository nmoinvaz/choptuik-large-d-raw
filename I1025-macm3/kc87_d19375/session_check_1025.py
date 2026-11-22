#!/usr/bin/env python3
"""#1025 macm3b kc79_d1925: the parent chain of the given pids up to pid 1, from one `ps -axo pid,ppid,pgid,sess,tt,command` snapshot, and of every descendant of the first pid.
Usage: session_check_1025.py LABEL PID [PID ...] -> session_check_LABEL.txt. Exit 1 if 'claude' is in any chain."""
import datetime, os, subprocess, sys
O = os.path.dirname(os.path.abspath(__file__)); lab = sys.argv[1]; pids = [int(x) for x in sys.argv[2:]]
T = {}
for l in subprocess.run(["ps", "-axo", "pid,ppid,pgid,sess,tt,command"], capture_output=True, text=True).stdout.splitlines()[1:]:
    f = l.split(None, 5)
    if len(f) == 6: T[int(f[0])] = f
def desc(p): 
    k = [q for q, f in T.items() if int(f[1]) == p and q != p]
    return k + [d for q in k for d in desc(q)]
def chain(p):
    out = []
    while p in T:
        out.append(T[p])
        if p == 1: break
        p = int(T[p][1])
    return out
todo = []
for p in pids:
    for q in [p] + sorted(desc(p)):
        if q not in todo: todo.append(q)
L = [f"# session check, {datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}: parent chain of each pid (the given ones and their descendants) up to pid 1 (pid ppid pgid sess tty command); fails if 'claude' is in a chain"]
bad = False
for p in todo:
    if p not in T: L.append(f"\npid {p}: not running"); continue
    ch = chain(p); L.append(f"\npid {p} ({T[p][5][:60]}):")
    for r in ch:
        L.append(f"  {r[0]:>6} ppid {r[1]:>6} pgid {r[2]:>6} tty {r[4]:>3}  {r[5][:100]}"); bad |= "claude" in r[5].lower()
    L.append(f"  chain ends at pid {ch[-1][0]} ({ch[-1][5][:20]}), {len(ch)} processes")
me = chain(os.getpid()); L.append("\nfor comparison, this checker's own chain: " + " <- ".join(f"{r[0]}:{r[5][:14]}" for r in me[:7]) + " ...")
L.append(f"claude in any chain of the run: {bad}; tty of the pids: " + ", ".join(sorted({T[p][4] for p in todo if p in T})) + " (?? = no controlling terminal)")
open(f"{O}/session_check_{lab}.txt", "w").write("\n".join(L) + "\n"); print("\n".join(L)); sys.exit(1 if bad else 0)
