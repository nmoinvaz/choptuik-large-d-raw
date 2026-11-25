"""#1025 the readings of (a), D 18 below 1.70, and (b), D 18.25 (d18_criteria.log, the coordinator's ruling after the D 18.5
scan). Robust sign changes, brackets and estimator ranges come from d185_scan_read.py (imported). Added here: the local
minima of the hybrid ln|det| that are not beside a sign change, where a near-tangent pair or a pair closer than the grid
shows, with their depth (the smaller rise to a neighbour); the scan's end points cannot hold one.
Mode a merges the scans of one state: a robust change below lambda 1.70 is reading (a1), a third root at D 18; none is
reading (a2), D 18.5's root continues one of the pair. Mode b prints the count and places; the post reads them.
usage: d18c_read.py a|b D WT_MATTER SCAN.jsonl[,SCAN2.jsonl]   |   d18c_read.py selftest [--mutate=nominima]"""
import sys, os, json
import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
sys.argv = [sys.argv[0], "x"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d185_scan_read as rd


def minima(S, chs):
    if MUT == "nominima":                                   # control: the minima are not looked for
        return []
    near = {round(v, 2) for c in chs for v in c["br"]}
    return [dict(lam=S[i]["lam"], depth=min(S[i - 1]["ln"], S[i + 1]["ln"]) - S[i]["ln"], beside=round(S[i]["lam"], 2) in near)
            for i in range(1, len(S) - 1) if S[i]["ln"] < S[i - 1]["ln"] and S[i]["ln"] < S[i + 1]["ln"]]


def read(mode, S, out=print, l0=None):
    rob, non = rd.changes(S)
    mins = minima(S, rob + non)
    out(f"points {len(S)}, {S[0]['lam']:.2f} to {S[-1]['lam']:.2f}; not noise-robust: {[r['lam'] for r in S if not r['noise_robust']] or 'none'}")
    out("signs: " + " ".join("%.2f%s" % (r["lam"], "+" if r["sign"] > 0 else "-") for r in S))
    out(f"robust sign changes: {len(rob)}; changes touching a non-robust point (not counted): {[c['br'] for c in non] or 'none'}")
    for c in rob:
        d = f", delta at the det-linear estimate {c['lin'] - l0:+.6f}" if l0 is not None else ""
        out(f"  bracket ({c['br'][0]:.2f}, {c['br'][1]:.2f}): det-linear {c['lin']:.6f}, range [{c['lo']:.6f}, {c['hi']:.6f}]{d}")
    free = [m for m in mins if not m["beside"]]
    out(f"ln|det| local minima: {[(round(m['lam'], 2), round(m['depth'], 4)) for m in mins] or 'none'}; without a sign change beside "
        f"them: {[(round(m['lam'], 2), round(m['depth'], 4)) for m in free] or 'none'}")
    v = None
    if mode == "a":
        below = [c for c in rob if c["br"][1] <= 1.70 + 1e-9]
        nb = [c for c in non if c["br"][1] <= 1.70 + 1e-9]
        if below:
            v = "a1"
            out(f"reading (a1): {len(below)} robust change(s) below 1.70 at {[c['br'] for c in below]}: a third root at D 18; D 18.5's root "
                f"at 1.677 likely continues it, and the D 18 pair has merged and left the real axis between D 18 and 18.5")
        elif nb:
            v = "unresolved"
            out(f"no reading: a change below 1.70 touches a non-robust point ({[c['br'] for c in nb]}); the coordinator rules")
        else:
            v = "a2"
            out("reading (a2): no change below 1.70 at D 18: D 18.5's root continues one of the pair, and the other's fate is open")
        fb = [m for m in free if m["lam"] < 1.70 + 1e-9]
        if fb:
            out(f"  note: ln|det| minima without a sign change below 1.70: {[round(m['lam'], 2) for m in fb]} (a near-tangent pair is possible there)")
    return dict(v=v, n=len(rob), non=len(non), free=[round(m["lam"], 2) for m in free], rob=rob)


def planted(lams, real, cplx=(), k=20.0):
    S = []
    for l in lams:
        f = np.prod([l - r for r in real]) * np.prod([(l - a) ** 2 + b ** 2 for a, b in cplx]) * np.exp(k * (l - 1.8))
        S.append(dict(lam=float(l), sign=float(np.sign(f)), ln=float(np.log(abs(f)) - 1920), noise_robust=True))
    return S


def selftest():
    g = [round(1.55 + 0.01 * i, 2) for i in range(36)]; g2 = [round(1.55 + 0.01 * i, 2) for i in range(41)]
    q = lambda *s: None
    ok = []
    r = read("a", planted(g, (1.6237, 1.774978, 1.8075)), q)
    ok.append(("a third root at 1.6237: reading a1, three robust changes", r["v"] == "a1" and r["n"] == 3))
    r = read("a", planted(g, (1.6952, 1.774978, 1.8075)), q)
    ok.append(("a third root at 1.6952, in the join (1.69, 1.70): reading a1", r["v"] == "a1"))
    r = read("a", planted(g, (1.774978, 1.8075)), q)
    ok.append(("no third root: reading a2, no minimum without a change", r["v"] == "a2" and r["free"] == []))
    r = read("a", planted(g, (1.774978, 1.8075), cplx=((1.6304, 0.001),)), q)
    ok.append(("a near-tangent pair at 1.6304 +- 0.001i: reading a2, a minimum without a change at 1.63", r["v"] == "a2" and r["free"] == [1.63]))
    r = read("b", planted(g2, (1.7215, 1.7285)), q)
    ok.append(("a pair inside one bracket (1.72, 1.73): no change, a minimum without a change there", r["n"] == 0 and r["free"] in ([1.72], [1.73])))
    r = read("b", planted(g2, (1.7150, 1.7240)), q)
    ok.append(("a close pair 0.009 apart in two brackets: two robust changes", r["n"] == 2))
    for name, good in ok:
        print(f"planted: {name}: {'PASS' if good else 'FAIL'}")
    allok = all(gd for _, gd in ok)
    print(f"selftest: {'PASS' if allok else 'FAIL'}{f' [mutate {MUT}]' if MUT else ''}")
    return 0 if allok else 1


if __name__ == "__main__":
    if args[0] == "selftest":
        sys.exit(selftest())
    mode, D, wt, files = args[0], float(args[1]), args[2], args[3].split(",")
    sys.path.insert(0, wt)
    import ell_delta
    l0, l0e = ell_delta.lam0_at(D, *ell_delta.lam0_table())
    S = {}
    for f in files:
        for l in open(f):
            r = json.loads(l)
            assert r["D"] == D, f"{f}: D {r['D']} is not {D}"
            assert round(r["lam"], 6) not in S, f"lambda {r['lam']} twice"
            S[round(r["lam"], 6)] = r
    S = [S[k] for k in sorted(S)]
    print(f"D {D:g}, mode {mode}, files {[os.path.basename(f) for f in files]}; lambda_0 {l0:.10f} (error {l0e:.1e})")
    read(mode, S, l0=l0)
    fc = [(a["lam"], b["lam"]) for a, b in zip(S, S[1:]) if a["f64_sign"] != b["f64_sign"]]
    print(f"float64 sign changes: {len(fc)} in {fc}; float64 differs from the hybrid at "
          f"{[x['lam'] for x in S if x['f64_sign'] != x['sign']]}")
