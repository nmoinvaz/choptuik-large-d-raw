"""#903 grip: the runs of 2026-11-17 10:49-13:17 UTC (k142 D 239.1312 and 244.1312) against their reruns.

From 07:02 to about 14:40 UTC that day site2's hpkernel lacked __init__.py, so a run started then loaded venv-314's
Nov 8 kernel (multidouble 4.0.0) instead of main 3c35f0c's (the coordinator, #903). The first runs are in old_kernel/,
the reruns (run.sh's guard: hpkernel from site2) in this folder. For each near_null JSON pair it prints the LU pivot
floor, the grip g (2-norm), sigma_1..6 and the Delta share of each, the largest relative difference over these, and
whether the pair is equal bit for bit in them; then each base's L = ln g(200) - ln g(142) in both.

Check (can fail): every rerun JSON exists and passed, and the rerun's L agrees with the first run's to 0.05 (the bar of
lift.py's control). A larger difference means the first runs' kernel changed the reading, and the reruns replace it.
Control --mutate=scale multiplies the first runs' g at order 200 by e^0.1, which must fail.

Run: python3 kernel_cmp.py FOLDER [--mutate=scale]. Exit 1 when the check fails.
"""
import json
import math
import os
import sys

d0 = sys.argv[1]
mut = "--mutate=scale" in sys.argv
ok = True


def nums(r):
    v = r["vectors"]
    return [r["pivots"][0], r["grip"]["two"]] + [x["sigma"] for x in v] + [x["delta"] for x in v]


for D in ("239.1312", "244.1312"):
    L = {}
    for K in (142, 200):
        n = f"nn_k142_D{D}_ks{K}.json"
        po, pn = os.path.join(d0, "old_kernel", n), os.path.join(d0, n)
        if not os.path.exists(pn):
            print(f"  {n}: no rerun")
            ok = False
            continue
        a, b = json.load(open(po)), json.load(open(pn))
        if mut and K == 200:
            a["grip"]["two"] *= math.exp(0.1)
        ok &= bool(b.get("passed"))
        x, y = nums(a), nums(b)
        rel = max(abs(p - q) / max(abs(p), abs(q), 1e-300) for p, q in zip(x, y))
        print(f"  {n}: g {a['grip']['two']:.6e} -> {b['grip']['two']:.6e}; sigma_1 {a['vectors'][0]['sigma']:.4e} -> "
              f"{b['vectors'][0]['sigma']:.4e}; pivot floor {a['pivots'][0]:.3e} -> {b['pivots'][0]:.3e}; largest "
              f"relative difference {rel:.2e}; {'equal bit for bit' if x == y else 'not equal'}; rerun passed "
              f"{b.get('passed')}")
        L.setdefault("old", {})[K] = math.log(a["grip"]["two"])
        L.setdefault("new", {})[K] = math.log(b["grip"]["two"])
    if all(len(L.get(k, {})) == 2 for k in ("old", "new")):
        lo, ln_ = L["old"][200] - L["old"][142], L["new"][200] - L["new"][142]
        good = abs(lo - ln_) < 0.05
        ok &= good
        print(f"  k142 D {D}: L first run {lo:+.4f}, rerun {ln_:+.4f}, difference {ln_ - lo:+.2e}: "
              f"{'agree' if good else 'DIFFER'}")
print(f"check{' (--mutate=scale)' if mut else ''}: {'pass' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
