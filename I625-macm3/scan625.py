#!/usr/bin/env python3
"""Tables of #625's option (b) scans: the M 48 sign pattern over k = -32..32 from scan48_p0..p3.jsonl (overlaps at k = -16, 0, 16 compared bit for bit
across processes), the band that holds all its sign changes, and the M 32 same-path control from scan32.jsonl. Usage: python3 scan625.py"""
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
def load(name, key):
    f = os.path.join(here, name)
    if not os.path.exists(f) or os.path.getsize(f) == 0: return None
    r = json.loads(open(f).readline())
    return r[key]["scan"] if key == "M48" else r["scan"]
ctrl = load("scan32.jsonl", "base")
ranges = {"p0": (-32, -16), "p1": (-16, 0), "p2": (0, 16), "p3": (16, 32)}
m48 = {p: load(f"scan48_{p}.jsonl", "M48") for p in ranges}
ok = True
if ctrl is None: print("M 32 control: not finished"); ok = False
else:
    s = [(int(k), lam, sg, ld) for k, lam, sg, ld in ctrl]
    ch = [(s[j][0], s[j + 1][0]) for j in range(len(s) - 1) if s[j][2] != s[j + 1][2]]
    print(f"M 32 control (centre 2.045529761477775, k = {s[0][0]}..{s[-1][0]}): signs " + "".join("+" if x[2] > 0 else "-" for x in s) + f"; sign changes {len(ch)} between k pairs {ch}")
if any(v is None for v in m48.values()):
    print("M 48 scans finished:", [p for p, v in m48.items() if v is not None]); ok = False
if not ok: sys.exit(2)
byk = {}
for p, recs in m48.items():
    k0, k1 = ranges[p]
    assert [int(r[0]) for r in recs] == list(range(k0, k1 + 1)), (p, [r[0] for r in recs])
    for k, lam, sg, ld in recs:
        byk.setdefault(int(k), []).append((p, lam, sg, ld))
bad = []
for k in (-16, 0, 16):
    v = byk[k]; assert len(v) == 2
    same = v[0][1:] == v[1][1:]
    print(f"overlap k = {k:+d}: {v[0][0]} and {v[1][0]}: lambda, sign, ln|det| {'bit for bit equal' if same else 'DIFFERENT'} ({int(v[0][2]):+d}, {v[0][3]!r} against {int(v[1][2]):+d}, {v[1][3]!r})")
    if not same: bad.append(k)
grid = [(k, byk[k][0][1], byk[k][0][2], byk[k][0][3]) for k in range(-32, 33)]
print("\n| k | lambda | sign | ln abs det |\n|---|---|---|---|")
for k, lam, sg, ld in grid: print(f"| {k:+d} | {lam!r} | {int(sg):+d} | {ld:.9f} |")
chg = [(grid[j][0], grid[j + 1][0]) for j in range(64) if grid[j][2] != grid[j + 1][2]]
print("\nsigns from k=-32: " + "".join("+" if g[2] > 0 else "-" for g in grid))
print(f"sign changes {len(chg)} between k pairs {chg}")
if chg:
    lo, hi = chg[0][0], chg[-1][1]
    print(f"band holding all sign changes: between k={chg[0][0]}..{chg[0][1]} and k={chg[-1][0]}..{chg[-1][1]}: at most {(hi - lo)*1e-14:.2e} and at least {(chg[-1][0] - chg[0][1])*1e-14:.2e} wide")
print("overlaps bit for bit equal" if not bad else f"OVERLAPS DIFFER at k = {bad}")
