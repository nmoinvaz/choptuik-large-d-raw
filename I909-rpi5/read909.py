#!/usr/bin/env python3
"""#909: the issue's acceptance from profile.jsonl (sweep A) and profileB.jsonl (sweep B).  python3 read909.py FOLDER
Per Delta: the least |F| of each sweep, the Jacobians, the ratio of the larger to the smaller, the smallest singular value
of J without its Delta column. Then: both sweeps hold Delta at every point; every ratio at most 2 (Delta decides);
the count of ratios above 3 against half of the points (branch decides); the Delta whose |F| is below half of both
neighbours' in each sweep (solution candidates, read only if Delta decides)."""
import json, os, sys
R = sys.argv[1]
def pts(f):
    return {round(p["target"], 6): p for p in [json.loads(l) for l in open(os.path.join(R, f)) if l.strip()][-1]["points"]}
pa, pb = pts("profile.jsonl"), pts("profileB.jsonl")
ds = sorted(pa)
print("| Delta | A least \\|F\\| | A Jac | B least \\|F\\| | B Jac | ratio larger/smaller | A smallest sv | B smallest sv |")
print("|---|---|---|---|---|---|---|---|")
r = {}
for d in ds:
    a, b = pa[d], pb[d]
    r[d] = max(a["F"], b["F"]) / min(a["F"], b["F"])
    print(f"| {d:.3f} | {a['F']:.4e} | {a['jac']} | {b['F']:.4e} | {b['jac']} | {r[d]:.3f} | {a['s_low'][0]:.2e} | {b['s_low'][0]:.2e} |")
held = all(p["held"] for p in list(pa.values()) + list(pb.values()))
n2, n3 = sum(x > 2 for x in r.values()), sum(x > 3 for x in r.values())
print(f"\nDelta held at every point of both sweeps: {held}")
print(f"ratios above 2: {n2} of {len(ds)} (Delta decides needs 0); above 3: {n3} of {len(ds)} (branch decides needs {len(ds) / 2:g} or more)")
for name, P in (("A", pa), ("B", pb)):
    F = [P[d]["F"] for d in ds]
    c = [ds[i] for i in range(1, len(ds) - 1) if F[i] < 0.5 * F[i - 1] and F[i] < 0.5 * F[i + 1]]
    print(f"sweep {name}: least |F| {min(F):.4e} at Delta {ds[F.index(min(F))]:.3f}; below half of both neighbours: {c if c else 'none'}")
verdict = "Delta decides" if n2 == 0 else "branch decides" if n3 >= len(ds) / 2 else "between (reported)"
print("reading by the frozen rule:", verdict)
