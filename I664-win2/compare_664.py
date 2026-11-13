#!/usr/bin/env python3
"""#664: one attempt's pair of runs against #603. usage: python compare_664.py TAG BASE_D TARGET_FILE   e.g.  compare_664.py 238.54 238.5375 anm_pin3_D239.5141.npz
For the refused attempt of #603 at the base D (the first attempt after the step header 'step N: D <BASE_D>'): own's attempt lines (the #666 trial lines removed, seconds and tol masked, the numbers of the
'on k:' lines rounded to two significant digits because newton_od now prints |dz| to three) against #603's chain.log lines; natural's attempt (trial lines, per-solve max|F|, result); and, where natural
converged at that a, its saved state's D_str and Delta (the eight parts summed exactly) against #603's state at the same D (TARGET_FILE in I603-win2/chain/). Prints; exit 0."""
import json, os, re, sys
import numpy as np
from mpmath import mp, mpf
mp.dps = 60
RAW = "D:/choptuik-large-d-raw/"
tag, base, target = sys.argv[1:4]


def _r2(m):
    return "%.1e" % float(m.group(0))


def mask(l):
    l = re.sub(r"\b\d+(\.\d+)? s\b", "<T> s", re.sub(r"tol [0-9.e+-]+", "tol <X>", l))
    if re.match(r"^\s+on \d+:", l):
        l = re.sub(r"\d\.\d+e[+-]\d+", _r2, l)
    return l


def attempt(lines, step_pat):
    s = [k for k, l in enumerate(lines) if re.match(step_pat, l)][0] if step_pat else 0
    i = [k for k, l in enumerate(lines) if k > s and re.match(r"^    a [0-9.]+: re-seeded", l)][0]
    j = [k for k, l in enumerate(lines) if k >= i and re.match(r"^    a [0-9.]+ -> D ", l)][0]
    return i, j


c = open(RAW + "I603-win2/chain.log", encoding="utf-8").read().splitlines()
ci, cj = attempt(c, r"^step \d+: D " + re.escape(base[:7]))
print(f"#603 chain.log lines {ci + 1} to {cj + 1}: {c[ci].strip()[:60]} ... {c[cj].strip()[:80]}")
o = open(RAW + f"I664-win2/{tag}_own.log", encoding="utf-8").read().splitlines()
oi, oj = attempt(o, None)
ob = [l for l in o[oi:oj + 1] if " trial lam " not in l]
cb = c[ci:cj + 1]
same = sum(mask(x) == mask(y) for x, y in zip(cb, ob))
print(f"own {tag}_own.log lines {oi + 1} to {oj + 1}: {len(ob)} lines without trial lines against {len(cb)}; identical with seconds, tol and digits masked: {same} of {len(cb)}")
for x, y in zip(cb, ob):
    if mask(x) != mask(y):
        print("   DIFF 603:", x[:200]); print("        own:", y[:200])
print("own result:", o[oj].strip()[:200])
n = open(RAW + f"I664-win2/{tag}_natural.log", encoding="utf-8").read().splitlines()
ni, nj = attempt(n, None)
print(f"natural {tag}_natural.log lines {ni + 1} to {nj + 1}:")
for l in n[ni:nj + 1]:
    print("   ", l[:215])
blk = "\n".join(n[ni:nj + 1])
conv = "not converged" not in blk and "no trial" not in blk
print("natural result:", n[nj].strip()[:215])
print("natural", "CONVERGED at this a" if conv else "REFUSED at this a")
if conv:
    def info(p):
        z = np.load(p); m = json.loads(str(z["meta"]))
        d = sum((mpf(float(z[k][-1])) for k in ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7") if k in z.files), mpf(0))
        return d, m.get("D_str"), z
    nat = [f for f in os.listdir(RAW + f"I664-win2/{tag}_natural") if f.startswith("anm_pin3_") and f.endswith(".npz")]
    if target not in nat:
        print("natural state", target, "not found; saved:", nat)
    else:
        dn, sn, zn = info(RAW + f"I664-win2/{tag}_natural/" + target)
        d3, s3, z3 = info(RAW + "I603-win2/chain/" + target)
        print("D_str natural:", sn, "| #603:", s3, "| equal:", sn == s3)
        print("Delta natural:", mp.nstr(dn, 50)); print("Delta #603   :", mp.nstr(d3, 50))
        print("difference:", mp.nstr(dn - d3, 6), "| within 1e-40:", abs(dn - d3) <= mpf("1e-40"), "| zh max|diff|", float(np.max(np.abs(zn["zh"] - z3["zh"]))), "zl", float(np.max(np.abs(zn["zl"] - z3["zl"]))))
