"""#1025 (d) and the orientation bookkeeping (d18_criteria.log, the coordinator's input after (a)): the scans of one state
merged, every robust sign change with its orientation (the sign below the root to the sign above it), bracket and estimator
range (d185_scan_read.py), the ln|det| minima without a sign change (d18c_read.py), and the repeated points' agreement
(same sign, ln|det| within 1e-6). With --above X: a robust change above X is where the plus-to-minus root went (reading d1);
none in the window above X is reading d2.
usage: d18d_read.py D WT_MATTER SCAN.jsonl[,SCAN2.jsonl,...] [--above=1.90]   |   d18d_read.py selftest [--mutate=orient]"""
import sys, os, json
import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
ABOVE = next((float(a.split("=", 1)[1]) for a in sys.argv if a.startswith("--above=")), None)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
sys.argv = [sys.argv[0], "x"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d185_scan_read as rd
import d18c_read as rc

sg = lambda s: "+" if s > 0 else "-"


def merge(rows):
    S, rep = {}, []
    for r in rows:
        k = round(r["lam"], 6)
        if k in S:
            rep.append((k, S[k]["sign"] == r["sign"] and abs(S[k]["ln"] - r["ln"]) <= 1e-6, S[k]["ln"] - r["ln"]))
            continue
        S[k] = r
    return [S[k] for k in sorted(S)], rep


def read(S, rep, above=None, out=print, l0=None):
    rob, non = rd.changes(S)
    mins = rc.minima(S, rob + non)
    out(f"points {len(S)}, {S[0]['lam']:.2f} to {S[-1]['lam']:.2f}; not noise-robust: {[r['lam'] for r in S if not r['noise_robust']] or 'none'}")
    out("signs: " + " ".join("%.2f%s" % (r["lam"], sg(r["sign"])) for r in S))
    out(f"repeated points: {[(k, 'agree' if a else 'DISAGREE', f'{d:+.1e}') for k, a, d in rep] or 'none'}")
    by = {round(r["lam"], 2): r for r in S}
    roots = []
    for c in rob:
        o = f"{sg(by[round(c['br'][0], 2)]['sign'])} to {sg(by[round(c['br'][1], 2)]['sign'])}"
        if MUT == "orient":                                  # control: the orientation is read reversed
            o = o[::-1]
        roots.append(dict(c, orient=o))
        d = f", delta {c['lin'] - l0:+.6f}" if l0 is not None else ""
        out(f"  root in ({c['br'][0]:.2f}, {c['br'][1]:.2f}), {o}: det-linear {c['lin']:.6f}, range [{c['lo']:.6f}, {c['hi']:.6f}]{d}")
    out(f"robust sign changes: {len(rob)}; touching a non-robust point (not counted): {[c['br'] for c in non] or 'none'}")
    free = [m for m in mins if not m["beside"]]
    out(f"ln|det| local minima without a sign change: {[(round(m['lam'], 2), round(m['depth'], 4)) for m in free] or 'none'}")
    v = None
    if above is not None:
        up = [x for x in roots if x["br"][0] >= above - 1e-9]
        nu = [c for c in non if c["br"][0] >= above - 1e-9]
        if up:
            v = "d1"
            out(f"reading (d1): {len(up)} robust change(s) above {above:.2f}: {[(x['br'], x['orient']) for x in up]}; the first is where the "
                f"plus-to-minus root went")
        elif nu:
            v = "unresolved"
            out(f"no reading: a change above {above:.2f} touches a non-robust point ({[c['br'] for c in nu]}); the coordinator rules")
        else:
            v = "d2"
            out(f"reading (d2): no change from {above:.2f} to {S[-1]['lam']:.2f}: the plus-to-minus root is not in that range")
    if any(not a for _, a, _ in rep):
        v = "repeat disagrees"
        out("STOP-level: a repeated point disagrees with its earlier evaluation; no reading")
    return dict(v=v, roots=roots)


def selftest():
    q = lambda *s: None
    lo = [round(1.55 + 0.01 * i, 2) for i in range(36)]; hi = [round(1.90 + 0.01 * i, 2) for i in range(21)]
    ok = []
    neg = lambda T: [dict(r, sign=-r["sign"]) for r in T]     # the real data's convention: - below the lowest root
    A = neg(rc.planted(lo, (1.677, 1.9634))); B = neg(rc.planted(hi, (1.677, 1.9634)))
    S, rep = merge(A + B)
    r = read(S, rep, 1.90, q)
    ok.append(("a root at 1.9634 above 1.90: d1, orientations - to + and + to -",
               r["v"] == "d1" and [x["orient"] for x in r["roots"]] == ["- to +", "+ to -"]))
    S, rep = merge(neg(rc.planted(lo, (1.677,))) + neg(rc.planted(hi, (1.677,))))
    r = read(S, rep, 1.90, q)
    ok.append(("no root above 1.90: d2", r["v"] == "d2" and len(r["roots"]) == 1))
    B2 = neg(rc.planted(hi, (1.677, 1.9634))); B2[0] = dict(B2[0], ln=B2[0]["ln"] + 1e-3)
    S, rep = merge(A + B2)
    r = read(S, rep, 1.90, q)
    ok.append(("a repeated point off by 1e-3 in ln|det|: no reading", r["v"] == "repeat disagrees"))
    for name, good in ok:
        print(f"planted: {name}: {'PASS' if good else 'FAIL'}")
    allok = all(gd for _, gd in ok)
    print(f"selftest: {'PASS' if allok else 'FAIL'}{f' [mutate {MUT}]' if MUT else ''}")
    return 0 if allok else 1


if __name__ == "__main__":
    if args[0] == "selftest":
        sys.exit(selftest())
    D, wt, files = float(args[0]), args[1], args[2].split(",")
    sys.path.insert(0, wt)
    import ell_delta
    l0, l0e = ell_delta.lam0_at(D, *ell_delta.lam0_table())
    rows = []
    for f in files:
        for l in open(f):
            r = json.loads(l)
            assert r["D"] == D, f"{f}: D {r['D']} is not {D}"
            rows.append(r)
    S, rep = merge(rows)
    print(f"D {D:g}, files {[os.path.basename(f) for f in files]}; lambda_0 {l0:.10f} (error {l0e:.1e})")
    read(S, rep, ABOVE, l0=l0)
    fc = [(a["lam"], b["lam"]) for a, b in zip(S, S[1:]) if a["f64_sign"] != b["f64_sign"]]
    print(f"float64 sign changes: {len(fc)} in {fc}; float64 differs from the hybrid at {len([x for x in S if x['f64_sign'] != x['sign']])} "
          f"of {len(S)} points")
