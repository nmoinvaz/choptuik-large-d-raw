#!/usr/bin/env python3
"""Singular-value track of M(lambda) near a root (#1025). Does lambda_1's zero sit in a regular singular value that
rises out of M's rounding floor (sigma = |g(lambda)|, g' != 0), or inside the floor?
SVD of M at lam1 and lam1 -/+ (0.03, 0.01, 0.003, 0.001). On each side the right singular vectors of the smallest N
triplets are continued from 0.03 inward by mutual best overlap (>= 0.9); a chain is a V candidate if its sigma falls
with the offset (log slope >= 0.5 from 0.03 to 0.01). A + candidate and a - candidate are joined when their vectors
at the innermost offset both reach overlap >= 0.9. For a joined pair g = -sigma on the - side and +sigma on the + side;
quadratic fits of g over (-/+0.03, -/+0.01) and over (-/+0.01, -/+0.003) give two predicted roots.
Verdict 'regular': a pair with sigma >= cut sigma_max at -/+0.01 whose two predicted roots lie within tol of lam1;
'inside the floor': no V candidate on either side; 'mixed' otherwise. Exit 0 regular, 3 not regular, 1 error.
Columns for each pair: |V_f^T v|^2 against the floor subspaces V_f (sigma < 1e-14 sigma_max) at lam1 -/+ 0.01
(the lift's references in test (a); zero by orthogonality at its own lambda when v is above the cut), and the
centre-odd share of |v|^2. --track=majority links on overlap^2 >= 0.5 (the triplet carrying most of the
direction) instead of overlap >= 0.9, so a V keeps its chain through an avoided crossing with a regular pair. --extra d1,d2,..: more + offsets, checked for a chain with a dip (sigma below half its
neighbours') at the middle one. --mutate=shift centres the grid and the criterion at lam1 + 0.02 (must not read
regular). planted: the same detector on synthetic M(lambda) with a known V (regular), a V buried in the floor and the
shift mutation; exit 0 when all three read as they must.
usage: svdtrack.py STATE D kc lam1 [--extra 0.0124,0.0144,0.0164] [--N 150] [--cut 1.5e-14] [--tol 1e-4]
                   [--mutate=shift] [--out FILE]
       svdtrack.py planted"""
import json, os, sys, time
import numpy as np

CORE = [0.03, 0.01, 0.003, 0.001]
OVL = 0.9
TRACK = "0.9"                          # "majority": a link needs overlap^2 >= 0.5 instead of overlap >= 0.9


def linked(o):
    return o * o >= 0.5 if TRACK == "majority" else o >= OVL


def svd_small(M, N):
    U, s, Vh = np.linalg.svd(M)
    return dict(smax=float(s[0]), s=s[::-1][:N] / s[0], V=Vh[::-1][:N].T.copy(),
                k14=int(np.sum(s < 1e-14 * s[0])), k12=int(np.sum(s < 1e-12 * s[0])))


def follow(pts):
    """chains of triplet indices through pts (outermost first) by mutual best overlap >= OVL; None after a break"""
    N = pts[0]["V"].shape[1]
    links = []
    for a, b in zip(pts[:-1], pts[1:]):
        O = np.abs(a["V"].T @ b["V"])
        jb, ia = O.argmax(axis=1), O.argmax(axis=0)
        links.append({i: int(jb[i]) for i in range(N) if ia[jb[i]] == i and linked(O[i, jb[i]])})
    out = []
    for i in range(N):
        seq, cur = [i], i
        for L in links:
            cur = L.get(cur) if cur is not None else None
            seq.append(cur)
        out.append(seq)
    return out


