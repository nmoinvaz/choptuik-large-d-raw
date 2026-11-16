"""I902-mac check: does raising the horizon order lift the weak grip on Delta at D 237-254, at the stored z?

Reads the near_null.py JSONs nn_D<d>_ks<K>.json (d 237, 249, 253 and 60; K 130, 160, 200, 250), the control's
nn_D253_ks250_mutks.json, the vectors V_D<d>_ks<K>.npy, and model.log (`solver/factored_horizon_sympy.py model`, its
M2 lines: ln f at K 130, 160, 200 and 250 for mu 1 and 3 at each of #693's states).

The reading is the grip on Delta, g = 1 / ||e_Delta^T J^-1||_2 (near_null.py), the size of Delta's response to a
residual. It does not depend on the order of the sigma, which changes once a weak mode rises past another (at
D 237.13, sigma_4 / sigma_3 = 1.8, #488). The model's prediction for ks 130 -> K is P(K) = ln f(K) - ln f(130), mu 1.
The sigma are reported by index, and the Delta mode is followed by its vector: the one of the largest Delta share at
ks 130, matched at each K to the vector of the largest overlap (tracked when the overlap is at least 0.5).

Criteria (each can fail):
  support   at D 237.13, 249.01 and 253.80: ln g(200) - ln g(130) within 30% of P(200), and |ln g(250) - ln g(200)| < 1
  refute    at D 253.80: |ln g(250) - ln g(130)| < ln 2
  control   at D 60: |ln g(K) - ln g(130)| < 0.05 and |ln sigma_i(K) - ln sigma_i(130)| < 0.05, i = 1..4, each K
  mutation  nn_D253_ks250_mutks.json (--ks 250 --mutate=ks) equals nn_D253_ks130.json: sigma, grip, pivots, steps
  runs      every run's near_null check passed (z unchanged; ||J v_1|| / sigma_1), and every run at a changed ks has
            only its horizon block's rows changed
The verdict is "supports" when support holds at all three D and refute does not, "refutes" when refute holds, and
"neither" otherwise. The same verdict read on sigma_3 by index (the issue's wording) is printed beside it, with whether
the two agree (reported, the coordinator's word on #902).

Run: python3 sigma.py FOLDER, or python3 sigma.py --selftest (planted: a grip that follows the model supports, a flat
one refutes, a control off by 0.1 fails, a mutation run one ulp off fails). Exits 1 when a criterion other than the
verdict fails, or the selftest does.
"""
import json
import math
import os
import re
import sys

import numpy as np

DS = {"237": 237.13, "249": 249.01, "253": 253.80}
KS = (130, 160, 200, 250)


def model(path):
    """ln f[D][mu][K] from the M2 lines of model.log"""
    pat = re.compile(r"^\s+D (\d+\.\d+) Re s .*mu 1: peak \d+, ln f (\S+) (\S+) (\S+) (\S+); mu 3: peak \d+, "
                     r"ln f (\S+) (\S+) (\S+) (\S+)")
    out = {}
    for line in open(path):
        mt = pat.match(line)
        if mt:
            v = [float(x) for x in mt.groups()[1:]]
            out[round(float(mt.group(1)), 2)] = {1: dict(zip(KS, v[:4])), 3: dict(zip(KS, v[4:]))}
    return out


def track(V0, V, i0):
    """the index in V of the largest overlap with V0's vector i0, and the overlap"""
    ov = np.abs(V.T @ V0[:, i0])
    return int(ov.argmax()), float(ov.max())


