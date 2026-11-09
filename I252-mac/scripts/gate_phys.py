"""Gate of a D's circles (criterion 4 of ../README.md): the last lambda_phys circle in CIRCLES.jsonl must wind +1 with
every step below pi/4, 0 verification mismatches and its zero within 1e-5 of LAM_PHYS. Exit 0 on pass, 1 on fail.

    python gate_phys.py CIRCLES.jsonl LAM_PHYS
"""
import json
import math
import sys

path, lam = sys.argv[1], float(sys.argv[2])
recs = [json.loads(l) for l in open(path)]
r = [x for x in recs if abs(x["center"][0] - lam) < 1e-9 and x["center"][1] == 0][-1]
z = complex(*r["zeros"][0]) if r.get("zeros") else None
ok = (abs(r["winding"] - 1) < 1e-6 and r["max_step"] < math.pi / 4 and r["verify_mismatch"] == 0 and z is not None
      and abs(z - lam) < 1e-5)
print(f"lambda_phys circle: winding {r['winding']:+.6f}, max step {r['max_step']:.3f}, mismatches {r['verify_mismatch']}, "
      f"zero {z}, |zero - lam_phys| {abs(z - lam) if z is not None else float('nan'):.1e} -> {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
