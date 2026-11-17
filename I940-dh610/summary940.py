#!/usr/bin/env python3
"""#940's closing tables from the window's records, read only.

    python3 -I summary940.py DIR      (DIR is I940-dh610/)

Reads DIR/inputs.txt, DIR/runs/jsonl/*.jsonl (the full-mode jobs and the plan_tol 1e-34 jobs) and DIR/runs_pinned/jsonl/*.jsonl (the pinned jobs on main
18dfeea7). Per D (keyed by its file name) and per record kind (full, full at plan_tol 1e-34, pinned) it takes the last record, with Delta = the four
parts of Delta_q summed in mpmath at 50 digits. Prints: below D 71 the convergence of both starts (|F| < 1e-45), the pin 5 minus pin 7 difference
(bar 1e-26), the plan_tol 1e-34 change; from D 71 the pinned convergence, the pin gap per D, and which full solves converge; and the pairing check
that costs no runs: pin 5 at each D against pin 7 at the next D (the difference must exceed 1e-26, so that the agreement test can fail)."""
import glob
import json
import os
import re
import sys

from mpmath import mp, mpf

mp.dps = 50
DIR = sys.argv[1]
rows = [l.split() for l in open(os.path.join(DIR, "inputs.txt"))]
rec = {}


def load(pattern, kind_of):
    for f in sorted(glob.glob(os.path.join(DIR, pattern))):
        for line in open(f):
            r = json.loads(line)
            m = re.search(r"pin([57])_D([0-9.]+)\.npz", r["source"])
            if not m:
                continue
            rec[(kind_of(r), m.group(1), m.group(2).rstrip("0").rstrip(".") if "." in m.group(2) else m.group(2))] = r


load("runs/jsonl/*.jsonl", lambda r: "full_p34" if r.get("plan_tol") == 1e-34 else r["mode"])
load("runs_pinned/jsonl/*.jsonl", lambda r: r["mode"])


def delta(r):
    return sum((mpf(x) for x in r["Delta_q"]), mpf(0))


def key(D):
    s = D
    return s.rstrip("0").rstrip(".") if "." in s else s


def get(kind, pin, D):
    return rec.get((kind, pin, key(D)))


def fmt(x, n=3):
    return mp.nstr(x, n)


print("### Below D 71: `--mode full`, both starts\n")
print("| D | pin 5 conv, \\|F\\|, steps | pin 7 conv, \\|F\\|, steps | Delta(pin 5) - Delta(pin 7) | within 1e-26 | plan_tol 1e-34 minus 1e-32 (pin 5) |")
print("|---|---|---|---|---|---|")
bad = []
for D, p5, p7 in rows:
    if float(D) >= 71:
        continue
    a, b, c = get("full", "5", D), get("full", "7", D), get("full_p34", "5", D)
    if not a or not b:
        print(f"| {D} | {'pending' if not a else ''} | {'pending' if not b else ''} | | | |")
        continue
    cv = lambda r: f"{'yes' if r['conv'] else 'NO'}, {r['F']:.1e}, {r['steps']}"
    d = delta(a) - delta(b)
    ok = a["conv"] and b["conv"] and a["F"] < 1e-45 and b["F"] < 1e-45
    if not ok:
        bad.append((D, a["F"], b["F"]))
    print(f"| {D} | {cv(a)} | {cv(b)} | {fmt(d)} | {'yes' if abs(d) < 1e-26 else 'NO'} | {fmt(delta(c) - delta(a)) if c else 'pending'} |")
print("\nBelow 71, starts not both converged below 1e-45:", bad if bad else "none")

print("\n### From D 71: `--mode pinned` on both pins, and `--mode full` on both\n")
print("| D | pinned pin 5 conv, \\|F\\|, steps | pinned pin 7 conv, \\|F\\|, steps | Delta(pin 5) - Delta(pin 7) (pin gap) | full pin 5 conv, \\|F\\| | full pin 7 conv, \\|F\\| |")
print("|---|---|---|---|---|---|")
for D, p5, p7 in rows:
    if float(D) < 71:
        continue
    a, b = get("pinned", "5", D), get("pinned", "7", D)
    fa, fb = get("full", "5", D), get("full", "7", D)
    cv = lambda r: "pending" if not r else f"{'yes' if r['conv'] else 'NO'}, {r['F']:.1e}" + (f", {r['steps']}" if r["mode"] == "pinned" else "")
    gap = fmt(delta(a) - delta(b)) if a and b else "pending"
    print(f"| {D} | {cv(a)} | {cv(b)} | {gap} | {cv(fa)} | {cv(fb)} |")

