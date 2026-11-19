"""#1012: analysis of the noise_r5.py outputs (logs/noise_r5_*.json): the spread of the corrected residual by row under nested-start perturbations at rel 1e-12 and 1e-10 (noise or response?),
the slope of the corrected r_5 in the level-5 unknowns from the x5-mode runs (control B and B'), the x5 resolution the noise corresponds to, and the comparison with the ends of the runs.

    python noise_analyze.py [--mutate=shuffle]       (from this folder; stdlib + numpy)
Checks (each can fail): control A (zero perturbation) has an exactly zero spread; the number of samples in each json equals its summary's n; at least 6 x5 samples respond above 10 x the nested-start
noise; the linear fit of the corrected r_5 on the level-5 offsets leaves a median residual below 30% of the response. --mutate=shuffle rolls the offsets against the responses (breaks their pairing):
it must fail the last check. (An earlier mutation, --mutate=swap, exchanged the two offset components of every sample, which only permutes the fitted matrix's columns and cannot fail: removed.)"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
L = os.path.join(HERE, "logs")
ld = lambda n: json.load(open(os.path.join(L, f"noise_r5_{n}.json")))
rows = ["r1 re", "r1 im", "r3 B", "r3 C", "r5 B", "r5 C", "r7 B", "r7 C", "r9 B", "r9 C"]
bad = 0
Z, N12, N10 = ld("zero"), ld("nested_1e-12"), ld("nested_1e-10")
X5_ = [ld(t) for t in ("x5_1e-12", "x5_1e-9", "x5_1e-8")]
for name, j in (("zero", Z), ("nested_1e-12", N12), ("nested_1e-10", N10), ("x5_1e-12", X5_[0]), ("x5_1e-9", X5_[1]), ("x5_1e-8", X5_[2])):
    if len(j["samples"]) != j["summary"]["n"]:
        print(f"CHECK FAILED: {name}: {len(j['samples'])} samples against n = {j['summary']['n']}"); bad = 1
if max(Z["summary"]["maxdev"]) != 0.0:
    print("CHECK FAILED: control A (zero perturbation) has a non-zero spread"); bad = 1
print("| row | nested 1e-12: std / max dev | nested 1e-10: std / max dev | ratio of std (1e-10 / 1e-12) |\n|---|---|---|---|")
for i, r in enumerate(rows):
    a, b = N12["summary"], N10["summary"]
    print(f"| {r} | {a['std'][i]:.2e} / {a['maxdev'][i]:.2e} | {b['std'][i]:.2e} / {b['maxdev'][i]:.2e} | {b['std'][i] / a['std'][i]:.2f} |")
n5a = np.hypot(N12["summary"]["std"][4], N12["summary"]["std"][5])
n5b = np.hypot(N10["summary"]["std"][4], N10["summary"]["std"][5])
n3 = np.hypot(N12["summary"]["std"][2], N12["summary"]["std"][3])
n1 = np.hypot(N12["summary"]["std"][0], N12["summary"]["std"][1])
print(f"\nnorm of the std over the two components: r5 {n5a:.2e} (1e-12), {n5b:.2e} (1e-10); r3 {n3:.2e}; r1 {n1:.2e}; r7 {np.hypot(*N12['summary']['std'][6:8]):.2e}; r9 {np.hypot(*N12['summary']['std'][8:10]):.2e}")
# slope of the corrected r5 in x5 from the x5-mode runs, v2 (written 12:08 UTC before the 1e-7 and 1e-6 data existed): the fit uses the samples whose response |dr| exceeds 10 x the nested-start
# noise norm (n5a); the CHECK needs the fit's median residual to be below 0.3 x |dr| over those samples; the swap mutation (the two dx components exchanged) must break it.
x50 = np.array(N12["summary"]["fixed_x"][4:6])
dx, dr, tag = [], [], []
X5 = []
for t in ("1e-12", "1e-9", "1e-8", "1e-7", "1e-6"):
    if os.path.exists(os.path.join(L, f"noise_r5_x5_{t}.json")) or t == "1e-12":
        X5.append((t, ld("x5_1e-12" if t == "1e-12" else f"x5_{t}")))
for t, j in X5:
    base = np.array(j["summary"]["base_r"][4:6])
    for sm in j["samples"]:
        d = np.array(sm["x"][4:6]) - x50
        dx.append(d); dr.append(np.array(sm["r"][4:6]) - base); tag.append(t)
dx, dr = np.array(dx), np.array(dr)
if "--mutate=shuffle" in sys.argv:
    dx = np.roll(dx, 3, axis=0)                      # the offsets no longer belong to their responses
mag = np.linalg.norm(dr, axis=1)
big = mag > 10 * n5a
print(f"x5-mode samples: {len(dr)} in the runs {[t for t, _ in X5]}; {int(big.sum())} with a response above 10 x the nested-start noise ({10 * n5a:.1e})")
if big.sum() < 6:
    print("CHECK FAILED: fewer than 6 x5 samples respond above 10 x the noise: the slope is not measured"); bad = 1
else:
    S, *_ = np.linalg.lstsq(dx[big], dr[big], rcond=None)        # dr = dx @ S
    S = S.T                                                       # dr_vec = S @ dx_vec
    sv = np.linalg.svd(S, compute_uv=False)
    pred = dx @ S.T
    rel = np.linalg.norm(dr - pred, axis=1) / np.maximum(mag, 1e-300)
    print(f"slope of the corrected r5 in (B5, C5) (S, r5 = S dx5): {S.tolist()}; singular values {sv[0]:.2e}, {sv[1]:.2e}; raw K block 5,5 max about 2.4e14")
    print(f"relative fit residual over the responding samples: median {np.median(rel[big]):.2f}, max {rel[big].max():.2f}")
    if not np.median(rel[big]) < 0.3:
        print("CHECK FAILED: the linear fit leaves a median residual of 30% or more of the response"); bad = 1
    res_x5 = [n5a / sv[0], n5a / sv[1]]
    print(f"x5 resolution the r5 noise corresponds to: sigma(r5) / singular value = {res_x5[0]:.2e} and {res_x5[1]:.2e} in (B5, C5) (relative to |x5| ~ 8.4e-3 and 1.5e-3: {res_x5[0] / 8.4e-3:.1e}, {res_x5[1] / 1.5e-3:.1e})")
sys.exit(bad)
