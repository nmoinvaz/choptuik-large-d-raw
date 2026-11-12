#!/usr/bin/env python3
"""Summary of the mode-count circles of #573 and #574: one row per circle folder with its state (running / done / cap), evaluations so far, winding, points, resolved flag and the zeros inside.
usage: python summ_57x.py [TASK ...]       (default both tasks; run from any directory; reads <RAW>/<task>/<circle>/res.jsonl, cap.json and the evaluation caches)"""
import glob, json, os, sys
RAW = "D:/choptuik-large-d-raw"
tasks = sys.argv[1:] or ["I573-win2", "I574-win2"]
for task in tasks:
    print(f"\n== {task}\n| circle | state | evals so far | winding | points | resolved | max step | zeros inside (estimate) |\n|---|---|---|---|---|---|---|---|")
    for d in sorted(glob.glob(os.path.join(RAW, task, "k*"))):
        name = os.path.basename(d)
        ev = sum(1 for _ in open(g)) if (g := next(iter(glob.glob(os.path.join(d, "modecount_*_evals.jsonl"))), None)) else 0
        res = os.path.join(d, "res.jsonl")
        if os.path.exists(os.path.join(d, "cap.json")):
            print(f"| {name} | cap | {ev} | | | | | |")
        elif os.path.exists(res) and os.path.getsize(res):
            r = [json.loads(l) for l in open(res)][-1]
            z = "; ".join(f"{a:.6f} {b:+.6f}i ({e:.0e})" for (a, b), e in zip(r.get("zeros", []), r.get("zeros_est", [])))
            print(f"| {name} | done | {ev} | {r['winding']:+.4f} | {r['points']} | {'yes' if r['resolved'] else 'NO'} | {r['max_step']:.3f} | {z} |")
        else:
            print(f"| {name} | running | {ev} | | | | | |")