def evaluate(runs, vecs, lnf, mut):
    """runs[d][K]: near_null records; vecs[d][K]: V; lnf: model; mut: the --mutate=ks record"""
    res, ok_all = {}, True
    print("sigma: g = 1 / ||e_Delta^T J^-1||_2; P(K) = ln f(K) - ln f(130), mu 1 (model.log)")
    for d in ("237", "249", "253", "60"):
        r = runs[d]
        lg = {K: math.log(r[K]["grip"]["two"]) for K in KS}
        sig = {K: [v["sigma"] for v in r[K]["vectors"]] for K in KS}
        dsh = [v["delta"] for v in r[130]["vectors"]]
        i0 = int(np.argmax(dsh))
        print(f"  D {d}: the Delta mode at ks 130 is sigma_{i0 + 1} (Delta share {dsh[i0]:.2f})")
        for K in KS:
            line = (f"    ks {K}: ln g {lg[K]:+.4f} (ln g - ln g(130) {lg[K] - lg[130]:+.4f}); sigma "
                    + ", ".join(f"{x:.3e}" for x in sig[K]))
            if d in DS:
                P = lnf[DS[d]][1][K] - lnf[DS[d]][1][130]
                line += f"; P {P:+.2f} (mu 3 {lnf[DS[d]][3][K] - lnf[DS[d]][3][130]:+.2f})"
            if vecs.get(d, {}).get(K) is not None and vecs[d].get(130) is not None:
                j, ov = track(vecs[d][130], vecs[d][K], i0)
                line += (f"; the Delta mode at sigma_{j + 1} {sig[K][j]:.3e} (overlap {ov:.2f}, ln sigma - ln "
                         f"sigma(130) {math.log(sig[K][j] / sig[130][i0]):+.3f})" if ov >= 0.5 else
                         f"; the Delta mode not among the {len(sig[K])} smallest (largest overlap {ov:.2f})")
            print(line)
        res[d] = lg
    checks = []
    sup = {}
    for d, D in DS.items():
        lg = res[d]
        P = lnf[D][1][200] - lnf[D][1][130]
        a = lg[200] - lg[130]
        b = lg[250] - lg[200]
        sup[d] = abs(a / P - 1) <= 0.3 and abs(b) < 1
        print(f"  support D {D:.2f}: ln g(200) - ln g(130) {a:+.3f} against P(200) {P:+.2f} ({a / P - 1:+.2f} of it, "
              f"|.| <= 0.3); ln g(250) - ln g(200) {b:+.3f} (|.| < 1): {'holds' if sup[d] else 'does not hold'}")
    rv = res["253"][250] - res["253"][130]
    refute = abs(rv) < math.log(2)
    print(f"  refute D 253.80: ln g(250) - ln g(130) {rv:+.3f} (|.| < ln 2): {'holds' if refute else 'does not hold'}")
    r60 = runs["60"]
    worst = 0.0
    for K in KS[1:]:
        worst = max(worst, abs(math.log(r60[K]["grip"]["two"] / r60[130]["grip"]["two"])),
                    *(abs(math.log(a["sigma"] / b["sigma"])) for a, b in zip(r60[K]["vectors"][:4],
                                                                             r60[130]["vectors"][:4])))
    checks.append(("control", worst < 0.05, f"D 60: the largest |ln g(K) - ln g(130)| or |ln sigma_i(K) - ln "
                   f"sigma_i(130)| {worst:.2e} (< 0.05)"))
    base = runs["253"][130]
    same = all(mut[k] == base[k] for k in ("pivots", "grip", "step", "step_pinned")) and \
        [v["sigma"] for v in mut["vectors"]] == [v["sigma"] for v in base["vectors"]]
    checks.append(("mutation", same and mut["mutate"] == "ks" and mut["ks"] == 250,
                   "--ks 250 --mutate=ks against ks 130 at D 253.80: " + ("equal" if same else "NOT equal")))
    bad = [f"D {d} ks {K}" for d in runs for K in KS
           if not runs[d][K].get("passed", True) or (runs[d][K]["rows"] is not None and not runs[d][K]["rows"]["ok"])]
    checks.append(("runs", not bad, "every run's check, and only the horizon block changed: "
                   + ("pass" if not bad else "FAIL at " + ", ".join(bad))))
    for name, ok, what in checks:
        print(f"  check {name}: {what}: {'pass' if ok else 'FAIL'}")
        ok_all &= ok
    verdict = "refutes" if refute else "supports" if all(sup.values()) else "neither"
    print(f"  verdict: {verdict} the reading")
    # the issue's sigma_3 by index under the same bars (reported; the coordinator's word: say if it disagrees with g)
    s3 = {d: {K: math.log(runs[d][K]["vectors"][2]["sigma"]) for K in KS} for d in DS}
    sup3 = {d: abs((s3[d][200] - s3[d][130]) / (lnf[D][1][200] - lnf[D][1][130]) - 1) <= 0.3
            and abs(s3[d][250] - s3[d][200]) < 1 for d, D in DS.items()}
    ref3 = abs(s3["253"][250] - s3["253"][130]) < math.log(2)
    v3 = "refutes" if ref3 else "supports" if all(sup3.values()) else "neither"
    print("  sigma_3 by index: " + "; ".join(f"D {D:.2f} ln sigma_3(200) - (130) {s3[d][200] - s3[d][130]:+.3f}, "
                                          f"(250) - (200) {s3[d][250] - s3[d][200]:+.3f}" for d, D in DS.items())
          + f"; verdict {v3}: g and sigma_3 {'agree' if v3 == verdict else 'DISAGREE'}")
    return ok_all, verdict


