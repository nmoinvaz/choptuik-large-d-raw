"""#1012 closing addition (the coordinator's hc, 2026-11-19 ~11:05 UTC): the noise of M = 9's corrected level-5 residual r5 at XI 0.11 at ONE fixed x, under tiny relative perturbations of the
nested levels' starts, so that the level-5 floor (4e-5 to 1.4e-3 at every step and rtol tried) can be compared with the noise and the omega error it induces judged.

    python noise_r5.py SRC MODE REL N OUT.json [--seed S]          SRC = solver/inner_stokes (D:/choptuik-h9b/...), INNER_NB_RTOL=1e-13 in the environment
      MODE nested   perturb the starts of the nested unknowns (levels 7 and 9: x[6:10]) by x (1 + REL u), u uniform(-1, 1)  [the measurement]
      MODE zero     no perturbation: N repeats from identical starts, each with a fresh Hier                                  [control A: must give identically zero spread]
      MODE x5       perturb the level-5 unknowns x[4:6] by (1 + REL u) and leave the nested starts alone                        [control B: a signal, r5c must move by K55 * dx5]

The fixed x is #1012 stage 1's (XI 0.11, AP 0.105, --h5=1e-4) state at its second level-5 solve's |r_5| = 4.254e-5, from the log (9 decimals; the nested levels are re-solved anyway):
A 2.719219, w/w_inf 1.000022, B3 0.148977988, C3 0.014770713, B5 0.008424405, C5 0.001512501, B7 0.000475371, C7 0.000122633, B9 2.6656e-05, C9 9.003e-06. The setup mirrors the runs:
LazyHier(9, r1 0.15, top 3), --schur (K from leak_jac at the nested-solved state, predict off), tol 0, floor_max 1e-4, approach 5:0.105, polish 5:0.11, levels 5, 7, 9 in polish mode,
default finite-difference steps. Each sample uses a FRESH Hier (K copied in) so the chord-Jacobian state of earlier samples cannot leak in. The output holds, per sample, the corrected full
residual (rows 0-9: r1 = rows 0,1; r3 = 2,3; r5 = 4,5; r7 = 6,7; r9 = 8,9) and the raw r5."""
import json, os, sys, time
import numpy as np

SRC, MODE, REL, N, OUT = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
SEED = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 1012
os.environ.setdefault("INNER_NB_RTOL", "1e-13")
sys.path.insert(0, SRC)
import hier_nb as HN, hier as H

X0 = np.array([2.719219, 1.000022, 0.148977988, 0.014770713, 0.008424405, 0.001512501, 0.000475371, 0.000122633, 2.6656e-05, 9.003e-06])


def make(K=None):
    h = HN.LazyHier(9, 0.15, top=3, verbose=0)
    h.predict, h.schur, h.tol, h.fasttrial, h.floorstop, h.floor_max = False, True, 0.0, False, False, 1e-4
    h.approach, h.polish = {5: 0.105}, {5: 0.11}
    h.mode = {5: "top", 7: "top", 9: "top"}
    if K is not None:
        h.K = K.copy()
    return h


t0 = time.time()
h0 = make()
xs, r_unc = h0.solve_from(7, X0.copy())                    # nested levels 7, 9 solved at the fixed x (no Schur correction yet)
h0.leak_jac(xs)                                            # K at that state
K = h0.K.copy()
base_x, base_r = make(K).solve_from(7, xs.copy())          # the corrected residual at the fixed x, from the solved start
print(f"setup {time.time() - t0:.0f} s; |r5| corrected at the fixed x {np.hypot(*base_r[4:6]):.3e}, raw {np.hypot(*make(K).res_raw(base_x)[4:6]):.3e}; max |K[5, :]| {np.abs(K[4:6]).max():.2e}", flush=True)
rng = np.random.default_rng(SEED)
samples = []
for s in range(N):
    xp = xs.copy()
    u = rng.uniform(-1, 1, size=10)
    if MODE == "nested":
        xp[6:10] *= 1 + REL * u[6:10]
    elif MODE == "x5":
        xp[4:6] *= 1 + REL * u[4:6]
    elif MODE != "zero":
        raise SystemExit("MODE must be nested, zero or x5")
    hh = make(K)
    xn, rn = hh.solve_from(7, xp)
    raw = hh.res_raw(xn)
    samples.append(dict(r=[float(v) for v in rn], raw5=[float(v) for v in raw[4:6]], x=[float(v) for v in xn]))
    print(f"sample {s + 1}/{N}: |r5c| {np.hypot(*rn[4:6]):.4e}  r5c {rn[4]:+.4e} {rn[5]:+.4e}  |r7| {np.hypot(*rn[6:8]):.2e}  |r9| {np.hypot(*rn[8:10]):.2e}  [{time.time() - t0:.0f} s]", flush=True)
R = np.array([s["r"] for s in samples])
dev = R - np.array([float(v) for v in base_r])
summary = dict(mode=MODE, rel=REL, n=N, seed=SEED, base_r=[float(v) for v in base_r],
               std=[float(v) for v in R.std(axis=0, ddof=1)] if N > 1 else None, maxdev=[float(v) for v in np.abs(dev).max(axis=0)], fixed_x=[float(v) for v in X0], K5max=float(np.abs(K[4:6]).max()))
json.dump(dict(summary=summary, samples=samples), open(OUT, "w"), indent=1)
lab = ["r1 re", "r1 im", "r3 B", "r3 C", "r5 B", "r5 C", "r7 B", "r7 C", "r9 B", "r9 C"]
print("row: std over samples / max deviation from the base value")
for i in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
    print(f"  {lab[i]}: {summary['std'][i] if N > 1 else float('nan'):.3e} / {summary['maxdev'][i]:.3e}")
