#!/usr/bin/env python3
"""I243-mac: an independent check of a count's samples at a second scale. Every interval of every edge gets one new
sample at its golden-section point (fraction PHI = 0.382 from its start), and the two pieces are checked: each step at
most tol (pi/4) and their sum equal to the interval's own step to 1e-6. It shares the determinant code, g's factors and
the count's samples with the count; it does not use the alias rule of #242 or the count's bisection.

    python3 offset_check.py NAME HP_DIR [--phi=0.381966]    (records/NAME.jsonl's state and options; the count's
                                                             re-evaluated record and cache in NAME/data/)

A flag means the interval's phase change is not confirmed at the second scale. A flagged interval is then re-sampled by
the count's rules from a uniform grid of spacing 0.05 with the golden point (bisection to steps <= tol, then halving of every
step > tol/2 with the sum check, repeated until
nothing is added) and the boxes are restated from the edges' new phase changes. Reading rule, fixed before the run: no
flag, the windings stand (unchanged); a flag whose re-sampling gives the same phase change, unchanged; a change of
2 pi k on an edge, the boxes that use it are corrected by the sums of modecount_wind's box_def.
Why the golden point: a uniform rate that turns an interval by 2 pi k gives pieces of 0.382 * 2 pi k and 0.618 * 2 pi k,
both within tol of a multiple of 2 pi only for k >= 5 (the midpoint fails at every even k). planted_offset.py tests it.
New determinants go to NAME/data/offset_evals.jsonl, results to NAME/offset.json.
"""
import json
import math
import os
import sys
import time

import numpy as np

PHI = (3 - math.sqrt(5)) / 2
HGRID = 0.05          # spacing of the re-sampling grid of a flagged interval (t_check.py used 0.03)
BOX = {"B0": ({"L1": 1, "H0": 1, "V0": -1}, math.pi), "U0": ({"H0": -1, "L2": 1, "T0": 1, "V0b": -1}, 2 * math.pi),
       "B1a": ({"V1": 1, "H3": 1, "L1": -1}, math.pi), "B1b": ({"V2": 1, "H2": 1, "V1": -1}, math.pi),
       "B1c": ({"R1": 1, "H1": 1, "V2": -1}, math.pi), "B1": ({"R1": 1, "H1": 1, "H2": 1, "H3": 1, "L1": -1}, math.pi),
       "U": ({"R2": 1, "T": 1, "L2": -1, "H1": -1, "H2": -1, "H3": -1}, 2 * math.pi),
       "full": ({"R1": 1, "R2": 1, "T": 1, "L2": -1, "L1": -1}, math.pi)}
NAMES = {"Re=aR, Im 0->y1": "R1", "Re=a2, Im 0->y1": "V2", "Re=a1, Im 0->y1": "V1", "Re=aL, Im 0->y1": "L1",
         "Re=aLL, Im 0->y1": "V0", "Im=y1, Re aR->a2": "H1", "Im=y1, Re a2->a1": "H2", "Im=y1, Re a1->aL": "H3",
         "Im=y1, Re aL->aLL": "H0", "Re=aR, Im y1->y2": "R2", "Re=aL, Im y1->y2": "L2", "Re=aLL, Im y1->y2": "V0b",
         "Im=y2, Re aR->aL": "T", "Im=y2, Re aL->aLL": "T0"}


def wrap(a):
    return math.remainder(a, 2 * math.pi)


