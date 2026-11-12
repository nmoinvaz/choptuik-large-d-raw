#!/usr/bin/env python3
"""#553: the finer last-node ladder across the Delta crossing, with mode tracking and the Delta column's norm.
usage: python crossing_553.py [--selftest] [--mutate]       (run from I553-win2 after lane_553.sh; reads vec_*.npz, nnv_*.log, eq_*.log here and ../I537-win2, ../I543-win2 logs for the reproducibility control)
Layouts 0.3, 0.4, 0.5, 0.6, x_last for x_last = 0.72 ... 0.80 (0.72, 0.74, 0.76, 0.80 are the existing ones, rerun with near_null_vec.py).
Modes: for each layout the four weakest right singular vectors v_i (octo-double inverse subspace iteration, near_null.py), restricted to the layout-independent blocks p1, c0, m_h, a_h, Delta (129 entries). The overlap of
vector i at one layout with vector j at the next is |<r_i, r_j>| / (|r_i| |r_j|); modes are matched between neighbouring layouts by the best total overlap over permutations of four (the matching is called ambiguous where the best
overlap of a mode is below 0.7 or its second best is above 0.5 x its best). The Delta mode is followed from x_last = 0.80 (pure Delta, delta share 1.00) down; the harmonic-3 pair is the two modes with delta share below 0.01 and the
closest sigma.
Acceptance of #553: (1) the x_last where the Delta mode's raw sigma meets the harmonic-3 pair's (mean of the two) is given to within 0.01: the bracketing layouts are 0.01 apart and the crossing is interpolated in ln sigma;
(2) the Delta mode's raw sigma at the layouts 0.76 to 0.80 equals ||J e_Delta||, the norm of the Delta column of the pinned Jacobian printed by near_null_vec.py, within 5%, and the check fails if not (--mutate scales the norm
by 1.1, which must make it fail); (3) renode checks pass and the --mutate sign control exits 1 once. Reproducibility control: near_null_vec.py's sigma on 0.72, 0.74, 0.76, 0.80 equal the logged near_null.py ones to 1e-3 relative.
--selftest: planted vectors (a known permutation, sign flips, noise 1e-3) are matched correctly, a planted pair of curves crosses where it should and the 5% test passes at 4% and fails at 6%."""
import itertools, math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OLD = {0.72: ("I537-win2", "last072", "nn_last072.log"), 0.74: ("I543-win2", "last074", "nn_last074.log"), 0.76: ("I543-win2", "last076", "nn_last076.log"), 0.80: ("I543-win2", "last080", "nn_last080.log")}
TAGS = {0.72: "old072", 0.73: "last073", 0.74: "old074", 0.75: "last075", 0.76: "old076", 0.77: "last077", 0.78: "last078", 0.79: "last079", 0.80: "old080"}
SIG = re.compile(r"^\s+sigma_(\d) ([0-9.e+-]+) \(converged", re.M)


def restricted(V, M, K):
    L = V.shape[0]
    idx = list(range(0, 2 * M)) + list(range(2 * M + 4 * M * K, 2 * M + 4 * M * K + 2 * M)) + [L - 1]
    return V[idx, :]


def overlaps(Ra, Rb):
    A = Ra / np.linalg.norm(Ra, axis=0)
    B = Rb / np.linalg.norm(Rb, axis=0)
    return np.abs(A.T @ B)


def match(O):
    best, bp = -1.0, None
    for p in itertools.permutations(range(O.shape[0])):
        s = sum(O[i, p[i]] for i in range(O.shape[0]))
        if s > best:
            best, bp = s, p
    amb = []
    for i in range(O.shape[0]):
        row = np.sort(O[i])[::-1]
        amb.append(bool(row[0] < 0.7 or row[1] > 0.5 * row[0]))
    return bp, amb


def crossing(xs, f):
    """x where f (ln sigma_D - ln sigma_H3) changes sign, by linear interpolation between the bracketing layouts; None if no sign change"""
    for a, b, fa, fb in zip(xs, xs[1:], f, f[1:]):
        if fa > 0 >= fb or fa < 0 <= fb:
            return a + (b - a) * fa / (fa - fb), (a, b)
    return None


def within(sigma, dcol, tol=0.05):
    return abs(sigma / dcol - 1) <= tol


def selftest():
    rng = np.random.default_rng(2)
    R = np.linalg.qr(rng.standard_normal((129, 4)))[0]
    perm = (2, 0, 3, 1)
    Rb = R[:, list(perm)] * np.array([1, -1, 1, -1]) + 1e-3 * rng.standard_normal((129, 4))
    O = overlaps(R, Rb)
    bp, amb = match(O)
    ok = all(O[i, bp[i]] > 0.99 for i in range(4)) and not any(amb)
    # the matched column of Rb for vector i of R is the column j with perm[j] == i
    ok = ok and all(perm[bp[i]] == i for i in range(4))
    xs = [0.72, 0.73, 0.74, 0.75, 0.76]
    fD = [math.log(v) for v in (5e-30, 4e-32, 3e-34, 3e-36, 6e-38)]
    fH = [math.log(3e-31)] * 5
    c = crossing(xs, [a - b for a, b in zip(fD, fH)])
    ok = ok and c is not None and abs(c[0] - 0.725833) < 1e-4 and c[1] == (0.72, 0.73)          # ln(5e-30 / 3e-31) = 2.813 and ln(4e-32 / 3e-31) = -2.015
    ok = ok and within(1.04, 1.0) and not within(1.06, 1.0)
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


