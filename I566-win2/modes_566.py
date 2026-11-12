#!/usr/bin/env python3
"""#566: the last node near the horizon: the weakest equilibrated sigma at x_last = 0.96 ... 0.995 with its mode, where it peaks, and whether the node4 modes at 0.98 are the m_h modes at 0.96.
usage: python modes_566.py [--selftest]       (run from I566-win2 after the lanes; reads vec_*.npz (near_null_vec.py), veq_*.npz (near_null_eq_vec.py), nnv_*.log, eqv_*.log here, ../I559-win2 and ../I554-win2 logs for the reproducibility control)
Layouts 0.3, 0.4, 0.5, 0.6, x_last for x_last = 0.96 (old096), 0.97, 0.98 (old098), 0.99, 0.995.
Representations (all restricted to the layout-independent blocks p1, c0, m_h, a_h, Delta, 129 entries, as in #553):
  raw: the four weakest right singular vectors of J (near_null_vec.py);
  scaled: the four weakest of D_r J D_c (near_null_eq_vec.py), in the scaled unknowns;
  in z: D_c v of those, normalised (the equilibrated modes in the original unknowns).
Overlap of vector i at one layout with vector j at the next: |<r_i, r_j>| / (|r_i| |r_j|) on the restricted parts; modes are matched between layouts by the best total overlap over permutations of four. A match is called
ambiguous where the best overlap of a mode is below 0.7 or its second best is above 0.5 x its best. The retained norm is the share of the unit vector's squared norm that the restricted part carries.
The statement 'the node4 modes at 0.98 are the m_h modes at 0.96' is made only if, for the equilibrated modes in z (the representation in the original unknowns), the match of every mode from 0.96 to 0.98 is unambiguous
with overlap at least 0.9 and the retained norm of every vector at both layouts is at least 0.5; if a mode is ambiguous or retains less, the report says it cannot be said from these blocks, and the statement is not made
(the check of the issue). The same is stated separately for the raw modes.
--selftest: planted vectors (a known permutation, sign flips, noise 1e-3) are matched correctly and unambiguously with the statement allowed; planted vectors whose restricted part carries 20% of the norm do not allow it;
planted vectors with two nearly equal columns are called ambiguous."""
import itertools, math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "I553-win2"))
import crossing_553 as c  # noqa: E402
LAY = [(0.96, "old096"), (0.97, "last097"), (0.98, "old098"), (0.99, "last099"), (0.995, "last0995")]
BLK = ("p1", "c0", "m_h", "a_h", "Delta")


def retained(V, M, K):
    r = c.restricted(V, M, K)
    return np.sum(r ** 2, axis=0) / np.sum(V ** 2, axis=0)


def statement(O_ret_pairs):
    """O_ret_pairs: list of (O, retA, retB) from 0.96 to 0.98; returns (allowed, reason)"""
    O, ra, rb = O_ret_pairs
    bp, amb = c.match(O)
    if any(amb):
        return False, "the match is ambiguous for at least one mode"
    if min(O[i, bp[i]] for i in range(4)) < 0.9:
        return False, "a matched overlap is below 0.9"
    if min(ra.min(), rb.min()) < 0.5:
        return False, f"the retained norm is below 0.5 (min {min(ra.min(), rb.min()):.2f})"
    return True, "all four modes match unambiguously (overlap >= 0.9) and keep >= 0.5 of their norm in the common blocks"


def selftest():
    rng = np.random.default_rng(3)
    M, K = 32, 5
    L = 2 * M + 4 * M * K + 2 * M + 1
    rows = list(range(0, 2 * M)) + list(range(2 * M + 4 * M * K, 2 * M + 4 * M * K + 2 * M)) + [L - 1]
    base = rng.standard_normal((len(rows), 4))
    full = np.zeros((L, 4))
    full[rows, :] = np.linalg.qr(base)[0]
    ok = True
    perm = (1, 3, 0, 2)
    Va = full
    Vb = full[:, list(perm)] * np.array([1, -1, 1, -1]) + 1e-3 * rng.standard_normal((L, 4))
    Va, Vb = Va / np.linalg.norm(Va, axis=0), Vb / np.linalg.norm(Vb, axis=0)
    O = c.overlaps(c.restricted(Va, M, K), c.restricted(Vb, M, K))
    allowed, why = statement((O, retained(Va, M, K), retained(Vb, M, K)))
    bp, _ = c.match(O)
    good = allowed and all(perm[bp[i]] == i for i in range(4))
    print(f"planted permutation in the common blocks: statement allowed {allowed} ({why}); matched correctly {all(perm[bp[i]] == i for i in range(4))}: {'pass' if good else 'FAIL'}")
    ok = ok and good
    # planted: 80% of the norm outside the common blocks
    outside = [i for i in range(L) if i not in set(rows)]
    W = np.zeros((L, 4))
    W[rows, :] = 0.447 * np.linalg.qr(base)[0]
    W[outside[:16], :] = 0.894 * np.linalg.qr(rng.standard_normal((16, 4)))[0]
    Wb = W[:, list(perm)] + 1e-3 * rng.standard_normal((L, 4))
    W, Wb = W / np.linalg.norm(W, axis=0), Wb / np.linalg.norm(Wb, axis=0)
    O2 = c.overlaps(c.restricted(W, M, K), c.restricted(Wb, M, K))
    allowed2, why2 = statement((O2, retained(W, M, K), retained(Wb, M, K)))
    good = not allowed2
    print(f"planted vectors with 80% of the norm outside the common blocks: statement allowed {allowed2} ({why2}): {'pass' if good else 'FAIL'}")
    ok = ok and good
    # planted: two nearly equal columns -> ambiguous
    X = np.linalg.qr(base)[0]
    X[:, 1] = X[:, 0] * 0.99 + 0.01 * X[:, 1]
    X /= np.linalg.norm(X, axis=0)
    O3 = c.overlaps(X, X + 1e-3 * rng.standard_normal(X.shape))
    _, amb = c.match(O3)
    good = any(amb)
    print(f"planted vectors with two nearly equal columns: ambiguous {any(amb)}: {'pass' if good else 'FAIL'}")
    ok = ok and good
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


