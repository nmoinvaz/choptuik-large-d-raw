#!/usr/bin/env python3
"""Isolation test of lambda_1's V among M(lambda)'s singular values (#1025; follows svdtrack's misread control,
svdtrack_control_note.log). A sigma-fit of the V is unbiased only where the V is isolated: no other singular value
within a factor ISO, so no avoided crossing bends it. Does such a window exist near the root, and does a fit there
return the root?
SVD at lam1 -/+ GRID (0.01 ... 1e-6). Chains: right singular vectors linked between neighbouring offsets by mutual
best overlap with overlap^2 >= 0.5 (the triplet carrying most of the direction); a chain starts at every triplet
not reached by a link. A chain point is isolated when sigma >= SIGMIN (1e-14) sigma_max and the nearest other singular
value at that lambda is at least a factor ISO (3) away on both sides. V candidate (per side): a chain with >= 2
isolated points whose consecutive isolated points have a log-log slope of sigma against the offset in [0.8, 1.2].
Pair: a - and a + candidate whose vectors at their innermost isolated offsets overlap^2 >= 0.5. Root: weighted
(1/|g|) quadratic fit of g = -sigma (- side), +sigma (+ side) over the pair's isolated points; centre + the zero
nearest 0. Verdict 'isolated V' (pass): a pair whose root lies within tol (1e-6) of the centre; else 'fail' with the
reason. Exit 0 pass, 3 fail, 1 error.
Columns: per pair point, |V_f^T v|^2 against the floor subspaces V_f (sigma < 1e-14 sigma_max) at centre -/+ 0.01, and
the centre-odd share of |v|^2; s' per side; the expected root precision, rounding (2e-16) / s'.
--mutate=shift centres the grid and the criterion at lam1 + 0.02 (must fail).
planted: synthetic M (svdtrack.planted_M): a regular V (slope 1e-8), the V crossing coupled regular pairs as at
D 13 (slope 2.5e-6), a V buried in the floor (3e-14), and the crossing case with --mutate=shift; exit 0 when they read
pass, pass, fail, fail. The truth is det M's zero: with the couplings it sits at 2.000337, not at the V's own 2.0.
usage: svdiso.py STATE D kc lam1 [--N 150] [--tol 1e-6] [--mutate=shift] [--out FILE]
       svdiso.py planted"""
import argparse, json, os, sys, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svdtrack import planted_M

GRID = [0.01, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5, 3e-6, 1e-6]
ISO, SIGMIN, MAJ = 3.0, 1e-14, 0.5


def svd_pt(M, N):
    U, s, Vh = np.linalg.svd(M)
    sr = s[::-1] / s[0]
    return dict(smax=float(s[0]), sall=sr, s=sr[:N], V=Vh[::-1][:N].T.copy(), k14=int(np.sum(sr < 1e-14)),
                k12=int(np.sum(sr < 1e-12)))


def chains(pts):
    N = pts[0]["V"].shape[1]
    links = []
    for a, b in zip(pts[:-1], pts[1:]):
        O = np.abs(a["V"].T @ b["V"])
        jb, ia = O.argmax(axis=1), O.argmax(axis=0)
        links.append({i: int(jb[i]) for i in range(N) if ia[jb[i]] == i and O[i, jb[i]] ** 2 >= MAJ})
    out = []
    for k in range(len(pts)):
        reached = set(links[k - 1].values()) if k else set()
        for i in (j for j in range(N) if j not in reached):
            seq, cur = [None] * k + [i], i
            for L in links[k:]:
                cur = L.get(cur) if cur is not None else None
                seq.append(cur)
            out.append(seq)
    return out


def isolated(p, j):
    s, sa = p["sall"][j], p["sall"]
    if s < SIGMIN or j + 1 >= len(sa):
        return False
    return (j == 0 or s >= ISO * sa[j - 1]) and ISO * s <= sa[j + 1]


