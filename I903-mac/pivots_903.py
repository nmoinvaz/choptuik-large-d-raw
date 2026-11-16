"""#903 Mac pilot, after q250's failure: the smallest octo-double LU pivot of the pinned system at q130's base (ks 130,
its stored plan) and of the ks 250 system on a new plan (1e-32) at the same point, the Jacobian q250 factored first.
Uses hp/adjoint_split.py's State, system and adjoint (main 663e3b2d). Run from hp/ with the #523 build on PYTHONPATH."""
import math
import sys
import mpmath as mp
import adjoint_split as A

base = sys.argv[1]
mp.mp.dps = A.DPS
st = A.State("", base, 8)
out = {}
for name, kw in (("ks130 stored plan", {}), ("ks250 new plan", dict(ks=250, plan=1e-32))):
    sn, so, segs = st.system(**kw)
    F = A.tomp(A.resid(so, st.z8))
    r = A.adjoint(st, sn, so)
    step = r["step"]
    out[name] = r["pmin"]
    print(f"{name}: plan {sum(len(s) - 1 for s in segs)} steps, max|F| {float(max(abs(x) for x in F)):.3e}, pivots "
          f"{r['pmin']:.4e}..{r['pmax']:.4e}, |psi| {float(mp.sqrt(mp.fdot(r['psi'], r['psi']))):.3e}, Newton step "
          f"max|dz| {float(max(abs(x) for x in step)):.3e}, its Delta {float(step[-1]):+.4e} (LU {r['t_lu']} s)", flush=True)
p130, p250 = out["ks130 stored plan"], out["ks250 new plan"]
print(f"ln(p250/p130) at q130's point: {math.log(p250 / p130):+.3f} (p130 {p130:.4e}, p250 {p250:.4e})", flush=True)
