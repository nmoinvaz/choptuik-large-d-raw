"""#1098: the rational rule of ladder_pade.py ([L/M] in 1/(D-2), the same selection as ladder_fit.select) on the real
ladder records, a second estimator beside ladder_fit.py's polynomial rule. Prints Delta_inf, h, s and the candidates
for M = 1, 2, 3.

    python3 pade_real.py LADDER_FOLDER... [--Ms=1,2,3]
"""
import sys

rest = sys.argv[1:]
sys.argv = [sys.argv[0], "pade"] + rest                  # ladder_fit reads its options from argv[2:]
import ladder_fit as LF  # noqa: E402
import ladder_pade as LP  # noqa: E402
import mpmath as mp  # noqa: E402

folders = [a for a in rest if not a.startswith("--")]
Ms = [int(v) for v in LF.args.get("Ms", "1,2,3").split(",")]
# recs_rat stores each value as a float of P(0) - lim, so lim must be close to Delta_inf for those floats to keep the
# digits: a 16-digit reference (not the answer: the result is lim + d at mpmath precision)
REF = mp.mpf(LF.args.get("ref", "1.6438937451253575"))
pts = LF.full_points(folders)
L_ = sorted(pts)
ys = [pts[d][0] for d in L_]
sig = [pts[d][1] for d in L_]
print("%d points, D %g to %g; sigma %.1e to %.1e" % (len(L_), L_[0], L_[-1], min(sig), max(sig)))
LF.VARS = {LP.VAR: LF.VARS[LP.VAR]}
for M in Ms:
    rr = LP.recs_rat(L_, ys, sig, M, REF)
    est = LF.select(rr, L_)
    if est is None:
        print("[L/%d]: no D0, nothing quoted (%d fits)" % (M, len(rr)))
        continue
    v = REF + mp.mpf(est["d"])
    cands = sorted(est["cands"])
    print("[L/%d]: Delta_inf %s, h %.2e, s %.2e, D0 %g, central L %d; candidates %s" % (
        M, mp.nstr(v, 25), est["h"], est["s"], est["D0"], est["K"],
        ", ".join("L %d lev %d: %s" % (c[2], c[1], mp.nstr(REF + mp.mpf(rr[c]["d"]), 25)) for c in cands)))
