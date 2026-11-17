"""#941: read near_null.py's JSONs (oORDER_DDDD.json, run941.sh) and tabulate the Delta mode, the harmonic-3 pair and sigma_5.

    python analyze941.py FOLDER                  (the tables; exit 1 if a state's vectors cannot be told apart)
    python analyze941.py --selftest [--mutate]   (planted records with known answers; --mutate swaps the expected sigma_Delta and
                                                  sigma_pair, so the selftest must then exit 1)

Per state the six vectors of near_null.py (sigma ascending) are classified by their content: the Delta mode is the vector with the
largest Delta share (it must exceed 0.5), a member of the harmonic-3 pair is a vector (not the Delta mode) whose two largest
(block, harmonic) components are (p1, 3) and (m_h, 3) in either order... one of them at least (its first or second component) and
the other among the five printed; exactly two must qualify. sigma_pair is the geometric mean of the two (both are printed).
sigma_5 is the fifth vector's sigma as near_null.py sorted it. Falls per unit D are (sigma_i / sigma_j)^(1/(D_j - D_i)) for
neighbouring states and, over the whole range, exp(-slope) of the least-squares line of ln sigma on D. The order test compares the
order-240 sigma with the order-160 one log-linearly interpolated to the same D (D 231.7466 lies past the last order-160 state, 231,
and is extrapolated: marked), within a factor 3 (#941)."""
import glob
import json
import math
import os
import re
import sys


def is_pair_member(top):
    names = {(b, k) for b, k, _ in top}
    first2 = {(b, k) for b, k, _ in top[:2]}
    return ("p1", 3) in names and ("m_h", 3) in names and bool(first2 & {("p1", 3), ("m_h", 3)})


def classify(rec):
    """-> dict(delta=index, pair=[i, j], s5=index) or raises ValueError"""
    v = rec["vectors"]
    d = max(range(len(v)), key=lambda i: v[i]["delta"])
    if v[d]["delta"] <= 0.5:
        raise ValueError(f"no vector has a Delta share above 0.5 (largest {v[d]['delta']:.3f})")
    pair = [i for i in range(len(v)) if i != d and is_pair_member(v[i]["top"])]
    if len(pair) != 2:
        raise ValueError(f"{len(pair)} vectors look like the harmonic-3 pair (need 2): {pair}")
    return dict(delta=d, pair=pair, s5=4)


def summary(rec):
    c = classify(rec)
    v = rec["vectors"]
    sd, (p1, p2), s5 = v[c["delta"]]["sigma"], [v[i]["sigma"] for i in c["pair"]], v[c["s5"]]["sigma"]
    return dict(D=rec["D"], c=c, sd=sd, sp=(p1, p2), spg=math.sqrt(p1 * p2), s5=s5, sig=[x["sigma"] for x in v])


def per_unit(Ds, ss):
    """(neighbour falls, least-squares fall over the range) of sigma(D), falls as factors per unit D"""
    nb = [(ss[i] / ss[i + 1]) ** (1 / (Ds[i + 1] - Ds[i])) for i in range(len(Ds) - 1)]
    n = len(Ds)
    mx, my = sum(Ds) / n, sum(math.log(s) for s in ss) / n
    slope = sum((d - mx) * (math.log(s) - my) for d, s in zip(Ds, ss)) / sum((d - mx) ** 2 for d in Ds)
    return nb, math.exp(-slope)


def resid(Ds, ss):
    """largest |ln sigma - (a + b D)| of the least-squares line, how far sigma is from a pure exponential in D"""
    n = len(Ds)
    mx, my = sum(Ds) / n, sum(math.log(s) for s in ss) / n
    b = sum((d - mx) * (math.log(s) - my) for d, s in zip(Ds, ss)) / sum((d - mx) ** 2 for d in Ds)
    return max(abs(math.log(s) - (my + b * (d - mx))) for d, s in zip(Ds, ss))


