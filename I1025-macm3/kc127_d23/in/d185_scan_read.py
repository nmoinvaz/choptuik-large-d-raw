"""#1025 D 18.5: the reading of the hybrid sign scan (d18_criteria.log, the coordinator's ruling after (A)).
A sign change between neighbouring grid points counts as robust when both points are noise-robust; changes that touch a
non-robust point are listed and not counted. Each robust change is bracketed by its grid points. Its estimator range is
the span of four estimates of the root of det M = sign exp(ln - ln_ref) inside the bracket: the line through the bracket,
the two quadratics through it and one neighbour, the cubic through it and both neighbours (information, not a bound).
Control on real data: the reference scan's (D 18) estimator ranges must contain its bisected roots; if not, the gap is
read from the brackets only. Gap reading, for two robust changes: the gap interval at D (from the ranges, or brackets)
against the reference's (bisected roots where given, else ranges); wholly below: approach, wholly above: separate, else
not resolved by the scan.
usage: d185_scan_read.py SCAN.jsonl D WT_MATTER REF_SCAN.jsonl REF_LO [REF_HI|-] [--mutate=noise|shift]
       d185_scan_read.py selftest [--mutate=noise|shift]   (exit 0 only if every planted case reads as written)"""
import sys, json
import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
args = [a for a in sys.argv[1:] if not a.startswith("--")]


def changes(S):
    x = np.array([r["lam"] for r in S]); ref = max(r["ln"] for r in S)
    f = np.array([r["sign"] * np.exp(r["ln"] - ref) for r in S])
    rob, non = [], []
    for i in range(len(S) - 1):
        if S[i]["sign"] == S[i + 1]["sign"]:
            continue
        ok = (S[i]["noise_robust"] and S[i + 1]["noise_robust"]) or MUT == "noise"   # noise: the control that ignores the noise test
        h = x[i + 1] - x[i]
        est = [x[i] + h * f[i] / (f[i] - f[i + 1])]
        for j, k in ((i - 1, 3), (i, 3), (i - 1, 4)):
            if j >= 0 and j + k <= len(S):
                p = np.polyfit(x[j:j + k] - x[i], f[j:j + k], k - 1)
                est += [r.real + x[i] for r in np.roots(p) if abs(r.imag) < 1e-12 and 0 <= r.real <= h]
        if MUT == "shift":
            est = [e + 0.003 for e in est]
        (rob if ok else non).append(dict(br=(float(x[i]), float(x[i + 1])), lin=float(est[0]), lo=float(min(est)),
                                         hi=float(max(est)), n_est=len(est)))
    return rob, non


def gap_iv(a, b, use_ranges):
    if use_ranges:
        return b["lo"] - a["hi"], b["hi"] - a["lo"]
    return b["br"][0] - a["br"][1], b["br"][1] - a["br"][0]


def read(S, R, ref_lo, ref_hi, out=print):
    rob, non = changes(S)
    rr, _ = changes(R)
    out(f"robust sign changes: {len(rob)}; changes touching a non-robust point (not counted): {[c['br'] for c in non] or 'none'}")
    for c in rob:
        out(f"  bracket ({c['br'][0]:.2f}, {c['br'][1]:.2f}): det-linear {c['lin']:.6f}, estimator range "
            f"[{c['lo']:.6f}, {c['hi']:.6f}] ({c['n_est']} estimates)")
    ctl = len(rr) == 2 and rr[0]["lo"] <= ref_lo <= rr[0]["hi"] and (ref_hi is None or rr[1]["lo"] <= ref_hi <= rr[1]["hi"])
    out(f"control: the reference's estimator ranges {[(round(c['lo'], 6), round(c['hi'], 6)) for c in rr]} "
        f"{'contain' if ctl else 'DO NOT contain'} its bisected roots {ref_lo}, {ref_hi if ref_hi is not None else '(upper not bisected)'}")
    if len(rob) != 2:
        out(f"reading: {len(rob)} robust sign changes, not two: the pair is not seen as two changes at 0.01; the coordinator rules")
        return dict(n=len(rob), non=len(non), ctl=ctl, verdict=None)
    g = gap_iv(rob[0], rob[1], ctl)
    a = dict(lo=ref_lo, hi=ref_lo, br=rr[0]["br"]) if ctl else dict(lo=ref_lo, hi=ref_lo, br=(ref_lo, ref_lo))
    b = (dict(lo=ref_hi, hi=ref_hi, br=(ref_hi, ref_hi)) if ref_hi is not None else (rr[1] if ctl else dict(br=rr[1]["br"])))
    gr = gap_iv(a, b, ctl)
    v = "approach" if g[1] < gr[0] else "separate" if g[0] > gr[1] else "not resolved by the scan"
    out(f"reading: two robust sign changes, the pair persists. Gap {'from the estimator ranges' if ctl else 'from the brackets only'}: "
        f"[{g[0]:.6f}, {g[1]:.6f}] against the reference's [{gr[0]:.6f}, {gr[1]:.6f}]: {v}")
    return dict(n=2, non=len(non), ctl=ctl, verdict=v, rob=rob)


