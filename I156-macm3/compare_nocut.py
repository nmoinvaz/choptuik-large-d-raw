"""Fresh no-cut M 48 determinants on October's own state against October's cache (I156-macm3).

    python3 compare_nocut.py [FRESH_CACHE]     (default hp_data_after/modecount_D30.0688_M48_evals.jsonl)

The October cache is october_inputs/modecount_D30.0688_M48_evals.jsonl (174 lines, none with CR). Thresholds fixed before the run (README): "a few ulp"
is largest |d ln|det|| <= 1e-12 and largest |d arg| <= 1e-10, an offset "persists" if |d ln|det|| >= 1e-3 at any shared point.
"""
import json
import math
import statistics
import sys

fresh_path = sys.argv[1] if len(sys.argv) > 1 else "hp_data_after/modecount_D30.0688_M48_evals.jsonl"
oct_ = {(r["re"], r["im"]): r for r in map(json.loads, open("october_inputs/modecount_D30.0688_M48_evals.jsonl"))}
new = {(r["re"], r["im"]): r for r in map(json.loads, open(fresh_path))}
keys = [k for k in new if k in oct_]
print(f"October cache {len(oct_)} points, fresh {len(new)}, shared {len(keys)}")
dl = [new[k]["lnabs"] - oct_[k]["lnabs"] for k in keys]
da = [(new[k]["arg"] - oct_[k]["arg"] + math.pi) % (2 * math.pi) - math.pi for k in keys]
dp = [new[k]["pmin"] / oct_[k]["pmin"] - 1 for k in keys]
print(f"ln|det|: largest |d| {max(map(abs, dl)):.3e}, median |d| {statistics.median(map(abs, dl)):.3e}, signed mean {statistics.mean(dl):+.3e}, identical {sum(1 for x in dl if x == 0)} of {len(dl)}")
print(f"arg: largest |d| {max(map(abs, da)):.3e}, median |d| {statistics.median(map(abs, da)):.3e}, identical {sum(1 for x in da if x == 0)} of {len(da)}")
print(f"pivot minimum: largest relative |d| {max(map(abs, dp)):.3e}")
a, b = max(map(abs, dl)), max(map(abs, da))
verdict = ("A FEW ULP: the offset is in the state" if a <= 1e-12 and b <= 1e-10 else
           "PERSISTS: the offset is in the evaluation" if a >= 1e-3 else "BETWEEN the two thresholds")
print("verdict by the fixed reading:", verdict)
print()
for k, x, y in sorted(((k, d, e) for k, d, e in zip(keys, dl, da)), key=lambda t: -abs(t[1]))[:10]:
    print(f"  ({k[0]:.5f}, {k[1]:.5f})  d ln|det| {x:+.3e}  d arg {y:+.3e}")