def logged(path):
    return [float(m.group(2)) for m in SIG.finditer(open(path, encoding="utf-8").read())]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    mutate = "--mutate" in sys.argv
    lay, data = sorted(TAGS), {}
    for x in lay:
        tag = TAGS[x]
        p = os.path.join(HERE, f"vec_{tag}.npz")
        if not os.path.exists(p):
            continue
        z = np.load(p)
        M, K = int(z["M"]), int(z["K"])
        V, sig, dcol = z["V"], z["sigma"], float(z["dcol"]) * (1.1 if mutate else 1.0)
        data[x] = dict(R=restricted(V, M, K), sig=sig, share=V[-1, :] ** 2, dcol=dcol)
    xs = sorted(data)
    print(f"{len(xs)} layouts with vectors: {', '.join(f'{x:.2f}' for x in xs)}")
    print("\nreproducibility control: near_null_vec.py sigma against the logged near_null.py ones (relative difference)")
    rep = True
    for x, (d, tag, log) in OLD.items():
        if x in data:
            lg = logged(os.path.join(HERE, "..", d, log))
            rel = max(abs(a / b - 1) for a, b in zip(data[x]["sig"], lg))
            rep = rep and rel < 1e-3
            print(f"  x_last {x:.2f}: {rel:.1e}")
    print("  reproduced to 1e-3" if rep else "  NOT reproduced")
    # chains of matches from the top layout down
    print("\nmode matches between neighbouring layouts (vector i at the lower x_last -> vector j at the higher; overlap; ambiguous?)")
    chain = {}
    for a, b in zip(xs, xs[1:]):
        O = overlaps(data[a]["R"], data[b]["R"])
        bp, amb = match(O)
        chain[(a, b)] = bp
        print(f"  {a:.2f} -> {b:.2f}: " + ", ".join(f"{i + 1}->{bp[i] + 1} ({O[i, bp[i]]:.2f}{', ambiguous' if amb[i] else ''})" for i in range(4)))
    # follow the Delta mode downwards from the highest layout
    top = xs[-1]
    cur = int(np.argmax(data[top]["share"]))
    path = {top: cur}
    for a, b in reversed(list(zip(xs, xs[1:]))):
        bp = chain[(a, b)]
        cur = [i for i in range(4) if bp[i] == cur][0]
        path[a] = cur
    print("\nthe Delta mode (the vector with delta share 1.00 at the top layout) followed down, and the harmonic-3 pair")
    print("| x_last | Delta mode: index, raw sigma, delta share | harmonic-3 pair (mean sigma) | ln(sigma_D / sigma_H3) | ||J e_Delta|| | sigma_D / ||J e_Delta|| |\n|---|---|---|---|---|---|")
    fx, ff = [], []
    for x in xs:
        d = data[x]
        i = path[x]
        pairs = [(abs(math.log(d["sig"][p] / d["sig"][q])), p, q) for p in range(4) for q in range(p + 1, 4) if d["share"][p] < 0.01 and d["share"][q] < 0.01]
        _, p, q = min(pairs)
        sH = math.sqrt(d["sig"][p] * d["sig"][q])
        f = math.log(d["sig"][i] / sH)
        fx.append(x); ff.append(f)
        print(f"| {x:.2f} | {i + 1}, {d['sig'][i]:.3e}, {d['share'][i]:.2f} | sigma_{p + 1}, sigma_{q + 1} ({sH:.3e}) | {f:+.2f} | {d['dcol']:.3e} | {d['sig'][i] / d['dcol']:.3f} |")
    c = crossing(fx, ff)
    if c:
        print(f"\ncrossing of the Delta mode's raw sigma with the harmonic-3 pair's: x_last = {c[0]:.4f}, bracketed by the layouts {c[1][0]:.2f} and {c[1][1]:.2f} ({c[1][1] - c[1][0]:.2f} apart): {'within 0.01' if c[1][1] - c[1][0] <= 0.0101 else 'bracket wider than 0.01'}")
    else:
        print("\nno crossing in the range")
    chk = [(x, within(data[x]["sig"][path[x]], data[x]["dcol"])) for x in xs if x >= 0.76 - 1e-9]
    print("\nthe Delta mode's raw sigma against ||J e_Delta|| at the layouts 0.76 to 0.80 (within 5%): " + ", ".join(f"{x:.2f} {'yes' if ok else 'NO'}" for x, ok in chk))
    allok = rep and all(ok for _, ok in chk)
    print("Delta-column check: " + ("pass" if all(ok for _, ok in chk) else "FAIL") + ("  (mutated: the norm scaled by 1.1)" if mutate else ""))
    sys.exit(0 if allok else 1)
