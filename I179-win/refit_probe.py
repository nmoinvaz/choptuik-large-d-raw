import sys, os, json
import numpy as np
sys.path.insert(0, os.path.join(r"C:\Users\nathan\Source\choptuik-i179", "solver"))
os.chdir(os.path.join(r"C:\Users\nathan\Source\choptuik-i179", "solver", "data"))
import scipy, formula_all
r = formula_all.refit_distance()
tag = sys.argv[1]
def conv(x):
    return x.tolist() if hasattr(x, "tolist") else x
out = {k: conv(v) for k, v in r.items()}
out["_env"] = [sys.version.split()[0], np.__version__, scipy.__version__]
json.dump(out, open(sys.argv[2], "w"), indent=0, default=str)
print(tag, "keys", list(r.keys()))
