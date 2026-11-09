"""Determinant check of a mode-count state before a count (#252, criteria in ../README.md).

    python det_check.py HP_DIR STATE.npz KF LAM_PHYS OUT.json [--dl=0.015] [--threads=1]

setup (modecount_common, fmax 1e-15) on the state at its own M, then det M at lam_phys - dl and lam_phys + dl with
hpkernel's real LU (Solver.mode_det) and modecount_cx's complex LU. Passes when det M changes sign across lam_phys in
both LUs, the two signs agree at each point, and |ln|det|_hp - ln|det|_cx| <= 1e-4 at both. Exit 0 on pass, 1 on
fail. Its control is a state where det M is known to be unusable (#141's node-0.85 state), which must fail.
"""
import json
import math
import sys
import time

hp_dir, path, kf, lam, out = sys.argv[1:6]
opts = dict(a[2:].split("=", 1) for a in sys.argv[6:] if a.startswith("--"))
sys.path.insert(0, hp_dir)
import modecount_common as mc  # noqa: E402

kf = None if kf == "none" else int(kf)
lam = float(lam)
dl = float(opts.get("dl", 0.015))
TOL = 1e-4
t0 = time.time()
st = mc.setup(path, M=None, kf=kf, fmax=1e-15, threads=int(opts.get("threads", 1)))
print(f"D {st.D} M {st.M} K {st.K} nodes {st.meta['nodes']} ks {st.ks} kf {st.kf} |F| {st.F:.1e} "
      f"lam_g {st.lam_g:.10f} ({time.time() - t0:.0f} s)", flush=True)
rows = []
for x in (lam - dl, lam + dl):
    t = time.time()
    sg, la_hp, pmin_hp, pmax_hp = st.det_real(x)
    t_hp = time.time() - t
    t = time.time()
    la_cx, arg, pmin_cx, pmax_cx = st.det(x, 0.0)
    t_cx = time.time() - t
    sg_cx = 1 if abs(arg) < 1.0 else -1
    rows.append(dict(lam=x, sign_hp=int(sg), lnabs_hp=la_hp, sign_cx=sg_cx, arg_cx=arg, lnabs_cx=la_cx,
                     diff=abs(la_hp - la_cx), pmin_hp=pmin_hp, pmax_hp=pmax_hp, pmin_cx=pmin_cx, pmax_cx=pmax_cx,
                     sec_hp=round(t_hp, 1), sec_cx=round(t_cx, 1)))
    r = rows[-1]
    print(f"  lam {x:.6f}: hp sign {r['sign_hp']:+d} ln|det| {la_hp:.10f} ({t_hp:.0f} s); cx arg {arg:+.3e} "
          f"ln|det| {la_cx:.10f} ({t_cx:.0f} s); |diff| {r['diff']:.2e}; pivots {pmin_cx:.2e} .. {pmax_cx:.2e}",
          flush=True)
a, b = rows
checks = dict(sign_change_hp=a["sign_hp"] != b["sign_hp"], sign_change_cx=a["sign_cx"] != b["sign_cx"],
              signs_agree=all(r["sign_hp"] == r["sign_cx"] for r in rows),
              lu_agree=all(r["diff"] <= TOL for r in rows) and all(math.isfinite(r["diff"]) for r in rows))
ok = all(checks.values())
rec = dict(state=path, D=st.D, M=st.M, kf=st.kf, nodes=st.meta["nodes"], ks=st.ks, F=st.F, lam_phys=lam, dl=dl,
           tol=TOL, rows=rows, checks=checks, passed=ok, seconds=round(time.time() - t0))
json.dump(rec, open(out, "w"), indent=1)
print(f"checks {checks} -> {'PASS' if ok else 'FAIL'}", flush=True)
sys.exit(0 if ok else 1)