def interp(Ds, ss, D):
    """log-linear interpolation of sigma at D from the two nearest states; second value: True if D is outside [Ds[0], Ds[-1]]"""
    i = min(range(len(Ds) - 1), key=lambda i: min(abs(D - Ds[i]), abs(D - Ds[i + 1])) if Ds[i] <= D <= Ds[i + 1] else 1e9 + abs(D - Ds[i]))
    if D > Ds[-1]:
        i = len(Ds) - 2
    s = math.log(ss[i]) + (math.log(ss[i + 1]) - math.log(ss[i])) * (D - Ds[i]) / (Ds[i + 1] - Ds[i])
    return math.exp(s), not (Ds[0] <= D <= Ds[-1])


def load(folder):
    out = {}
    for p in sorted(glob.glob(os.path.join(folder, "o*_D*.json"))):
        m = re.match(r"o(\d+)_D([\d.]+)\.json$", os.path.basename(p))
        if m:
            out.setdefault(int(m.group(1)), []).append(summary(json.load(open(p))))
    return {k: sorted(v, key=lambda s: s["D"]) for k, v in out.items()}


def tables(folder):
    S = load(folder)
    ok = True
    for order in sorted(S, reverse=True):
        print(f"\n== order {order}: the six vectors per state (sigma, its convergence = relative change over the last two iterations, "
              f"Delta share, two largest (block, harmonic) components)")
        for st in S[order]:
            rec = json.load(open(os.path.join(folder, f"o{order}_D{st['D']:.4f}.json")))
            print(f"  D {st['D']:.4f}  pivots {rec['pivots'][0]:.3e}..{rec['pivots'][1]:.3e}  Delta mode = vector {st['c']['delta'] + 1}, "
                  f"pair = vectors {st['c']['pair'][0] + 1}, {st['c']['pair'][1] + 1}")
            for i, x in enumerate(rec["vectors"]):
                tag = "Delta" if i == st["c"]["delta"] else ("pair" if i in st["c"]["pair"] else "")
                print(f"    {i + 1}  sigma {x['sigma']:.4e}  conv {x['conv']:.1e}  Delta {x['delta']:.3f}  "
                      + "  ".join(f"{b} k{k} {s:.3f}" for b, k, s in x["top"][:2]) + f"   {tag}")
    print("\n== sigma_Delta, sigma_pair (geometric mean; the two members), sigma_5, ratios")
    print("order  D          sigma_Delta   sigma_pair    (members)                  sigma_5       Delta/pair   Delta/s5")
    for order in sorted(S, reverse=True):
        for st in S[order]:
            print(f"{order:<5}  {st['D']:<9.4f}  {st['sd']:.4e}   {st['spg']:.4e}    ({st['sp'][0]:.3e}, {st['sp'][1]:.3e})  {st['s5']:.4e}   "
                  f"{st['sd'] / st['spg']:<10.4g}   {st['sd'] / st['s5']:.4g}")
    print("\n== the fall per unit D (factor), neighbouring states and over the whole range (least squares of ln sigma on D)")
    for order in sorted(S, reverse=True):
        Ds = [s["D"] for s in S[order]]
        if len(Ds) < 2:
            print(f"order {order}: one state, no fall")
            continue
        for name, key in (("sigma_Delta", "sd"), ("sigma_pair", "spg"), ("sigma_5", "s5")):
            nb, ls = per_unit(Ds, [s[key] for s in S[order]])
            print(f"order {order}  {name:<12} neighbours {', '.join(f'{x:.3g}' for x in nb)}  whole range {ls:.3g}  "
                  f"(largest ln residual from a pure exponential in D: {resid(Ds, [s[key] for s in S[order]]):.3f})")
        r = [s["sd"] / s["spg"] for s in S[order]]
        print(f"order {order}  Delta/pair    {', '.join(f'{x:.4g}' for x in r)}  (last/first {r[-1] / r[0]:.3g})")
    if 240 in S and 160 in S:
        print("\n== order test: order-240 sigma against order 160 log-linearly interpolated to the same D (within 3 is a pass)")
        D160 = [s["D"] for s in S[160]]
        for key, name in (("sd", "sigma_Delta"), ("spg", "sigma_pair"), ("s5", "sigma_5")):
            for st in S[240]:
                v160, extra = interp(D160, [s[key] for s in S[160]], st["D"])
                f = st[key] / v160
                print(f"  {name:<12} D {st['D']:.4f}: order 240 {st[key]:.4e}, order 160 at that D {v160:.4e}"
                      f"{' (EXTRAPOLATED past D ' + format(D160[-1], 'g') + ')' if extra else ''}, ratio {f:.3f}: "
                      f"{'within 3' if 1 / 3 <= f <= 3 else 'OUTSIDE 3'}")
    if 135 in S and 160 in S:
        print("\n== control, order 135 against order 160 interpolated to the same D")
        D160 = [s["D"] for s in S[160]]
        for st in S[135]:
            for key, name in (("sd", "sigma_Delta"), ("spg", "sigma_pair"), ("s5", "sigma_5")):
                v160, extra = interp(D160, [s[key] for s in S[160]], st["D"])
                print(f"  D {st['D']:.4f} {name:<12} order 135 {st[key]:.4e}, order 160 {v160:.4e}, 135 / 160 = {st[key] / v160:.3e}")
    return ok


