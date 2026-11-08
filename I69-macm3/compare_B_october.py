"""Round B against October, point by point and box by box (I69-macm3). Usage: python3 compare_B_october.py D16.7600_M32 [D8.2500_M32 ...]

Reads october_logs/modecount_<t>.log (Windows line endings), data_A/..._evals.jsonl (the October cache, copied) and data_B/..._evals.jsonl (this
build, evaluated fresh). Prints the per-point difference of ln|det| and arg at the points both caches hold, and whether the 8 box lines of the logs
are identical apart from line endings.
"""
import json
import math
import statistics
import sys


def load(p):
    return {(r["re"], r["im"]): r for r in map(json.loads, open(p))}


def boxes(p):
    return [l.rstrip("\r\n") for l in open(p, newline="") if l.startswith("  box ")]


for t in sys.argv[1:]:
    a, b = load(f"data_A/modecount_{t}_evals.jsonl"), load(f"data_B/modecount_{t}_evals.jsonl")
    keys = [k for k in b if k in a]
    print(f"===== {t}: October cache {len(a)} points, fresh {len(b)}, shared {len(keys)}")
    dl = [b[k]["lnabs"] - a[k]["lnabs"] for k in keys]
    da = [(b[k]["arg"] - a[k]["arg"] + math.pi) % (2 * math.pi) - math.pi for k in keys]
    rel = [abs(b[k]["lnabs"] - a[k]["lnabs"]) / max(1e-300, abs(a[k]["lnabs"])) for k in keys]
    print(f"  ln|det| fresh - October: largest |d| {max(map(abs, dl)):.3e}, median |d| {statistics.median(map(abs, dl)):.3e}, "
          f"signed mean {statistics.mean(dl):+.3e}, largest relative {max(rel):.2e}")
    print(f"  arg fresh - October (wrapped): largest |d| {max(map(abs, da)):.3e}, median |d| {statistics.median(map(abs, da)):.3e}")
    pm = [abs(b[k]["pmin"] - a[k]["pmin"]) / a[k]["pmin"] for k in keys]
    print(f"  pivot minimum relative difference: largest {max(pm):.2e}")
    ob, nb = boxes(f"october_logs/modecount_{t}.log"), boxes(f"data_B/modecount_{t}.log")
    same = [x == y for x, y in zip(ob, nb)]
    print(f"  box lines October {len(ob)}, fresh {len(nb)}, identical {sum(same)} of {len(same)} (line endings ignored)")
    for x, y, s in zip(ob, nb, same):
        if not s:
            i = next((k for k in range(min(len(x), len(y))) if x[k] != y[k]), min(len(x), len(y)))
            print(f"   differs: {x[:10]!r} at char {i}: October ...{x[max(0, i - 20):i + 60]!r}\n   {' ' * 18}fresh   ...{y[max(0, i - 20):i + 60]!r}")