def analyse(pt, centre, tol, nodd, log):
    side = {}
    for sg in (-1, 1):
        P = [pt[sg * d] for d in GRID]
        cands = []
        for seq in chains(P):
            iso = [(k, j) for k, j in enumerate(seq) if j is not None and isolated(P[k], j)]
            if len(iso) < 2:
                continue
            sl = [np.log(P[a]["s"][ja] / P[b]["s"][jb]) / np.log(GRID[a] / GRID[b]) for (a, ja), (b, jb) in zip(iso[:-1], iso[1:])]
            if all(0.8 <= x <= 1.2 for x in sl):
                cands.append(dict(iso=iso, slopes=[float(x) for x in sl],
                                  pts=[(sg * GRID[k], float(P[k]["s"][j])) for k, j in iso]))
        side[sg] = cands
        log(f"side {'+' if sg > 0 else '-'}: {len(cands)} V candidates with >= 2 isolated points and slopes in [0.8, 1.2]"
            + "".join(f"\n    isolated at {[f'{d:+g}' for d, _ in c['pts']]}, sigma {[f'{s:.3e}' for _, s in c['pts']]}, "
                      f"slopes {[round(x, 3) for x in c['slopes']]}" for c in cands[:6]))
    Wm, Wp = (pt[d]["V"][:, :pt[d]["k14"]] for d in (-0.01, 0.01))
    pairs = []
    for cm in side[-1]:
        for cp in side[1]:
            (km, jm), (kp, jp) = cm["iso"][-1], cp["iso"][-1]
            o = float(abs(pt[-GRID[km]]["V"][:, jm] @ pt[GRID[kp]]["V"][:, jp]))
            if o * o < MAJ:
                continue
            pts_ = sorted(cm["pts"] + cp["pts"])
            d = np.array([x for x, _ in pts_]); g = np.array([np.sign(x) * s for x, s in pts_])
            r = np.roots(np.polyfit(d, g, 2, w=1 / np.abs(g)))
            r = r[np.isreal(r)].real
            root = float(centre + r[np.argmin(abs(r))]) if len(r) else None
            sl = {sg: float(np.median([s / abs(x) for x, s in c["pts"]])) for sg, c in ((-1, cm), (1, cp))}
            w = {}
            for sg, c in ((-1, cm), (1, cp)):
                for k, j in c["iso"]:
                    v = pt[sg * GRID[k]]["V"][:, j]
                    w[f"{sg * GRID[k]:+g}"] = dict(wA=float(np.sum((Wm.T @ v) ** 2)), wB=float(np.sum((Wp.T @ v) ** 2)),
                                                   centre_odd=float(np.sum(v[:nodd] ** 2)))
            pairs.append(dict(join_overlap=o, points=pts_, root=root, minus_centre=(root - centre) if root else None,
                              slope_minus=sl[-1], slope_plus=sl[1], precision=2e-16 / min(sl.values()),
                              within=bool(root is not None and abs(root - centre) <= tol), weights=w))
    for p in pairs:
        log(f"pair (overlap {p['join_overlap']:.3f}): {len(p['points'])} isolated points; s' {p['slope_minus']:.3e} (-), "
            f"{p['slope_plus']:.3e} (+); root {p['root']!r}, minus centre {p['minus_centre']:+.3e} (tol {tol:g}: "
            f"{p['within']}); expected precision {p['precision']:.1e}")
        for dd, x in p["weights"].items():
            log(f"    at {dd}: |V_f(-0.01)^T v|^2 {x['wA']:.3e}, |V_f(+0.01)^T v|^2 {x['wB']:.3e}, centre-odd share {x['centre_odd']:.4f}")
    if any(p["within"] for p in pairs):
        verdict, why = "isolated V", ""
    elif pairs:
        verdict, why = "fail", "pairs found but no root within tol"
    elif side[-1] or side[1]:
        verdict, why = "fail", "V candidates on one side only, or not joined"
    else:
        verdict, why = "fail", "no isolated V candidate"
    return dict(verdict=verdict, reason=why, pairs=pairs, n_cand_minus=len(side[-1]), n_cand_plus=len(side[1]))