def analyse(pt, centre, cut, tol, nodd, extra, log):
    """pt: {signed offset: svd dict}; returns the verdict record"""
    side = {}
    for sg in (-1, 1):
        P = [pt[sg * d] for d in CORE]
        cands = []
        for seq in follow(P):
            if seq[1] is None:
                continue
            sl = np.log(P[0]["s"][seq[0]] / P[1]["s"][seq[1]]) / np.log(CORE[0] / CORE[1])
            if sl >= 0.5:
                cands.append(dict(seq=seq, slope=float(sl),
                                  sig=[float(P[k]["s"][j]) if j is not None else None for k, j in enumerate(seq)]))
        side[sg] = cands
        log(f"side {'+' if sg > 0 else '-'}: {len(cands)} V candidates (log slope >= 0.5 from 0.03 to 0.01): "
            + "; ".join(f"slope {c['slope']:.2f} sigma " + ",".join(f"{v:.2e}" if v else "-" for v in c["sig"])
                        for c in cands[:8]))
    WA, WB = (pt[d]["V"][:, :pt[d]["k14"]] for d in (-0.01, 0.01))
    pairs = []
    for cm in side[-1]:
        for cp in side[1]:
            k = max(k for k in range(4) if cm["seq"][k] is not None and cp["seq"][k] is not None)
            if k < 2:
                continue
            o = float(abs(pt[-CORE[k]]["V"][:, cm["seq"][k]] @ pt[CORE[k]]["V"][:, cp["seq"][k]]))
            if not linked(o):
                continue
            dd = np.array([-0.03, -0.01, -0.003, 0.003, 0.01, 0.03])
            g = np.array([-cm["sig"][0], -cm["sig"][1], -cm["sig"][2], cp["sig"][2], cp["sig"][1], cp["sig"][0]])

            def root(ix):
                r = np.roots(np.polyfit(dd[ix], g[ix], 2))
                r = r[np.isreal(r)].real
                return float(centre + r[np.argmin(abs(r))]) if len(r) else None
            ro, ri = root([0, 1, 4, 5]), root([1, 2, 3, 4])
            vs = {sg * CORE[k2]: pt[sg * CORE[k2]]["V"][:, j]
                  for sg, ch in ((-1, cm), (1, cp)) for k2, j in enumerate(ch["seq"]) if j is not None}
            w = {f"{d:+g}": dict(wA=float(np.sum((WA.T @ v) ** 2)), wB=float(np.sum((WB.T @ v) ** 2)),
                                 centre_odd=float(np.sum(v[:nodd] ** 2))) for d, v in sorted(vs.items())}
            pairs.append(dict(join_offset=CORE[k], join_overlap=o, sig_minus=cm["sig"], sig_plus=cp["sig"],
                              slope_ratio=float(cp["sig"][1] / cm["sig"][1]), root_outer=ro, root_inner=ri,
                              above_cut=bool(min(cm["sig"][1], cp["sig"][1]) >= cut),
                              within=bool(ro is not None and ri is not None and abs(ro - centre) <= tol
                                          and abs(ri - centre) <= tol), weights=w))
    for p in pairs:
        log(f"pair (joined at {p['join_offset']}, overlap {p['join_overlap']:.3f}): sigma at -0.01 {p['sig_minus'][1]:.3e}, "
            f"+0.01 {p['sig_plus'][1]:.3e} (cut {cut:g}: {p['above_cut']}); roots outer {p['root_outer']}, inner "
            f"{p['root_inner']} (within {tol:g} of {centre}: {p['within']})")
        for d, x in p["weights"].items():
            log(f"    at {d}: |V_f(-0.01)^T v|^2 {x['wA']:.3e}, |V_f(+0.01)^T v|^2 {x['wB']:.3e}, centre-odd share {x['centre_odd']:.4f}")
    rec = dict(pairs=pairs, n_cand_minus=len(side[-1]), n_cand_plus=len(side[1]))
    if extra:
        ex = sorted(extra)
        P = [pt[CORE[0]]] + [pt[d] for d in ex[::-1]] + [pt[CORE[1]]]
        mid = len(ex) // 2 + 1
        dips = []
        for seq in follow(P):
            if None in seq[mid - 1:mid + 2]:
                continue
            s3 = [P[mid + j]["s"][seq[mid + j]] for j in (-1, 0, 1)]
            if s3[1] < 0.5 * min(s3[0], s3[2]):
                dips.append([float(v) for v in s3])
        rec["dips_at"] = ex[len(ex) // 2]
        rec["dips"] = dips
        log(f"chains with a dip at +{ex[len(ex) // 2]} (lambda {centre + ex[len(ex) // 2]:.6f}): {len(dips)} {dips[:5]}")
    good = [p for p in pairs if p["above_cut"] and p["within"]]
    rec["verdict"] = "regular" if good else ("inside the floor" if not side[-1] and not side[1] else "mixed")
    return rec


def main_state(a):
    sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
    from dss_ell import DSSEll, NODES_STD
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("state"); ap.add_argument("D", type=float); ap.add_argument("kc", type=int)
    ap.add_argument("lam1", type=float); ap.add_argument("--extra", default=None)
    ap.add_argument("--N", type=int, default=150); ap.add_argument("--cut", type=float, default=1.5e-14)
    ap.add_argument("--tol", type=float, default=1e-4); ap.add_argument("--mutate", default=None)
    ap.add_argument("--out", default=None)
    o = ap.parse_args(a)
    st, D, kc, lam1, N, cut, tol, mut = o.state, o.D, o.kc, o.lam1, o.N, o.cut, o.tol, o.mutate
    extra = [float(v) for v in o.extra.split(",")] if o.extra else []
    centre = lam1 + 0.02 if mut == "shift" else lam1
    z = np.load(st)
    S = DSSEll(kc=kc, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=30, u0=0.04)
    S.freeze_from(z, 0.7)
    t0 = time.time()
    log = lambda m: print(m, flush=True)
    log(f"svdtrack D {D} k_c {kc} lam1 {lam1} centre {centre} (mutate {mut}); N {N}, cut {cut:g}, tol {tol:g}; "
        f"n_odd {S.n_odd}, centre-odd columns {S.layout()[0][0]}")
    pt = {}
    for d in [0.0] + [s * c for c in CORE for s in (-1, 1)] + extra:
        t1 = time.time()
        with np.errstate(all="ignore"):
            M = S.mode_matrix(z, centre + d)
        pt[d] = svd_small(M, N)
        p = pt[d]
        log(f"lam {centre + d:.9f} (offset {d:+g}): sigma_max {p['smax']:.4e}, below 1e-14: {p['k14']}, below 1e-12: "
            f"{p['k12']}, smallest {p['s'][0]:.2e} {p['s'][1]:.2e} {p['s'][2]:.2e}, {time.time() - t1:.0f} s")
    rec = analyse(pt, centre, cut, tol, S.layout()[0][0], extra, log)
    rec.update(D=D, kc=kc, state=os.path.basename(st), lam1=lam1, centre=centre, mutate=mut, cut=cut, tol=tol,
               points={f"{d:+g}": dict(lam=centre + d, k14=p["k14"], k12=p["k12"], smax=p["smax"],
                                       s=[float(v) for v in p["s"][:60]]) for d, p in sorted(pt.items())},
               seconds=round(time.time() - t0))
    log(f"VERDICT D {D} k_c {kc} (mutate {mut}): {rec['verdict']}")
    out = o.out or os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "svdtrack_1025.jsonl")
    open(out, "a").write(json.dumps(rec) + "\n")
    return 0 if rec["verdict"] == "regular" else 3


