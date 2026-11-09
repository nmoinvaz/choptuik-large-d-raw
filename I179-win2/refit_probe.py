"""I179-win2: formula_all.refit_distance() on this stack, the three numbers of check_numbers.py's formula_refit item
(limits 1e-9, 1e-8, and a window of 0.5e-7 to 2e-7). Run from anywhere: python refit_probe.py OUT.json"""
import sys, os, json
import numpy as np
ROOT = r"D:\choptuik-large-d"
sys.path.insert(0, os.path.join(ROOT, "solver"))
os.chdir(os.path.join(ROOT, "solver", "data"))
import scipy, formula_all
r = formula_all.refit_distance()
conv = lambda x: x.tolist() if hasattr(x, "tolist") else x
out = {k: conv(v) for k, v in r.items()}
out["_env"] = [sys.version.split()[0], np.__version__, scipy.__version__]
json.dump(out, open(OUT, "w"), indent=0, default=str)
for k in ("delta_fit_range", "gamma_fit_range", "delta_80"):
    print(k, r.get(k))
print("env", out["_env"])
