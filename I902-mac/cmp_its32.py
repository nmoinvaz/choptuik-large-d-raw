"""I902-mac: the rerun of D 249.01 at ks 160 with --its=32 against the run with --its=16 (C1's failure).

Passes when the rerun's near_null check passed, its sigma_1 converged below 1e-3, and |ln g(32) - ln g(16)| < 1e-3.
Also prints whether the grip, the pivots and the pinned step's Delta are equal, and sigma_1-4 of both runs.
Run: python3 cmp_its32.py FOLDER [--mutate=self]. The control --mutate=self reads the --its=16 run as the rerun, and
must FAIL (its check failed, sigma_1 at 1.35e-3). Exits 1 when it fails.
"""
import json
import math
import os
import sys

d = sys.argv[1]
a = json.load(open(os.path.join(d, "nn_D249_ks160.json")))
b = json.load(open(os.path.join(d, "nn_D249_ks160_its32.json")))
if "--mutate=self" in sys.argv:
    b = a
    print("cmp_its32: --mutate=self, the --its=16 run read as the rerun")
la, lb = math.log(a["grip"]["two"]), math.log(b["grip"]["two"])
print(f"cmp_its32: ln g its 16 {la:+.6f}, its 32 {lb:+.6f}, difference {lb - la:+.3e}")
print(f"  grip equal {a['grip'] == b['grip']}; pivots equal {a['pivots'] == b['pivots']}; pinned step's Delta equal "
      f"{a['step_pinned']['delta'] == b['step_pinned']['delta']} ({b['step_pinned']['delta']:+.6e})")
for i, (x, y) in enumerate(zip(a["vectors"][:4], b["vectors"][:4])):
    print(f"  sigma_{i + 1} its 16 {x['sigma']:.6e} (conv {x['conv']:.2e}, Delta share {x['delta']:.2e}), its 32 "
          f"{y['sigma']:.6e} (conv {y['conv']:.2e}, Delta share {y['delta']:.2e}), ln ratio {math.log(y['sigma'] / x['sigma']):+.2e}")
checks = [("run", b["passed"], f"the rerun's near_null check passed: {b['passed']}"),
          ("conv", b["vectors"][0]["conv"] < 1e-3, f"sigma_1 converged to {b['vectors'][0]['conv']:.2e} (< 1e-3)"),
          ("grip", abs(lb - la) < 1e-3, f"|ln g(32) - ln g(16)| {abs(lb - la):.2e} (< 1e-3)")]
for name, ok, what in checks:
    print(f"  check {name}: {what}: {'pass' if ok else 'FAIL'}")
ok = all(c[1] for c in checks)
print(f"cmp_its32: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
