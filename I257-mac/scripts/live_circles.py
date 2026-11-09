"""#257: a circle whose alias-rule replay needs determinants its cache lacks (recheck_circles.py), re-run with
hp/modecount_circle.circle (wip/i254, b40fa99) on the stored background it was counted on. Cached points are taken
from a copy of the circle's cache; new points are evaluated with modecount_common.build_pair on the stored state (the
layout of the state's meta, kf from the command line) and appended to the copy. No setup(): the state is used as
stored, so the background is the one the original circle used, and the #141 series gate (which setup would apply)
is only reported.

    python3 live_circles.py CODE_HP_DIR STATE.npz KF CACHE.jsonl OUTDIR RE,IM,R,N0 [...]

Control before any circle: two cached points (the first and the last cache lines) are re-evaluated live; their
ln|det| and arg must agree with the cache to 1e-4 (the two LU builds on different machines; #141 saw 1e-6 to 6e-5).
Exit 1 if the control fails. Records go to OUTDIR/live_circles.jsonl, the extended cache to OUTDIR/<cache name>.
"""
import json
import math
import os
import shutil
import sys
import time

sys.path.insert(0, sys.argv[1])
import numpy as np  # noqa: E402
import modecount_common as mc  # noqa: E402
import modecount_circle as C  # noqa: E402
from hpkernel.driver import load  # noqa: E402

state, kf, cache_src, outdir = sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
os.makedirs(outdir, exist_ok=True)
cache_path = os.path.join(outdir, os.path.basename(cache_src))
if not os.path.exists(cache_path):
    shutil.copy(cache_src, cache_path)
cache = {}
lines = [json.loads(x) for x in open(cache_path)]
for r in lines:
    cache[(r["re"], r["im"])] = r
zh, zl, meta = load(state)
M = meta["M"]
s, c = mc.build_pair(meta, zh, zl, M, kf)
zh, zl = np.ascontiguousarray(zh), np.ascontiguousarray(zl)
F = mc.resid(s, zh, zl)
tails = [mc.series_tail(s, zh, zl, meta, w) for w in (0, 1)]
print(f"{state}: D {meta['D']}, M {M}, kf {kf}, |F| {F:.1e}, series {mc.tails_text(tails)} "
      f"(#141 gate {'passes' if max(t['tail'] for t in tails) <= mc.SERIES_TAIL else 'FIRES'})", flush=True)
cf = open(cache_path, "a")
nlive = [0]


def live(re, im):
    t = time.time()
    la, arg, pmin, pmax = c.mode_det(zh, zl, float(re), float(im))
    return dict(re=re, im=im, lnabs=la, arg=arg, pmin=pmin, pmax=pmax, sec=round(time.time() - t, 2))


bad = 0
for r in (lines[0], lines[-1]):
    x = live(r["re"], r["im"])
    d_ln, d_arg = abs(x["lnabs"] - r["lnabs"]), abs(math.remainder(x["arg"] - r["arg"], 2 * math.pi))
    ok = d_ln < 1e-4 and d_arg < 1e-4
    bad += not ok
    print(f"  control at {r['re']:.6f} {r['im']:+.6f}i: ln|det| {x['lnabs']:.8f} (cache {r['lnabs']:.8f}, diff "
          f"{d_ln:.1e}), arg diff {d_arg:.1e}, {x['sec']} s -> {'ok' if ok else 'FAIL'}", flush=True)
if bad:
    sys.exit(1)


def det(lam):
    k = (float(lam.real), float(lam.imag))
    if k not in cache:
        r = live(*k)
        cache[k] = r
        cf.write(json.dumps(r) + "\n")
        cf.flush()
        nlive[0] += 1
    return cache[k]["lnabs"], cache[k]["arg"]


out = open(os.path.join(outdir, "live_circles.jsonl"), "a")
for spec in sys.argv[6:]:
    re, im, R, n0 = spec.split(",")
    n_before = nlive[0]
    t = time.time()
    rec = C.circle(det, complex(float(re), float(im)), float(R), math.pi / 4, int(n0))
    rec = dict(state=state, kf=kf, cache=cache_src, D=meta["D"], M=M, F=F, n0=int(n0), new_determinants=nlive[0] - n_before,
               seconds=round(time.time() - t), **rec)
    print(f"  circle |lam - ({float(re):.4f} {float(im):+.4f}i)| = {R}: winding {rec['winding']:+.6f}, {rec['points']} "
          f"points ({rec['new_determinants']} new determinants), max step {rec['max_step']:.3f}, mismatches "
          f"{rec['verify_mismatch']}, alias bisections {rec['alias_bisections']}, largest arc*scale "
          f"{rec['max_scale_h']:.2f}, resolved {rec['resolved']}, {rec['seconds']} s", flush=True)
    out.write(json.dumps(rec, default=str) + "\n")
    out.flush()
