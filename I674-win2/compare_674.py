#!/usr/bin/env python3
"""#674: one arm's first attempt at an attempt of #603 (the class A refusals). usage: python compare_674.py TAG ARM TARGET_FILE   e.g.  compare_674.py 244.637 A anm_pin3_D245.6366.npz
Prints the first attempt of <TAG>_arm<ARM>.log (from its 're-seeded' line to its 'a X -> D' line), flags converged or refused, and where converged compares the saved state at the attempt's target D
(TARGET_FILE in <TAG>_arm<ARM>/) with #603's state of the same name in I603-win2/chain/: D_str, Delta (the eight parts summed exactly) and zh, zl."""
import json, os, re, sys
import numpy as np
from mpmath import mp, mpf
mp.dps = 60
RAW = "D:/choptuik-large-d-raw/"
tag, arm, target = sys.argv[1:4]
lines = open(RAW + f"I674-win2/{tag}_arm{arm}.log", encoding="utf-8").read().splitlines()
i = [k for k, l in enumerate(lines) if re.match(r"^    a [0-9.]+: re-seeded", l)][0]
j = [k for k, l in enumerate(lines) if k >= i and re.match(r"^    a [0-9.]+ -> D ", l)][0]
print(f"{tag}_arm{arm}.log lines {i + 1} to {j + 1}:")
for l in lines[i:j + 1]:
    print("   ", l[:215])
blk = "\n".join(lines[i:j + 1])
conv = "not converged" not in blk and "no trial" not in blk and "stalled" not in blk
print("arm", arm, "CONVERGED at this a" if conv else "REFUSED at this a")
secs = re.search(r"moved [0-9.e+-]+, (\d+) s", lines[j])
if secs:
    print("attempt seconds:", secs.group(1))
if conv:
    def info(p):
        z = np.load(p); m = json.loads(str(z["meta"]))
        d = sum((mpf(float(z[k][-1])) for k in ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7") if k in z.files), mpf(0))
        return d, m.get("D_str"), z
    fol = RAW + f"I674-win2/{tag}_arm{arm}/"
    if not os.path.exists(fol + target):
        print("state", target, "not found; saved:", [f for f in os.listdir(fol) if f.startswith("anm_pin3_")])
    else:
        dn, sn, zn = info(fol + target)
        d3, s3, z3 = info(RAW + "I603-win2/chain/" + target)
        print("D_str arm:", sn, "| #603:", s3, "| equal:", sn == s3)
        print("Delta arm :", mp.nstr(dn, 50)); print("Delta #603:", mp.nstr(d3, 50))
        print("difference:", mp.nstr(dn - d3, 6), "| within 1e-40:", abs(dn - d3) <= mpf("1e-40"), "| zh max|diff|", float(np.max(np.abs(zn["zh"] - z3["zh"]))), "zl", float(np.max(np.abs(zn["zl"] - z3["zl"]))))