def resample(phase, a, b, tol, hmin_t, h_t, tm):
    """the count's rules on [a, b] (fractions of the edge), as I230-mac/t_check.py: a uniform grid of spacing at most
    h_t with the golden point tm, then bisection to |step| <= tol, then halving of every step > tol / 2 with the sum
    check, until nothing is added. phase(t) -> arg g. Returns (phase change, points, mismatches)"""
    n = max(2, int(math.ceil((b - a) / h_t)))
    v = {t: phase(t) for t in [a + (b - a) * i / n for i in range(n)] + [b, tm]}
    checked, bad = set(), 0
    while True:
        changed = True
        while changed:
            changed = False
            ts = sorted(v)
            for x, y in zip(ts[:-1], ts[1:]):
                if y - x >= hmin_t and abs(wrap(v[y] - v[x])) > tol:
                    v[0.5 * (x + y)] = phase(0.5 * (x + y))
                    changed = True
        ts = sorted(v)
        added = False
        for x, y in zip(ts[:-1], ts[1:]):
            d = wrap(v[y] - v[x])
            if abs(d) > tol / 2 and y - x >= hmin_t and (x, y) not in checked:
                checked.add((x, y))
                m = 0.5 * (x + y)
                v[m] = phase(m)
                added = True
                bad += abs(wrap(v[m] - v[x]) + wrap(v[y] - v[m]) - d) > 1e-6
        if not added:
            break
    ts = sorted(v)
    return sum(wrap(v[y] - v[x]) for x, y in zip(ts[:-1], ts[1:])), len(ts), bad