def planted(kind):
    """runs following the model (kind 'model'), flat ('flat'), a control off by 0.1 ('ctl'), a mutation off ('mut')"""
    lnf = {D: {mu: {K: (-50.0 if K == 130 else -20.0 if K == 160 else -0.5 if K == 200 else -0.01) * D / 250
                    for K in KS} for mu in (1, 3)} for D in DS.values()}
    runs = {}
    for d in ("237", "249", "253", "60"):
        runs[d] = {}
        for K in KS:
            lg = -50.0 + (lnf[DS[d]][1][K] - lnf[DS[d]][1][130] if d in DS and kind != "flat" else 0.0)
            if d == "60" and kind == "ctl" and K == 250:
                lg += 0.1
            vec = [dict(sigma=1e-25 * (i + 1), delta=0.9 if i == 2 else 0.01) for i in range(6)]
            runs[d][K] = dict(grip=dict(two=math.exp(lg)), vectors=vec, pivots=[1e-23, 1e33], step={"max": 1.0},
                              step_pinned={"max": 1.0}, rows=None if K == 130 else dict(ok=True), passed=True,
                              mutate="", ks=K)
    mut = json.loads(json.dumps(runs["253"][130]))
    mut.update(mutate="ks", ks=250)
    if kind == "mut":
        mut["vectors"][0]["sigma"] = float(np.nextafter(mut["vectors"][0]["sigma"], 1.0))
    return runs, {}, lnf, mut


argv = sys.argv[1:]
if argv[0] == "--selftest":
    res = []
    for kind, want in [("model", (True, "supports")), ("flat", (True, "refutes")), ("ctl", (False, "supports")),
                       ("mut", (False, "supports"))]:
        print(f"planted {kind} (want {'pass' if want[0] else 'FAIL'}, {want[1]})")
        res.append(evaluate(*planted(kind)) == want)
    ok = all(res)
    print(f"sigma selftest: {'PASS' if ok else 'FAIL'}")
else:
    d0 = argv[0]
    lnf = model(os.path.join(d0, "model.log"))
    runs, vecs = {}, {}
    for d in ("237", "249", "253", "60"):
        runs[d], vecs[d] = {}, {}
        for K in KS:
            runs[d][K] = json.load(open(os.path.join(d0, f"nn_D{d}_ks{K}.json")))
            fv = os.path.join(d0, f"V_D{d}_ks{K}.npy")
            vecs[d][K] = np.load(fv) if os.path.exists(fv) else None
    ok, verdict = evaluate(runs, vecs, lnf, json.load(open(os.path.join(d0, "nn_D253_ks250_mutks.json"))))
    print(f"sigma: {'PASS' if ok else 'FAIL'} (verdict: {verdict})")
sys.exit(0 if ok else 1)
