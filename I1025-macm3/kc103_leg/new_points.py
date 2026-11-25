#!/usr/bin/env python3
"""new_points.py REC DATA TAG PUSHED: prints the D (repr), one per line, oldest first, of each record in REC whose state file DATA/sol_TAG_D<D:.6f>.npy exists and whose D is not listed in PUSHED."""
import json, os, sys
rec, data, tag, pushed = sys.argv[1:5]
done = set(open(pushed).read().split()) if os.path.exists(pushed) else set()
rows = []
if os.path.exists(rec):
    for l in open(rec):
        try: rows.append(json.loads(l))
        except ValueError: pass          # a line still being written
for r in rows:
    D = r["D"]
    if repr(D) not in done and os.path.exists(os.path.join(data, "sol_%s_D%.6f.npy" % (tag, D))):
        print(repr(D))