def main_state(argv):
    sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
    from dss_ell import DSSEll, NODES_STD
    ap = argparse.ArgumentParser()
    ap.add_argument("state"); ap.add_argument("D", type=float); ap.add_argument("kc", type=int)
    ap.add_argument("lam1", type=float); ap.add_argument("--N", type=int, default=150)
    ap.add_argument("--tol", type=float, default=1e-6); ap.add_argument("--mutate", default=None)
    ap.add_argument("--out", default=None)
    o = ap.parse_args(argv)
    centre = o.lam1 + 0.02 if o.mutate == "shift" else o.lam1
    z = np.load(o.state)
    S = DSSEll(kc=o.kc, nodes=NODES_STD, n=o.D - 2, ell=1, Delta_ref=z[-1], Ks=30, u0=0.04)
    S.freeze_from(z, 0.7)
    nodd = S.layout()[0][0]
    log = lambda m: print(m, flush=True)
    log(f"svdiso D {o.D} k_c {o.kc} lam1 {o.lam1!r} centre {centre!r} (mutate {o.mutate}); N {o.N}, tol {o.tol:g}, "
        f"ISO {ISO:g}, SIGMIN {SIGMIN:g}; centre-odd columns {nodd}")
    t0, pt = time.time(), {}
    for d in [s * g for g in GRID for s in (-1, 1)]:
        t1 = time.time()
        with np.errstate(all="ignore"):
            M = S.mode_matrix(z, centre + d)
        pt[d] = p = svd_pt(M, o.N)
        log(f"lam {centre + d:.9f} (offset {d:+g}): below 1e-14: {p['k14']}, below 1e-12: {p['k12']}, smallest "
            f"{p['s'][0]:.2e}, kept top {p['s'][-1]:.2e}, {time.time() - t1:.0f} s")
    rec = analyse(pt, centre, o.tol, nodd, log)
    rec.update(D=o.D, kc=o.kc, state=os.path.basename(o.state), lam1=o.lam1, centre=centre, mutate=o.mutate, tol=o.tol,
               spectra={f"{d:+g}": [float(v) for v in p["s"][:80]] for d, p in sorted(pt.items())},
               seconds=round(time.time() - t0))
    log(f"VERDICT D {o.D} k_c {o.kc} (mutate {o.mutate}): {rec['verdict']} {rec['reason']}")
    out = o.out or os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "svdiso_1025.jsonl")
    open(out, "a").write(json.dumps(rec) + "\n")
    return 0 if rec["verdict"] == "isolated V" else 3


def planted_root(s1, c, cross):
    """zero of det of svdtrack.planted_M: the V's 7x7 block [[g, k^T], [k, diag p]] has det = prod(p) (g - k^T p^-1 k),
    so with the couplings the root is where g = sum k^2 / p (constants as in planted_M)"""
    if not cross:
        return 2.0
    kap = np.array([2e-9, 2e-9, 1e-9, 1e-9, 2e-10, 2e-10]); p = np.array([1.2e-8, 1.22e-8, 1.4e-8, 1.41e-8, 2.05e-9, 2.06e-9])
    r = np.roots([c, s1, -np.sum(kap ** 2 / p)])
    r = r[np.isreal(r)].real
    return 2.0 + float(r[np.argmin(abs(r))])


def main_planted():
    ok = True
    for name, s1, c, cross, mut, want in (("regular V, slope 1e-8", 1e-8, 2e-8, False, None, "pass"),
                                          ("V crossing coupled regular pairs (D 13-like)", 2.5e-6, 5e-6, True, None, "pass"),
                                          ("V buried in the floor", 3e-14, 6e-14, False, None, "fail"),
                                          ("crossing case, --mutate=shift", 2.5e-6, 5e-6, True, "shift", "fail")):
        centre = planted_root(s1, c, cross) + (0.02 if mut else 0.0)
        print(f"planted {name}: true root {planted_root(s1, c, cross)!r}, grid centre {centre!r}", flush=True)
        pt = {d: svd_pt(planted_M(centre + d, s1, c, cross=cross), 150) for d in [s * g for g in GRID for s in (-1, 1)]}
        rec = analyse(pt, centre, 1e-6, 50, lambda m: print("  " + m))
        good = (rec["verdict"] == "isolated V") == (want == "pass")
        ok &= good
        print(f"planted {name}: {rec['verdict']} {rec['reason']}, wanted {want}: {'OK' if good else 'BAD'}", flush=True)
    print(f"planted: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main_planted() if sys.argv[1:2] == ["planted"] else main_state(sys.argv[1:]))
