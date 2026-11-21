"""#1025 (e) (d18_criteria.log, the coordinator's ruling after (d)): the scans of one state merged (d18d_read.merge: a repeated point
must agree), and in the window [LO, HI] the robust sign changes with their orientation. One plus-to-minus change and nothing else in
the window places the rising eigenvalue: bracket, estimator range (d185_scan_read.changes, information) and delta against lambda_0 at
that D. None: not placed. More than one change, or a minus-to-plus one: all listed, the coordinator rules. A repeat that disagrees:
no reading. A change touching a non-robust point is not counted.
usage: d18e_read.py D WT_MATTER SCAN.jsonl[,...] LO HI   |   d18e_read.py selftest [--mutate=orient]"""
import sys, os, json
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
sys.argv = [sys.argv[0], "x"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d185_scan_read as rd
import d18c_read as rc
import d18d_read as dr

sg = lambda s: "+" if s > 0 else "-"
WANT = "- to +" if MUT == "orient" else "+ to -"                 # control: the rising root read with the wrong orientation


def read(S, rep, lo, hi, l0=None, l0e=0.0, out=print):
    rob, non = rd.changes(S)
    by = {round(r["lam"], 2): r for r in S}
    inw = lambda c: c["br"][0] >= lo - 1e-9 and c["br"][1] <= hi + 1e-9
    W = [r for r in S if lo - 1e-9 <= r["lam"] <= hi + 1e-9]
    out(f"window {lo:.2f}-{hi:.2f}: {len(W)} points; not noise-robust: {[r['lam'] for r in W if not r['noise_robust']] or 'none'}")
    out("signs: " + " ".join("%.2f%s" % (r["lam"], sg(r["sign"])) for r in W))
    out(f"repeated points: {[(k, 'agree' if a else 'DISAGREE', f'{d:+.1e}') for k, a, d in rep] or 'none'}")
    cs = []
    for c in rob:
        if inw(c):
            o = f"{sg(by[round(c['br'][0], 2)]['sign'])} to {sg(by[round(c['br'][1], 2)]['sign'])}"
            cs.append(dict(c, orient=o))
            dl = f", delta [{c['lo'] - l0:+.6f}, {c['hi'] - l0:+.6f}] (lambda_0 {l0:.10f}, error {l0e:.1e})" if l0 is not None else ""
            out(f"  change in ({c['br'][0]:.2f}, {c['br'][1]:.2f}), {o}: det-linear {c['lin']:.6f}, range [{c['lo']:.6f}, {c['hi']:.6f}]{dl}")
    nw = [c["br"] for c in non if inw(c)]
    out(f"robust changes in the window: {len(cs)}; touching a non-robust point (not counted): {nw or 'none'}")
    free = [m for m in rc.minima(W, [c for c in rob + non if inw(c)]) if not m["beside"]]
    out(f"ln|det| local minima without a sign change in the window: {[(round(m['lam'], 2), round(m['depth'], 4)) for m in free] or 'none'}")
    if any(not a for _, a, _ in rep):
        out("STOP-level: a repeated point disagrees with its earlier evaluation; no reading")
        return dict(v="repeat disagrees", cs=cs)
    if len(cs) == 1 and cs[0]["orient"] == WANT and not nw:
        out(f"reading: one plus-to-minus root in the window, in ({cs[0]['br'][0]:.2f}, {cs[0]['br'][1]:.2f}): it places the rising eigenvalue")
        return dict(v="placed", cs=cs)
    if not cs and not nw:
        out("reading: no plus-to-minus change in the window: the rising eigenvalue is not placed")
        return dict(v="not placed", cs=cs)
    out(f"no reading: {[(c['br'], c['orient']) for c in cs]} and non-robust {nw or 'none'} in the window; the coordinator rules")
    return dict(v="coordinator", cs=cs)


def selftest():
    q = lambda *a: None
    neg = lambda T: [dict(r, sign=-r["sign"]) for r in T]
    g1 = [round(1.55 + 0.01 * i, 2) for i in range(56)]; g2 = [round(2.10 + 0.01 * i, 2) for i in range(31)]
    ok = []
    S, rep = dr.merge(neg(rc.planted(g1, (1.677, 2.2537))) + neg(rc.planted(g2, (1.677, 2.2537))))
    r = read(S, rep, 2.10, 2.40, 2.118, 0.0, q)
    ok.append(("a plus-to-minus root at 2.2537 in 2.10-2.40: placed, in (2.25, 2.26)", r["v"] == "placed" and r["cs"][0]["br"] == (2.25, 2.26)))
    S, rep = dr.merge(rc.planted(g1, (1.677,)) + rc.planted(g2, (1.677,)))
    r = read(S, rep, 2.10, 2.40, 2.118, 0.0, q)
    ok.append(("no root in 2.10-2.40: not placed", r["v"] == "not placed"))
    S, rep = dr.merge(rc.planted(g1, (1.677, 2.2537, 2.3312)) + rc.planted(g2, (1.677, 2.2537, 2.3312)))
    r = read(S, rep, 2.10, 2.40, 2.118, 0.0, q)
    ok.append(("two roots in the window, + to - and - to +: the coordinator rules", r["v"] == "coordinator" and len(r["cs"]) == 2))
    B = neg(rc.planted(g2, (1.677, 2.2537))); B[0] = dict(B[0], ln=B[0]["ln"] + 1e-3)
    S, rep = dr.merge(neg(rc.planted(g1, (1.677, 2.2537))) + B)
    r = read(S, rep, 2.10, 2.40, 2.118, 0.0, q)
    ok.append(("the repeated 2.10 off by 1e-3: no reading", r["v"] == "repeat disagrees"))
    for name, good in ok:
        print(f"planted: {name}: {'PASS' if good else 'FAIL'}")
    allok = all(g for _, g in ok)
    print(f"selftest: {'PASS' if allok else 'FAIL'}{f' [mutate {MUT}]' if MUT else ''}")
    return 0 if allok else 1


if __name__ == "__main__":
    if args[0] == "selftest":
        sys.exit(selftest())
    D, wt, files, lo, hi = float(args[0]), args[1], args[2].split(","), float(args[3]), float(args[4])
    sys.path.insert(0, wt)
    import ell_delta
    l0, l0e = ell_delta.lam0_at(D, *ell_delta.lam0_table())
    rows = []
    for f in files:
        for l in open(f):
            r = json.loads(l)
            assert r["D"] == D, f"{f}: D {r['D']} is not {D}"
            rows.append(r)
    S, rep = dr.merge(rows)
    print(f"D {D:g}, files {[os.path.basename(f) for f in files]}; {len(S)} points {S[0]['lam']:.2f} to {S[-1]['lam']:.2f}")
    read(S, rep, lo, hi, l0, l0e)
    W = [r for r in S if lo - 1e-9 <= r["lam"] <= hi + 1e-9]
    fc = [(a["lam"], b["lam"]) for a, b in zip(W, W[1:]) if a["f64_sign"] != b["f64_sign"]]
    print(f"float64 in the window: sign changes {fc or 'none'}; differs from the hybrid at {sum(r['f64_sign'] != r['sign'] for r in W)} of {len(W)} points")
