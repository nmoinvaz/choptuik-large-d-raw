#!/usr/bin/env python3
"""leg2_pick.py [--mutate=F|steps] [--tag TAG] [--n N] [--log leap.log]: picks the seeds and h of the second leg of the #1025 kc71_leap (the coordinator's hc of
2026-11-22 ~06:40 UTC: "start a new run from its last two saved states with the same flags, h as the run left it, --fold, to D_end 20 ... use the last two
states whose records reproduce"). From the newest record of the first leg back (data/<TAG>.jsonl in the worktree), a state is taken when
kc71_syscheck.py accepts it (its record's |F| within the class bar, |F| of the saved state within 1% of the record's, freeze_from's step count equal to the
record's, with the checker's own two controls); the first two accepted are the seeds. h is the last 'h -> X' of leap.log after the last start or restart header line (whose h argument sets it) (the value the run was using when it
stopped; 0.0625, the first leg's start, when the log has none). Prints 'DA DB H' on the last line and exits 0, or exits 1 when fewer than two states are
accepted. --mutate=F|steps makes the checker's record wrong on purpose: every state must then be refused (exit 1)."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WTM = "D:/choptuik-i1025k71/solver/matter"
tag = "l1kc71Lw1025"; n = 2; mut = None; logp = os.path.join(HERE, "leap.log")
a = sys.argv[1:]
for i, x in enumerate(a):
    if x.startswith("--mutate="): mut = x
    if x == "--tag": tag = a[i + 1]
    if x == "--n": n = int(a[i + 1])
    if x == "--log": logp = a[i + 1]
recs = [json.loads(l) for l in open(f"{WTM}/data/{tag}.jsonl") if l.strip()]
got = []
for r in reversed(recs):
    D = r["D"]
    st = f"{WTM}/data/sol_{tag}_D{D:.6f}.npy"
    if not os.path.exists(st):
        print(f"D {D}: no state file {st}; skipped"); continue
    cmd = [sys.executable, os.path.join(HERE, "kc71_syscheck.py"), f"{WTM}/data/{tag}.jsonl", st, repr(D), WTM] + ([mut] if mut else [])
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
    p = subprocess.run(cmd, capture_output=True, text=True, env=env)
    verdict = [l for l in p.stdout.splitlines() if l.startswith(("ACCEPTED", "NOT ACCEPTED"))]
    print(f"D {D}: exit {p.returncode}: {verdict[0][:160] if verdict else p.stderr[-200:]}")
    if p.returncode == 0:
        got.append(D)
        if len(got) == n: break
if len(got) < n:
    print(f"only {len(got)} state(s) accepted: no second leg"); sys.exit(1)
h = 0.0625
for l in open(logp, errors="replace"):
    if l.startswith("#") and "ell_leap.py" in l and " --tol " in l:  # a start or restart header resets h to its h argument
        h = float(l.split(" --tol ")[0].split()[-1])
    m = re.search(r"h -> ([0-9.eE+-]+)\s*$", l)
    if m and l.startswith(("fold watch", "failed at")): h = float(m.group(1))
DA, DB = sorted(got)
print(f"{DA!r} {DB!r} {h!r}")
