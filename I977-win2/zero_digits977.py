"""#977: the zero and error estimate of m7_outer.py --local with full digits (the arithmetic of its local(), copied), checked against
the numbers m7_outer printed in the same file (A, w/w_inf to 6 decimals, the estimate to 2 digits); exit 1 when they disagree.

    python zero_digits977.py logs/m7_outer_win2_TAG.txt [--json]     (run_job976 / combine977 output files)
"""
import json, os, re, sys
import numpy as np
sys.path.insert(0, os.environ.get("RUN_SRC", "D:/choptuik-i962/solver/inner_stokes"))
import m7_outer

path = sys.argv[1]
txt = open(path, encoding="utf-8").read()
cmd = [l for l in txt.splitlines() if l.startswith("$ ")][0][2:].split()
args = cmd[cmd.index("--local") + 1:]
k = args.index("--")
cen = [m7_outer.point(f, True) for f in args[:k]]
offs = [m7_outer.point(f, True) for f in args[k + 1:]]
good = [c for c in cen if c[3] < 1e-6]
if not good or any(o[3] >= 1e-6 for o in offs):
    sys.exit("m7_outer's refusal: not enough solves with |r_3| < 1e-6")
p0 = good[0][1]; R = np.array([c[2] for c in good]); r0 = R.mean(axis=0)
noise = 0.5 * float(np.ptp(R, axis=0).max()) if len(good) > 1 else float("nan")
(_, pa, ra, _), (_, pw, rw, _) = offs
J = np.column_stack([(ra - r0) / (pa[0] - p0[0]), (rw - r0) / (pw[1] - p0[1])])
sv = np.linalg.svd(J, compute_uv=False)
step = -np.linalg.solve(J, r0)
z = p0 + step
hmin = min(abs(pa[0] - p0[0]), abs(pw[1] - p0[1]))
dz_noise = noise / sv[-1]; dz_J = np.linalg.norm(step) * 2 * noise / (sv[-1] * hmin)
est = dz_noise + dz_J
m = re.search(r"zero: A ([0-9.]+), w/w_inf ([0-9.]+).*?error estimate ([0-9.]+e[+-]\d+)", txt)
ok = (m is not None and abs(float(m.group(1)) - z[0]) < 6e-7 and abs(float(m.group(2)) - z[1]) < 6e-7
      and abs(float(m.group(3)) / est - 1) < 0.06)
res = {"file": os.path.basename(path), "n_centre_good": len(good), "A": z[0], "w": z[1], "estimate": est, "noise_part": dz_noise,
       "J_part": dz_J, "centre_noise": noise, "sv": sv.tolist(), "matches_m7_outer_print": bool(ok)}
if "--json" in sys.argv:
    print(json.dumps(res))
else:
    print(f"{res['file']}: {len(good)} centre solves, zero A {z[0]:.9f}, w/w_inf {z[1]:.9f}, estimate {est:.3e} "
          f"({dz_noise:.2e} noise, {dz_J:.2e} J), centre noise {noise:.4f}; matches m7_outer's print: {ok}")
sys.exit(0 if ok else 1)
