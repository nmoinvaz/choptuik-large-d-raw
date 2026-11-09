#!/usr/bin/env python3
"""I230-mac: recompute two of #212's cached determinants on this machine (the setup the circles use) and compare.

    python3 repro_check.py HP_DIR I212_EVALS.jsonl OUT.jsonl

HP_DIR is the worktree's hp/ (with hp/data/modecount_state_D61.0264_M48_kf23.npz, byte-identical to
I212-macm3/hp_data_after/). Pass criterion, fixed before the run: ln|det M| and arg det M at both points agree with
the I212 cache to 1e-8 (macm3 and this Mac are both arm64 NEON builds; the double-double LU rounds at about 1e-30
relative, so a difference above 1e-8 means a different matrix, state or build). Exit 1 otherwise.
"""
import json
import sys
import time

hp, evals, out = sys.argv[1:4]
sys.path.insert(0, hp)
from modecount_common import setup  # noqa: E402

cache = {}
for line in open(evals):
    e = json.loads(line)
    cache[(e["re"], e["im"])] = e
pts = [(3.0, 0.0)]
# one complex point of the edge Re = a2 (V2), the first off the real axis in the cache
pts.append(min((k for k in cache if abs(k[0] - 2.643532530673195) < 1e-12 and k[1] > 0), key=lambda k: k[1]))
st = setup(f"{hp}/data/seeds/local/up23_D61.0264.npz", M=48, kf=23, fmax=1e-15)
ok = True
with open(out, "a") as fo:
    for re_, im_ in pts:
        t = time.time()
        la, arg, pmin, pmax = st.det(re_, im_)
        c = cache[(re_, im_)]
        d = max(abs(la - c["lnabs"]), abs(arg - c["arg"]))
        ok &= d <= 1e-8
        rec = dict(re=re_, im=im_, lnabs=la, arg=arg, lnabs_I212=c["lnabs"], arg_I212=c["arg"], diff=d, F=st.F,
                   sec=round(time.time() - t, 1), time=time.strftime("%Y-%m-%d %H:%M:%S"))
        fo.write(json.dumps(rec) + "\n")
        print(f"lam {re_} {im_:+}i: ln|det| {la:.12f} (I212 {c['lnabs']:.12f}), arg {arg:.12f} (I212 {c['arg']:.12f}), "
              f"difference {d:.1e}, {rec['sec']} s; setup |F| {st.F:.1e}", flush=True)
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
