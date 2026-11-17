"""#903 ladder at D 225.13: one rung's numbers from its saved base on its own system (its ks and stored plan): max|F|,
the smallest octo-double LU pivot, |psi|, ln(p_K / p_130) and Delta_K - Delta_130 (eight parts summed exactly).
hp/adjoint_split.py's State, system and adjoint (main 663e3b2d). Run from hp/ with the #523 build on PYTHONPATH.
    python3 rung_info.py BASE_K BASE_130 P130 OUT.jsonl"""
import json
import math
import sys
import mpmath as mp
import adjoint_split as A

bk, b130, p130, outp = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
mp.mp.dps = A.DPS
st = A.State("", bk, 8)
sn, so, segs = st.system()
F = A.tomp(A.resid(so, st.z8))
r = A.adjoint(st, sn, so)
d130 = A.tomp(A.State("", b130, 8).z8)[-1]
dK = A.tomp(st.z8)[-1]
rec = dict(ks=st.ks, base=bk, plan_steps=sum(len(s) - 1 for s in segs), F=float(max(abs(x) for x in F)), pmin=r["pmin"],
           pmax=r["pmax"], psi=float(mp.sqrt(mp.fdot(r["psi"], r["psi"]))), ln_p_over_p130=math.log(r["pmin"] / p130),
           dDelta=float(dK - d130), Delta=mp.nstr(dK, 40))
with open(outp, "a") as f:
    f.write(json.dumps(rec) + "\n")
print(f"rung ks {st.ks}: plan {rec['plan_steps']} steps, max|F| {rec['F']:.2e}, p_min {rec['pmin']:.4e}, |psi| {rec['psi']:.3e}, "
      f"ln(p/p130) {rec['ln_p_over_p130']:+.3f}, Delta - Delta_130 {rec['dDelta']:+.6e}", flush=True)
