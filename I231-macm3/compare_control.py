"""I231-macm3: the rebuild control. The evals cache of the rerun of #237's (c) (control_D55_M32/data) against I237-macm3/D55_M32/data, bit for bit, line by line.
    python3 compare_control.py
Exit 0: every line equal (re, im, lnabs, arg, pmin, pmax; not the timings) and the control (one digit of one lnabs changed) differs. Exit 1: the caches differ. Exit 2: the control did not differ."""
import json, sys

def load(p):
    return [json.loads(l) for l in open(p)]
a = load("control_D55_M32/data/modecount_D55.0351_M32_kf23_evals.jsonl")
b = load("../I237-macm3/D55_M32/data/modecount_D55.0351_M32_kf23_evals.jsonl")
K = ("re", "im", "lnabs", "arg", "pmin", "pmax")
print(f"lines: control {len(a)}, I237 {len(b)}")
bad = []
if len(a) == len(b):
    for i, (x, y) in enumerate(zip(a, b)):
        d = [k for k in K if x[k] != y[k]]
        if d:
            bad.append((i, d))
print("lines differing:", len(bad), bad[:5])
code = 0 if len(a) == len(b) and not bad else 1
# control: change one digit of one lnabs of the control's copy and compare again
import copy
c = copy.deepcopy(a)
v = repr(c[0]["lnabs"])
c[0]["lnabs"] = float(v[:-1] + ("1" if v[-1] != "1" else "2"))
ctl = any(c[i][k] != b[i][k] for i in range(min(len(c), len(b))) for k in K)
print("control (last digit of lnabs of line 0 changed) differs:", ctl)
if code == 0 and not ctl:
    code = 2
print("exit", code)
sys.exit(code)