def planted(lams, a, b, k=20.0, robust_off=(), cplx=False):
    S = []
    for l in lams:
        f = ((l - a) ** 2 + b ** 2 if cplx else (l - a) * (l - b)) * np.exp(k * (l - 1.8))
        S.append(dict(lam=float(l), sign=float(np.sign(f)), ln=float(np.log(abs(f)) - 1920), noise_robust=round(l, 2) not in robust_off))
    return S


def selftest():
    g18 = [round(1.70 + 0.01 * i, 2) for i in range(21)]; g185 = [round(1.55 + 0.01 * i, 2) for i in range(36)]
    a, b = 1.774978, 1.8075                    # D 18 analogue; b is not given as bisected
    R = planted(g18, a, b)
    q = lambda *s: None
    ok = []
    r = read(R, R, a, None, q)
    inside = r["n"] == 2 and r["rob"][0]["lo"] <= a <= r["rob"][0]["hi"] and r["rob"][1]["lo"] <= b <= r["rob"][1]["hi"]
    ok.append(("reference: two robust changes, planted roots inside their ranges", r["n"] == 2 and r["ctl"] and inside))
    r = read(planted(g18, a, b, robust_off=(1.78,)), R, a, None, q)
    ok.append(("a non-robust point beside the lower change: one robust change, one listed", r["n"] == 1 and r["non"] == 1))
    r = read(planted(g185, 1.66, 0.004, cplx=True), R, a, None, q)
    ok.append(("a complex pair: no change", r["n"] == 0))
    g0 = b - a
    for dg, want in ((+0.005, ("separate",)), (-0.005, ("approach",)), (+0.0003, ("separate", "not resolved by the scan"))):
        a2 = 1.6237; S = planted(g185, a2, a2 + g0 + dg)
        r = read(S, R, a, None, q)
        inside = r["n"] == 2 and r["rob"][0]["lo"] <= a2 <= r["rob"][0]["hi"] and r["rob"][1]["lo"] <= a2 + g0 + dg <= r["rob"][1]["hi"]
        ok.append((f"gap change {dg:+.4f}: reads {want}, planted roots inside their ranges", r["verdict"] in want and inside))
    for name, good in ok:
        print(f"planted: {name}: {'PASS' if good else 'FAIL'}")
    allok = all(g for _, g in ok)
    print(f"selftest: {'PASS' if allok else 'FAIL'}{f' [mutate {MUT}]' if MUT else ''}")
    return 0 if allok else 1


if __name__ == "__main__":
    if args[0] == "selftest":
        sys.exit(selftest())
    scan, D, wt, refscan, rlo = args[0], float(args[1]), args[2], args[3], float(args[4])
    rhi = None if len(args) < 6 or args[5] == "-" else float(args[5])
    sys.path.insert(0, wt)
    import ell_delta
    l0, l0e = ell_delta.lam0_at(D, *ell_delta.lam0_table())
    S = sorted((json.loads(l) for l in open(scan)), key=lambda r: r["lam"])
    R = sorted((json.loads(l) for l in open(refscan)), key=lambda r: r["lam"])
    print(f"scan: {len(S)} points, {S[0]['lam']:.2f} to {S[-1]['lam']:.2f}, D {D:g}; signs: "
          + " ".join("%.2f%s" % (r["lam"], "+" if r["sign"] > 0 else "-") for r in S))
    print(f"points not noise-robust: {[r['lam'] for r in S if not r['noise_robust']] or 'none'}")
    r = read(S, R, rlo, rhi)
    for c in r.get("rob", []) or changes(S)[0]:
        print(f"  delta at the det-linear estimate {c['lin']:.6f}: {c['lin'] - l0:+.6f} (lambda_0({D:g}) {l0:.10f}, error {l0e:.1e})")
    fc = [(a["lam"], b["lam"]) for a, b in zip(S, S[1:]) if a["f64_sign"] != b["f64_sign"]]
    dis = [x["lam"] for x in S if x["f64_sign"] != x["sign"]]
    print(f"float64 sign changes: {len(fc)} in {fc}; float64 differs from the hybrid at {len(dis)} of {len(S)} points")
