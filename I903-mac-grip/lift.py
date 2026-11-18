"""I903-mac-grip check: how much of the horizon cut do the fixed-order chains (orders 142 and 160) leave near the fold?

Reads near_null.py's JSONs nn_<tag>_D<d>_ks<K>[_mutks].json (tag k142: xfkappa's I903-mac/chain_fixed; k160: dh610's
I903-dh610/chain_k160; k140 was its first plan; k135: macm3b's I903-macm3/chain_k135; ctl: #902's D 60 state) and the vectors V_<tag>_D<d>_ks<K>.npy. Each state is read at its own
order (the smallest K of its runs) and at ks 200, at the stored z with no Newton step (#902's method).

The reading is the lift L = ln g(200) - ln g(own), g = 1 / ||e_Delta^T J^-1||_2. The coordinator's bar (#903): at the
base near D 255 of each chain, L < ln 10 says the chain's order leaves little of the cut, so the fixed-order fold test is a
fair test of it; L >= ln 10 says it leaves a large part, so the fold could stay put at that order and still move at a
higher one. Bases: the first stored base with D >= T - 1 for T = 230, 240, 245, 250, 255.

Checks (each can fail):
  runs      every run's near_null check passed (sigma_1 converged to 1e-3, ||J v_1|| / sigma_1 within 1e-2, z unchanged),
            and at ks 200 only the horizon block's rows of F and J changed, F's there nonzero
  mutation  each *_mutks run (--ks 200 --mutate=ks, built at the own order) equals the own-order run bit for bit
  control   ctl (D 60): |L| and |ln sigma_i(200) - ln sigma_i(own)|, i = 1..4, below 0.05
Reported: L at every base with sigma_1-4 at both orders, the Delta mode followed by overlap, Delta's pinned step at
200, and the horizon rows' max|dF|. And the split of 1/g^2 = sum_i v_i,Delta^2 / sigma_i^2 (exact over all singular
triplets; v_i,Delta^2 is near_null's Delta share) over the six computed modes: the share each carries, with its top
harmonic, and the six's sum against 1/g^2 (coverage), which says which mode sets the grip.

Run: python3 lift.py FOLDER, or python3 lift.py --selftest (planted: a lift of 1 reads small, 5 reads large, a failed
run, a mutation one ulp off and a control off by 0.1 fail). Exits 1 when a check fails or the selftest does.
"""
import glob
import json
import math
import os
import re
import sys

import numpy as np

TARGETS = (230, 240, 245, 250, 255)
BAR = math.log(10)
NAME = re.compile(r"nn_(k135|k142|k160|k140|ctl)_D([\d.]+)_ks(\d+)(_mutks)?\.json$")


def load(d0):
    """groups[(tag, d)] = {"runs": {K: rec}, "mut": rec or None, "V": {K: array}}"""
    groups = {}
    for p in sorted(glob.glob(os.path.join(d0, "nn_*.json"))):
        mt = NAME.search(os.path.basename(p))
        if not mt:
            continue
        tag, d, K, mut = mt.group(1), mt.group(2), int(mt.group(3)), mt.group(4)
        g = groups.setdefault((tag, d), {"runs": {}, "mut": None, "V": {}})
        rec = json.load(open(p))
        if mut:
            g["mut"] = rec
        else:
            g["runs"][K] = rec
            fv = os.path.join(d0, f"V_{tag}_D{d}_ks{K}.npy")
            g["V"][K] = np.load(fv) if os.path.exists(fv) else None
    return groups


def split(r):
    """the six modes' shares of 1/g^2 = sum_i delta_i / sigma_i^2, and their sum against 1/g^2"""
    c = [v["delta"] / v["sigma"] ** 2 for v in r["vectors"]]
    tot = r["grip"]["two"] ** -2
    o = sorted(range(len(c)), key=lambda i: -c[i])
    return sum(c) / tot, [(i, r["vectors"][i]["top"][0][1], c[i] / tot) for i in o[:2]]


def target(D):
    t = [T for T in TARGETS if D >= T - 1]
    return t[-1] if t else None