def planted_M(lam, s1, c, lam1=2.0, n=400, K=40, cross=False):
    g = np.random.default_rng(5)
    Q0L, Q0R = (np.linalg.qr(g.standard_normal((n, n)))[0] for _ in range(2))
    AL, AR = (0.3 * (B - B.T) / np.sqrt(n) for B in (g.standard_normal((n, n)) for _ in range(2)))
    from scipy.linalg import expm
    QL, QR = expm((lam - lam1) * AL) @ Q0L, expm((lam - lam1) * AR) @ Q0R
    pairs = [1.2e-8, 1.22e-8, 1.4e-8, 1.41e-8, 2.05e-9, 2.06e-9] if cross else []
    reg = np.logspace(0, -7 if cross else -9, n - K - 1 - len(pairs))
    sig = np.concatenate([reg, pairs, [s1 * (lam - lam1) + c * (lam - lam1) ** 2],
                          np.logspace(-15, -17.5, K) * (1 + 0.3 * (lam - lam1))])
    C = np.diag(sig)
    if cross:                                          # the V couples to the pairs on its path: avoided crossings
        iv = n - K - 1
        for j, kap in zip(range(iv - 6, iv), (2e-9, 2e-9, 1e-9, 1e-9, 2e-10, 2e-10)):
            C[iv, j] = C[j, iv] = kap
    E = 1e-16 * np.random.default_rng(int(abs(lam) * 1e9) % 2 ** 32).standard_normal((n, n)) / np.sqrt(n)
    return QL @ C @ QR.T + E


def main_planted():
    ok = True
    print(f"planted, tracking rule {TRACK}", flush=True)
    for name, s1, c, mut, cross, want in (("regular V", 1e-10, 2e-10, None, False, "regular"),
                                          ("V buried in the floor", 3e-14, 6e-14, None, False, "not"),
                                          ("regular V, --mutate=shift", 1e-10, 2e-10, "shift", False, "not"),
                                          ("V crossing coupled regular pairs (as at D 13)", 2.5e-6, 5e-6, None, True,
                                           "regular")):
        centre = 2.0 + (0.02 if mut else 0.0)
        pt = {d: svd_small(planted_M(centre + d, s1, c, cross=cross), 150)
              for d in [0.0] + [s * x for x in CORE for s in (-1, 1)]}
        rec = analyse(pt, centre, 1.5e-14, 1e-4, 50, [], lambda m: print("  " + m))
        good = (rec["verdict"] == "regular") == (want == "regular")
        ok &= good
        print(f"planted {name}: verdict {rec['verdict']}, wanted {want}: {'OK' if good else 'BAD'}", flush=True)
    print(f"planted: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--track=majority" in sys.argv:
        TRACK = "majority"
        sys.argv.remove("--track=majority")
    sys.exit(main_planted() if sys.argv[1:2] == ["planted"] else main_state(sys.argv[1:]))