print("\n### Pairing check: pin 5 at D_i against pin 7 at D_i+1 (must fail the 1e-26 agreement test)\n")
print("| D_i | D_i+1 | mode | Delta(pin 5, D_i) - Delta(pin 7, D_i+1) | exceeds 1e-26 |")
print("|---|---|---|---|---|")
nfail = ntot = 0
for (D, _, _), (E, _, _) in zip(rows, rows[1:]):
    mode = "full" if float(D) < 71 and float(E) < 71 else "pinned" if float(D) >= 71 else None
    if not mode:
        continue
    a, b = get(mode, "5", D), get(mode, "7", E)
    if not a or not b:
        continue
    d = delta(a) - delta(b)
    ntot += 1
    nfail += abs(d) > 1e-26
    print(f"| {D} | {E} | {mode} | {fmt(d)} | {'yes' if abs(d) > 1e-26 else 'NO'} |")
print(f"\nPairs that fail the agreement test (difference above 1e-26): {nfail} of {ntot}")

# ---- aggregates for the closing
print("\n### Aggregates\n")
low = [(D, get("full", "5", D), get("full", "7", D), get("full_p34", "5", D)) for D, _, _ in rows if float(D) < 71]
both = [(D, a, b, c) for D, a, b, c in low if a and b and a["conv"] and b["conv"] and a["F"] < 1e-45 and b["F"] < 1e-45]
print(f"below D 71: {len(low)} D, both starts converge below 1e-45 at {len(both)}; pin 5 only fails at {sum(1 for D,a,b,c in low if not (a['conv'] and a['F']<1e-45) and (b['conv'] and b['F']<1e-45))}, pin 7 only fails at {sum(1 for D,a,b,c in low if (a['conv'] and a['F']<1e-45) and not (b['conv'] and b['F']<1e-45))}, both fail at {sum(1 for D,a,b,c in low if not (a['conv'] and a['F']<1e-45) and not (b['conv'] and b['F']<1e-45))}")
ds = [abs(delta(a) - delta(b)) for D, a, b, c in both]
print(f"where both converge: |Delta(pin 5) - Delta(pin 7)| max {fmt(max(ds))}, median {fmt(sorted(ds)[len(ds)//2])}; within 1e-26 at {sum(1 for d in ds if d < 1e-26)} of {len(ds)}")
ps = [(D, delta(c) - delta(a)) for D, a, b, c in both if c and c["conv"]]
if ps:
    v = [abs(x) for _, x in ps]
    print(f"plan_tol 1e-34 minus 1e-32 (pin 5, both converged): {len(ps)} D, |change| min {fmt(min(v))}, median {fmt(sorted(v)[len(v)//2])}, max {fmt(max(v))}")
hi = [(D, get("pinned", "5", D), get("pinned", "7", D), get("full", "5", D), get("full", "7", D)) for D, _, _ in rows if float(D) >= 71]
print(f"from D 71: {len(hi)} D, pinned converges at {sum(1 for D,a,b,fa,fb in hi if a and b and a['conv'] and b['conv'])} of {len(hi)} (both pins), max |F| {max(max(a['F'],b['F']) for D,a,b,fa,fb in hi):.2e}")
gaps = [delta(a) - delta(b) for D, a, b, fa, fb in hi]
print(f"pin gap Delta(pin 5) - Delta(pin 7): min {fmt(min(gaps))}, max {fmt(max(gaps))}, median |gap| {fmt(sorted(abs(g) for g in gaps)[len(gaps)//2])}")
fc = [(D, fa, fb) for D, a, b, fa, fb in hi]
print(f"full mode from 71: pin 5 converges at {sum(1 for D,fa,fb in fc if fa and fa['conv'])} of {len(fc)}, pin 7 at {sum(1 for D,fa,fb in fc if fb and fb['conv'])} of {len(fc)}; last D with a converged full solve: {max([float(D) for D,fa,fb in fc if (fa and fa['conv']) or (fb and fb['conv'])], default=None)}")
