#!/usr/bin/env python3
"""#1111 stage 1: the verdicts of bars 1-4 from the three runs' JSONL and logs (run from this folder)."""
import json, re, sys
runs = {"k35": "ddet_k35", "all": "ddet_all", "hionly": "ddet_k35_hionly"}
R = {}
for k, f in runs.items():
    r = json.loads(open(f + ".jsonl").readline())
    log = open(f + ".log").read()
    build = float(re.search(r"dd M built in (\d+) s", log).group(1))
    ln = [v["ln"] for v in r["dd"]]
    sg = [v["sign"] for v in r["dd"]]
    lus = [v["sec"] for v in r["dd"]]
    R[k] = dict(steps=r["steps"], signs=sg, ln=ln[0], spread=max(ln) - min(ln), f64_sign=r["f64_sign"], f64_ln=r["f64_ln"],
                build=build, lu=sum(lus), total=build + sum(lus), agree=len(set(sg)) == 1)
print("run     steps  signs(5)          ln|det| dd (variant 0)  spread max-min   float64 sign, ln|det|        M build s  5 LU s  total s")
for k, v in R.items():
    print(f"{k:7s} {v['steps']}  {''.join('+' if s > 0 else '-' for s in v['signs'])}  {v['ln']:.10f}  {v['spread']:.2e}  "
          f"{'+' if v['f64_sign'] > 0 else '-'} {v['f64_ln']:.10f}  {v['build']:.0f}  {v['lu']:.1f}  {v['total']:.1f}")
b1 = all(v["steps"] == 5124 and v["agree"] for v in R.values())
d2 = abs(R["hionly"]["ln"] - R["k35"]["ln"])
b2 = d2 > R["hionly"]["spread"] and d2 > R["k35"]["spread"]
d3 = abs(R["k35"]["ln"] - R["all"]["ln"])
b3 = d3 <= 0.1
b4 = abs(d3 - 0.81) <= 0.081
print(f"bar 1 (5124 steps; five variants agree in sign, each run): {'PASS' if b1 else 'FAIL'}")
print(f"bar 2 (hionly control: |hionly - k35| {d2:.6f} > spreads {R['hionly']['spread']:.2e} (hionly), {R['k35']['spread']:.2e} (k35); signs "
      f"{R['k35']['signs'][0]:+.0f} -> {R['hionly']['signs'][0]:+.0f}): {'PASS' if b2 else 'FAIL'}")
print(f"bar 3 (|k35 - all| {d3:.12f} <= 0.1): {'PASS' if b3 else 'FAIL'}")
print(f"bar 4 (|diff - 0.81| {abs(d3 - 0.81):.6f} = {100 * abs(d3 - 0.81) / 0.81:.3f}% of 0.81, bar 10%): {'PASS' if b4 else 'FAIL'}")
print(f"float64 minus dd: k35 {R['k35']['f64_ln'] - R['k35']['ln']:+.6f}, all {R['all']['f64_ln'] - R['all']['ln']:+.6f}; "
      f"float64 difference k35 - all {R['k35']['f64_ln'] - R['all']['f64_ln']:+.6f}")
print(f"float64 sign vs dd sign: k35 {R['k35']['f64_sign']:+.0f} vs {R['k35']['signs'][0]:+.0f}, all {R['all']['f64_sign']:+.0f} vs {R['all']['signs'][0]:+.0f}")
sys.exit(0 if (b1 and b2) else 1)