def fake(D, sd, sp, s5, dshare_pair=1e-3):
    """a record with a known Delta mode (vector 3), pair (vectors 1, 2) and sigma_5 (vector 5)"""
    vs = []
    for i, s in enumerate([sp * 0.99, sp * 1.01, sd, sd * 5, s5, s5 * 1.1]):
        top = [["p1", 3, 0.13], ["m_h", 3, 0.09]] if i < 2 else [["p1", 1, 0.06], ["m_h", 1, 0.04]]
        vs.append(dict(sigma=s, conv=0.0, delta=0.8 if i == 2 else dshare_pair, top=top, blocks={}))
    return dict(D=D, vectors=vs, pivots=[1e-20, 1e34])


def selftest(mutate):
    sd, sp, s5 = 7.9e-16, 3.5e-18, 1.5e-10
    st = summary(fake(230.0, sd, sp, s5))
    gm = math.sqrt(0.99 * 1.01)           # the pair's members are 0.99 sp and 1.01 sp
    exp_sd, exp_sp = (sp * gm, sd) if mutate else (sd, sp * gm)
    ok = st["c"]["delta"] == 2 and st["c"]["pair"] == [0, 1] and abs(st["sd"] / exp_sd - 1) < 1e-12 and abs(st["spg"] / exp_sp - 1) < 1e-12 \
        and abs(st["s5"] / s5 - 1) < 1e-12
    nb, ls = per_unit([229.0, 230.0, 231.0], [1e-14, 1e-15, 1e-16])
    ok = ok and abs(nb[0] - 10) < 1e-9 and abs(ls - 10) < 1e-9
    v, extra = interp([229.0, 230.0, 231.0], [1e-14, 1e-15, 1e-16], 229.5)
    ok = ok and abs(v / (1e-14 / 10 ** 0.5) - 1) < 1e-9 and not extra
    try:
        classify(fake(230.0, sd, sp, s5, dshare_pair=0.9) | dict(vectors=[dict(x, delta=0.3) for x in fake(230.0, sd, sp, s5)["vectors"]]))
        ok = ok and False       # no vector above 0.5: classify must raise
    except ValueError:
        pass
    print(f"selftest{' --mutate' if mutate else ''}: {'pass' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    try:
        sys.exit(0 if tables(sys.argv[1]) else 1)
    except ValueError as e:
        print("classification failed:", e)
        sys.exit(1)
