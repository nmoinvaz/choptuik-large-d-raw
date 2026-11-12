#!/usr/bin/env python3
"""#583: B = 3e-15 fixed on the issue before the test data were read. For each circle folder (one circle, one process, its own
cache) read only the circle's closure (res.jsonl: resolved, winding) and, for EVERY evaluation of its cache, pmin.
    python3 read_pmin.py DIR [DIR ...]      (DIR holds circle folders with *_evals.jsonl and res.jsonl)
Prints per circle: closure, evaluations, smallest pmin, evaluations below B, evaluations within a factor 2 of B; and the verdict of
the issue's prediction: every closed circle has all its points at pmin >= B."""
import glob
import json
import os
import sys

B = 3e-15
rows = []
for d in sys.argv[1:]:
    for sub in sorted(glob.glob(os.path.join(d, "*/"))):
        evs = glob.glob(os.path.join(sub, "*_evals.jsonl"))
        res = os.path.join(sub, "res.jsonl")
        if not evs:
            continue
        pm = [json.loads(l)["pmin"] for f in evs for l in open(f) if l.strip()]
        rr = [json.loads(l) for l in open(res)] if os.path.exists(res) else []
        closed = bool(rr) and all(r.get("resolved") for r in rr)
        rows.append((os.path.basename(os.path.dirname(d.rstrip("/"))) + "/" + os.path.basename(sub.rstrip("/")), closed,
                     [r.get("winding") for r in rr], len(pm), min(pm), sum(p < B for p in pm), sum(B / 2 <= p <= 2 * B for p in pm)))
print("| circle | closed | winding | evaluations | smallest pmin | below B | within a factor 2 of B |")
print("|---|---|---|---|---|---|---|")
for n, c, w, k, m, b, f in rows:
    print(f"| {n} | {'yes' if c else 'NO'} | {', '.join(f'{x:+.0f}' for x in w) if w else '-'} | {k} | {m:.3e} | {b} | {f} |")
closed = [r for r in rows if r[1]]
bad = [r for r in closed if r[5] > 0]
print()
print(f"circles {len(rows)}, closed {len(closed)}, evaluations {sum(r[3] for r in rows)}; closed circles with a point below B: {len(bad)}; "
      f"smallest pmin over all {min(r[4] for r in rows):.3e}; points below B {sum(r[5] for r in rows)}; within a factor 2 of B {sum(r[6] for r in rows)}")
sys.exit(1 if bad else 0)