def check(rec, gfun, phi=PHI, resample_flags=True, mutate=None):
    """rec: a count record; gfun(lam) -> complex ln g (for a sample point it must equal the record's sample).
    Returns (per-edge results, boxes restated)."""
    tol = rec["tol"]
    out, dphi = {}, {}
    for label, e in rec["edges"].items():
        name = NAMES.get(label, label)
        z0, z1 = complex(*e["z0"]), complex(*e["z1"])
        L = abs(z1 - z0)
        S = e["samples"]
        flags, change, max_piece, max_sum = [], 0.0, 0.0, 0.0
        for a, b in zip(S[:-1], S[1:]):
            s = wrap(b[2] - a[2])
            tm = a[0] + phi * (b[0] - a[0])
            # mutate=interp (the control): no new sample, the golden point's phase interpolated from the endpoints
            pm = a[2] + phi * s if mutate == "interp" else gfun(z0 + tm * (z1 - z0)).imag
            s1, s2 = wrap(pm - a[2]), wrap(b[2] - pm)
            max_piece, max_sum = max(max_piece, abs(s1), abs(s2)), max(max_sum, abs(s1 + s2 - s))
            if abs(s1) > tol or abs(s2) > tol or abs(s1 + s2 - s) > 1e-6:
                f = dict(t=[a[0], b[0]], re_im=[[(z0 + a[0] * (z1 - z0)).real, (z0 + a[0] * (z1 - z0)).imag],
                                                [(z0 + b[0] * (z1 - z0)).real, (z0 + b[0] * (z1 - z0)).imag]],
                         step=s, pieces=[s1, s2])
                if resample_flags:
                    new, npts, bad = resample(lambda t: gfun(z0 + t * (z1 - z0)).imag, a[0], b[0], tol, 1e-4 / L,
                                              HGRID / L, tm)
                    f.update(resampled=new, points=npts, mismatches=bad, turns=(new - s) / (2 * math.pi))
                    change += new - s
                flags.append(f)
        out[name] = dict(intervals=len(S) - 1, flags=flags, dphi_old=e["dphi"], dphi_new=e["dphi"] + change,
                         max_piece=max_piece, max_sum_error=max_sum)
        dphi[name] = e["dphi"] + change
    boxes = {}
    for b, (eds, div) in BOX.items():
        if all(n in dphi for n in eds):
            boxes[b] = dict(old=rec["boxes"][b]["winding_g"], new=sum(sg * dphi[n] for n, sg in eds.items()) / div)
    return out, boxes


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    name, hp = sys.argv[1:3]
    phi = float(([a.split("=", 1)[1] for a in sys.argv[3:] if a.startswith("--phi=")] or [PHI])[0])
    sys.path.insert(0, hp)
    from modecount_common import setup, horizon_poles
    rec0 = json.loads(open(os.path.join(here, "records", name + ".jsonl")).readline())
    data = os.path.join(here, name, "data")
    rec = [r for r in (json.loads(l) for l in open(os.path.join(data, "modecount_results.jsonl")))
           if r["tag"] == rec0["tag"]][-1]
    cache_file = [f for f in os.listdir(data) if f.endswith("_evals.jsonl") and not f.startswith("offset")][0]
    ev = {}
    for f in (cache_file, "offset_evals.jsonl"):
        p = os.path.join(data, f)
        if os.path.exists(p):
            for line in open(p):
                x = json.loads(line)
                ev[(x["re"], x["im"])] = complex(x["lnabs"], x["arg"])
    toks = open(os.path.join(here, name, "count.cmd")).read().split()
    state = toks[2]
    fmax = float([t for t in toks if t.startswith("--fmax=")][0].split("=", 1)[1])
    kf = None if rec["kfreeze"] is None else rec["kfreeze"]
    st = setup(state, M=rec["M"], kf=kf, fmax=fmax)
    poles = [p for _, p in horizon_poles(st)]
    Q = np.array([p for p in poles if abs(p.imag) < rec["y2"] + 3 * rec["omega"]], complex)
    assert len(Q) == rec["n_candidate_poles_factored"], (len(Q), rec["n_candidate_poles_factored"])
    K = np.array([complex(*z) for z in rec["expected_zeros"]])
    pc = rec["trend"]
    keys = np.array([complex(*k) for k in ev]) if ev else np.zeros(0, complex)
    vals = list(ev.values())
    cf = open(os.path.join(data, "offset_evals.jsonl"), "a")
    nnew = [0]

    def gfun(lam):
        key = (float(lam.real), float(lam.imag))
        i = int(np.argmin(np.abs(keys - lam))) if len(keys) else -1
        if i >= 0 and abs(keys[i] - lam) < 1e-9:      # the record stores t to 10 digits
            v = vals[i]
        elif key in ev:
            v = ev[key]
        else:
            t = time.time()
            la, arg, pmin, pmax = st.det(*key)
            x = dict(re=key[0], im=key[1], lnabs=la, arg=arg, pmin=pmin, pmax=pmax, sec=round(time.time() - t, 2))
            cf.write(json.dumps(x) + "\n")
            cf.flush()
            ev[key] = v = complex(la, arg)
            nnew[0] += 1
            print(f"  det {nnew[0]} at {key[0]:.6f}{key[1]:+.6f}i: {x['sec']} s", flush=True)
        return v + complex(np.sum(np.log(lam - Q)) - np.sum(np.log(lam - K))) - complex(np.polyval(pc, lam))

    # the stored samples must be reproduced by gfun (same factors, trend and cache)
    worst = 0.0
    for e in rec["edges"].values():
        z0, z1 = complex(*e["z0"]), complex(*e["z1"])
        for s in e["samples"]:
            v = gfun(z0 + s[0] * (z1 - z0))
            worst = max(worst, abs(v.real - s[1]), abs(wrap(v.imag - s[2])))
    print(f"{name}: g reproduces the record's samples to {worst:.1e}", flush=True)
    assert worst < 1e-4
    out, boxes = check(rec, gfun, phi)
    nflag = sum(len(v["flags"]) for v in out.values())
    res = dict(name=name, tag=rec["tag"], phi=phi, stored_check=worst, new_determinants=nnew[0], flags=nflag,
               intervals=sum(v["intervals"] for v in out.values()), edges=out, boxes=boxes,
               time=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))
    json.dump(res, open(os.path.join(here, name, "offset.json"), "w"), indent=1)
    for n, v in out.items():
        for f in v["flags"]:
            print(f"  {n}: flagged {f['re_im']}, step {f['step']:+.3f}, pieces {f['pieces'][0]:+.3f} {f['pieces'][1]:+.3f}"
                  + (f", re-sampled {f['resampled']:+.4f} ({f['points']} points, {f['mismatches']} mismatches, "
                     f"{f['turns']:+.4f} turns)" if "resampled" in f else ""))
    print(f"{name}: largest piece {max(v['max_piece'] for v in out.values()):.3f} rad, largest sum error "
          f"{max(v['max_sum_error'] for v in out.values()):.1e}")
    print(f"{name}: {nflag} of {res['intervals']} intervals flagged, {nnew[0]} new determinants; boxes "
          + ", ".join(f"{b} {x['old']:+.4f} -> {x['new']:+.4f}" for b, x in boxes.items()))


if __name__ == "__main__":
    main()