def main():
    data = {}
    for x, tag in LAY:
        pr, pe = os.path.join(HERE, f"vec_{tag}.npz"), os.path.join(HERE, f"veq_{tag}.npz")
        if not (os.path.exists(pr) and os.path.exists(pe)):
            continue
        zr, ze = np.load(pr), np.load(pe)
        M, K = int(zr["M"]), int(zr["K"])
        Vr = zr["V"]
        Vs = ze["V"]
        Vz = ze["dc"][:, None] * Vs
        Vz = Vz / np.linalg.norm(Vz, axis=0)
        data[x] = dict(M=M, K=K, raw=Vr, sc=Vs, z=Vz, sig_raw=zr["sigma"], sig_eq=ze["sigma"], dcol=float(zr["dcol"]))
    xs = sorted(data)
    print(f"{len(xs)} layouts with vectors: {', '.join(f'{x:g}' for x in xs)}")
    # block weights of the equilibrated (scaled) modes
    print("\nblock weights of the four equilibrated modes (scaled vectors, share of the squared norm)")
    print("| x_last | mode (sigma) | p1 | c0 | node0..node3 | node4.p | node4.m | node4.a | node4.c | m_h | a_h | Delta |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for x in xs:
        d = data[x]
        M, K = d["M"], d["K"]
        for i in range(4):
            v = d["sc"][:, i]
            sq = v ** 2
            p1, c0 = sq[:M].sum(), sq[M:2 * M].sum()
            nodes_ = [sq[2 * M + 4 * M * n + j * M: 2 * M + 4 * M * n + (j + 1) * M].sum() for n in range(K) for j in range(4)]
            first = sum(nodes_[:4 * (K - 1)])
            n4 = nodes_[4 * (K - 1):]
            o = 2 * M + 4 * M * K
            mh, ah, de = sq[o:o + M].sum(), sq[o + M:o + 2 * M].sum(), sq[-1]
            print(f"| {x:g} | {i + 1} ({d['sig_eq'][i]:.3e}) | {p1:.3f} | {c0:.3f} | {first:.3f} | {n4[0]:.3f} | {n4[1]:.3f} | {n4[2]:.3f} | {n4[3]:.3f} | {mh:.3f} | {ah:.3f} | {de:.3f} |")
    print("\nmode matches between neighbouring layouts (vector i at the lower x_last -> vector j at the higher; overlap; ambiguous?)")
    for rep, label in (("raw", "raw modes (near_null_vec.py)"), ("z", "equilibrated modes in z (D_c v)"), ("sc", "equilibrated modes, scaled")):
        print(f"\n{label}")
        for a, b in list(zip(xs, xs[1:])) + ([(0.96, 0.98)] if 0.96 in data and 0.98 in data else []):
            Da, Db = data[a], data[b]
            Ra, Rb = c.restricted(Da[rep], Da["M"], Da["K"]), c.restricted(Db[rep], Db["M"], Db["K"])
            O = c.overlaps(Ra, Rb)
            bp, amb = c.match(O)
            ra, rb = retained(Da[rep], Da["M"], Da["K"]), retained(Db[rep], Db["M"], Db["K"])
            print(f"  {a:g} -> {b:g}: " + ", ".join(f"{i + 1}->{bp[i] + 1} ({O[i, bp[i]]:.2f}{', ambiguous' if amb[i] else ''}; keeps {ra[i]:.2f}/{rb[bp[i]]:.2f})" for i in range(4)))
    if 0.96 in data and 0.98 in data:
        print("\nthe statement 'the node4 modes at 0.98 are the m_h modes at 0.96':")
        for rep, label in (("raw", "raw modes"), ("z", "equilibrated modes in z")):
            Da, Db = data[0.96], data[0.98]
            Ra, Rb = c.restricted(Da[rep], Da["M"], Da["K"]), c.restricted(Db[rep], Db["M"], Db["K"])
            allowed, why = statement((c.overlaps(Ra, Rb), retained(Da[rep], Da["M"], Da["K"]), retained(Db[rep], Db["M"], Db["K"])))
            print(f"  {label}: {'MADE' if allowed else 'NOT made'}: {why}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