def evaluate(groups):
    print(f"lift: L = ln g(200) - ln g(own), g = 1 / ||e_Delta^T J^-1||_2; bar at D 255: L < ln 10 = {BAR:.4f}")
    bad, checks, reading, last = [], [], {}, {}
    for (tag, d), g in sorted(groups.items(), key=lambda t: (t[0][0], float(t[0][1]))):
        runs = g["runs"]
        for K, r in runs.items():
            if not r.get("passed", False) or (r["rows"] is not None and not r["rows"]["ok"]):
                bad.append(f"{tag} D {d} ks {K}")
        if len(runs) < 2 or 200 not in runs:
            print(f"  {tag} D {d}: runs at ks {sorted(runs)} (incomplete)")
            continue
        own = min(runs)
        a, b = runs[own], runs[200]
        L = math.log(b["grip"]["two"] / a["grip"]["two"])
        D = float(b["D"])
        sa = [v["sigma"] for v in a["vectors"][:4]]
        sb = [v["sigma"] for v in b["vectors"][:4]]
        dsh = [v["delta"] for v in a["vectors"]]
        i0 = int(np.argmax(dsh))
        line = (f"  {tag} D {D:.4f} (target {target(D)}): ks {own} ln g {math.log(a['grip']['two']):+.4f}, ks 200 "
                f"{math.log(b['grip']['two']):+.4f}, L {L:+.4f}; sigma_1-4 at {own} "
                + ", ".join(f"{x:.3e}" for x in sa) + "; at 200 " + ", ".join(f"{x:.3e}" for x in sb)
                + f"; the Delta mode at {own} sigma_{i0 + 1} (share {dsh[i0]:.2f})")
        if g["V"].get(own) is not None and g["V"].get(200) is not None:
            ov = np.abs(g["V"][200].T @ g["V"][own][:, i0])
            j = int(ov.argmax())
            line += (f", at 200 sigma_{j + 1} {b['vectors'][j]['sigma']:.3e} (overlap {ov[j]:.2f}, ln ratio "
                     f"{math.log(b['vectors'][j]['sigma'] / a['vectors'][i0]['sigma']):+.3f})")
        hz = b["rows"]["blocks"]["horizon"]["F"] if b["rows"] else None
        line += (f"; Delta's pinned step at 200 {b['step_pinned']['delta']:+.3e}"
                 + (f"; horizon max|dF| {hz:.2e}" if hz is not None else ""))
        for K, r in ((own, a), (200, b)):
            if "top" in r["vectors"][0]:
                cov, top = split(r)
                line += (f"; 1/g^2 at {K}: " + ", ".join(f"sigma_{i + 1} (k{h}) {f:.3f}" for i, h, f in top)
                         + f", six {cov:.3f}")
        print(line)
        if tag == "ctl":
            worst = max([abs(L)] + [abs(math.log(y / x)) for x, y in zip(sa, sb)])
            checks.append(("control", worst < 0.05, f"D {D:.2f}: the largest |L| or |ln sigma_i(200) - ln "
                           f"sigma_i({own})| {worst:.2e} (< 0.05)"))
        elif target(D) == 255:
            reading[tag] = (D, L)
        if tag != "ctl" and D > last.get(tag, (0, 0))[0]:
            last[tag] = (D, L)
        m = g["mut"]
        if m is not None:
            same = all(m[k] == a[k] for k in ("pivots", "grip", "step", "step_pinned")) and \
                [v["sigma"] for v in m["vectors"]] == [v["sigma"] for v in a["vectors"]]
            checks.append(("mutation", same and m["mutate"] == "ks" and m["ks"] == 200,
                           f"{tag} D {D:.4f}: --ks 200 --mutate=ks against ks {own}: "
                           + ("equal" if same else "NOT equal")))
    checks.append(("runs", not bad, "every run's check, and only the horizon block changed: "
                   + ("pass" if not bad else "FAIL at " + ", ".join(bad))))
    ok = True
    for name, c, what in checks:
        print(f"  check {name}: {what}: {'pass' if c else 'FAIL'}")
        ok &= c
    for tag in ("k135", "k142", "k160"):
        if tag in reading:
            D, L = reading[tag]
            print(f"  reading {tag} at D {D:.4f}: L {L:+.4f} " + (
                f"< ln 10: order {tag[1:]} leaves little of the cut; the fold test is a fair test of it" if L < BAR else
                f">= ln 10: order {tag[1:]} leaves a large part of the cut; its fold could stay and still move higher"))
        else:
            print(f"  reading {tag}: no base near D 255 yet"
                  + (f"; its last base, D {last[tag][0]:.4f}: L {last[tag][1]:+.4f} "
                     f"({'<' if last[tag][1] < BAR else '>='} ln 10, {255 - last[tag][0]:.2f} short of D 255)"
                     if tag in last else ""))
    return ok, {t: v[1] < BAR for t, v in reading.items()}


def planted(kind):
    """one k142 base near D 255 with a lift of 1 (kind 'small') or 5 ('large'), a ctl group and a mutation run"""
    def rec(K, lg, ks0, passed=True):
        vec = [dict(sigma=1e-20 * (i + 1), delta=0.9 if i == 0 else 0.01) for i in range(6)]
        rows = None if K == ks0 else dict(ok=True, blocks=dict(horizon=dict(F=1e-20)))
        return dict(D=254.5, grip=dict(two=math.exp(lg)), vectors=vec, pivots=[1e-20, 1e30], step={"max": 1.0},
                    step_pinned={"max": 1.0, "delta": 1e-9}, rows=rows, passed=passed, mutate="", ks=K)
    lift = 5.0 if kind == "large" else 1.0
    k = {"runs": {142: rec(142, -40.0, 142), 200: rec(200, -40.0 + lift, 142, kind != "failed")}, "V": {},
         "mut": None}
    k["mut"] = json.loads(json.dumps(k["runs"][142]))
    k["mut"].update(mutate="ks", ks=200)
    if kind == "mut":
        k["mut"]["vectors"][0]["sigma"] = float(np.nextafter(k["mut"]["vectors"][0]["sigma"], 1.0))
    c = {"runs": {142: rec(142, -19.0, 100), 200: rec(200, -19.0 + (0.1 if kind == "ctl" else 0.0), 100)}, "V": {},
         "mut": None}
    for r in c["runs"].values():
        r["D"] = 60.0
    return {("k142", "254.5"): k, ("ctl", "60.0"): c}


argv = sys.argv[1:]
if argv and argv[0] == "--selftest":
    res = []
    for kind, want in [("small", (True, True)), ("large", (True, False)), ("failed", (False, True)),
                       ("mut", (False, True)), ("ctl", (False, True))]:
        print(f"planted {kind} (want {'pass' if want[0] else 'FAIL'}, {'small' if want[1] else 'large'})")
        ok, rd = evaluate(planted(kind))
        res.append((ok, rd.get("k142")) == want)
    ok = all(res)
    print(f"lift selftest: {'PASS' if ok else 'FAIL'}")
else:
    ok, _ = evaluate(load(argv[0]))
    print(f"lift: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
