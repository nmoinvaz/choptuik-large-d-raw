"""#1025 (iii) and (ii) (d18_criteria.log, the coordinator's rulings after the sign-convention check). A robust change places the
crossing root. Modes:
  dseq LAM FILES            the hybrid sign at one lambda across states, in D order: one robust change places the crossing between
                            the two states; more than one: listed, the coordinator rules; a non-robust point is not counted.
  window D LO HI FILES      one state's points merged (a repeat must agree: same sign, ln|det| to 1e-6), rows of other D and above
                            HI + 0.1 left out: one robust change in [LO, HI] places the crossing root (bracket, estimator range);
                            none: not placed; more than one: listed, the coordinator rules; ln|det| minima without a change reported.
  refine D LO HI FILES      the 0.01 points inside each bracket of [LO, HI] with a sign change (robust or not), comma-separated;
                            exit 4 if there is none or more than 4.
  selftest [--mutate=refine]   (refine: each bracket taken one coarse step too low; the control must fail)"""
import sys, os, json
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
sys.argv = [sys.argv[0], "x"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d185_scan_read as rd
import d18c_read as rc
import d18d_read as dr
sg = lambda s: "+" if s > 0 else "-"


def load(files, D=None, top=None, out=print):
    rows = []
    for f in files:
        rs = [json.loads(l) for l in open(f)]
        keep = [r for r in rs if (D is None or r["D"] == D) and (top is None or r["lam"] <= top + 1e-9)]
        out(f"  {os.path.basename(f)}: {len(rs)} records, {len(keep)} used")
        rows += keep
    return rows


def dseq(rows, lam, out=print):
    R = sorted((r for r in rows if abs(r["lam"] - lam) < 1e-9), key=lambda r: r["D"])
    out(f"lambda {lam:.2f}: " + ", ".join(f"D {r['D']:g} {sg(r['sign'])}{'' if r['noise_robust'] else ' (NOT noise-robust)'}" for r in R))
    ch = [(a["D"], b["D"], a["noise_robust"] and b["noise_robust"]) for a, b in zip(R, R[1:]) if a["sign"] != b["sign"]]
    rob = [(a, b) for a, b, ok in ch if ok]; non = [(a, b) for a, b, ok in ch if not ok]
    out(f"robust changes: {rob or 'none'}; touching a non-robust point (not counted): {non or 'none'}")
    if len(rob) == 1 and not non:
        out(f"reading: the crossing of {lam:.2f} lies between D {rob[0][0]:g} and D {rob[0][1]:g}")
        return dict(v="placed", rob=rob)
    if not rob and not non:
        out(f"reading: no change at {lam:.2f} over D {R[0]['D']:g}-{R[-1]['D']:g}: not placed")
        return dict(v="not placed", rob=rob)
    out(f"no reading: changes {rob}, non-robust {non or 'none'}; the coordinator rules")
    return dict(v="coordinator", rob=rob)


def window(S, rep, lo, hi, out=print):
    rob, non = rd.changes(S)
    by = {round(r["lam"], 2): r for r in S}
    inw = lambda c: c["br"][0] >= lo - 1e-9 and c["br"][1] <= hi + 1e-9
    W = [r for r in S if lo - 1e-9 <= r["lam"] <= hi + 1e-9]
    out(f"window {lo:.2f}-{hi:.2f}: {len(W)} points; not noise-robust: {[r['lam'] for r in W if not r['noise_robust']] or 'none'}")
    out("signs: " + " ".join("%.2f%s" % (r["lam"], sg(r["sign"])) for r in W))
    out(f"repeated points: {[(k, 'agree' if a else 'DISAGREE', f'{d:+.1e}') for k, a, d in rep] or 'none'}")
    cs = [c for c in rob if inw(c)]; nw = [c["br"] for c in non if inw(c)]
    for c in cs:
        o = f"{sg(by[round(c['br'][0], 2)]['sign'])} to {sg(by[round(c['br'][1], 2)]['sign'])}"
        out(f"  change in ({c['br'][0]:.2f}, {c['br'][1]:.2f}), {o} in this state: det-linear {c['lin']:.6f}, range [{c['lo']:.6f}, {c['hi']:.6f}]")
    out(f"robust changes in the window: {len(cs)}; touching a non-robust point (not counted): {nw or 'none'}")
    free = [m for m in rc.minima(W, [c for c in rob + non if inw(c)]) if not m["beside"]]
    out(f"ln|det| local minima without a sign change in the window: {[(round(m['lam'], 2), round(m['depth'], 4)) for m in free] or 'none'}")
    if any(not a for _, a, _ in rep):
        out("STOP-level: a repeated point disagrees with its earlier evaluation; no reading")
        return dict(v="repeat disagrees", cs=cs)
    if len(cs) == 1 and not nw:
        out(f"reading: one robust change in the window, in ({cs[0]['br'][0]:.2f}, {cs[0]['br'][1]:.2f}): it places the crossing root")
        return dict(v="placed", cs=cs)
    if not cs and not nw:
        out("reading: no change in the window: not placed")
        return dict(v="not placed", cs=cs)
    out(f"no reading: {[c['br'] for c in cs]} robust and {nw or 'none'} non-robust in the window; the coordinator rules")
    return dict(v="coordinator", cs=cs)


def refine(S, lo, hi):
    W = [r for r in S if lo - 1e-9 <= r["lam"] <= hi + 1e-9]
    br = [(a["lam"], b["lam"]) for a, b in zip(W, W[1:]) if a["sign"] != b["sign"] and b["lam"] - a["lam"] > 0.011]
    if MUT == "refine":
        br = [(a - 0.05, b - 0.05) for a, b in br]
    pts = [round(a + 0.01 * k, 2) for a, b in br for k in range(1, int(round((b - a) / 0.01)))]
    return br, pts


def selftest():
    q = lambda *a: None
    neg = lambda T: [dict(r, sign=-r["sign"]) for r in T]
    coarse = [round(1.20 + 0.05 * i, 2) for i in range(8)]; b25 = [round(1.55 + 0.01 * i, 2) for i in range(41)]
    ok = []
    roots = (1.3712, 1.7425, 2.1)                       # one root in (1.35, 1.40), as D 18.25's parity predicts
    T = lambda ls: [dict(r, D=18.25) for r in rc.planted(ls, roots)]
    S, rep = dr.merge(T(coarse) + T(b25))
    br, pts = refine(S, 1.20, 1.55)
    ok.append(("refine: the bracket (1.35, 1.40) and its points 1.36-1.39", br == [(1.35, 1.4)] and pts == [1.36, 1.37, 1.38, 1.39]))
    S, rep = dr.merge(T(coarse) + T(b25) + T(pts))
    r = window(S, rep, 1.20, 1.55, q)
    ok.append(("window: one robust change placed in (1.37, 1.38)", r["v"] == "placed" and r["cs"][0]["br"] == (1.37, 1.38)))
    T3 = lambda ls: [dict(r, D=18.25) for r in rc.planted(ls, (1.2731, 1.3712, 1.4523, 1.7425, 2.1))]
    S, rep = dr.merge(T3(coarse) + T3(b25))
    ok.append(("three roots in 1.20-1.55: the coordinator rules", window(S, rep, 1.20, 1.55, q)["v"] == "coordinator"))
    B = T(b25); B[0] = dict(B[0], ln=B[0]["ln"] + 1e-3)
    S, rep = dr.merge(T(coarse) + B)
    ok.append(("the repeated 1.55 off by 1e-3: no reading", window(S, rep, 1.20, 1.55, q)["v"] == "repeat disagrees"))
    seq = lambda signs: [dict(D=D, lam=1.2, sign=float(s), noise_robust=True) for D, s in zip((18.25, 18.3125, 18.375, 18.4375, 18.5), signs)]
    r = dseq(seq((1, 1, -1, -1, -1))[::-1], 1.2, q)          # given in reverse order: must be sorted by D
    ok.append(("dseq: the crossing between D 18.3125 and 18.375", r["v"] == "placed" and r["rob"] == [(18.3125, 18.375)]))
    ok.append(("dseq: three changes, the coordinator rules", dseq(seq((1, -1, 1, -1, -1)), 1.2, q)["v"] == "coordinator"))
    for name, good in ok:
        print(f"planted: {name}: {'PASS' if good else 'FAIL'}")
    allok = all(g for _, g in ok)
    print(f"selftest: {'PASS' if allok else 'FAIL'}{f' [mutate {MUT}]' if MUT else ''}")
    return 0 if allok else 1


if __name__ == "__main__":
    m = args[0]
    if m == "selftest":
        sys.exit(selftest())
    if m == "dseq":
        lam, files = float(args[1]), args[2].split(",")
        print(f"dseq at lambda {lam:.2f}:"); rows = load(files)
        dseq(rows, lam)
        sys.exit(0)
    D, lo, hi, files = float(args[1]), float(args[2]), float(args[3]), args[4].split(",")
    if m == "refine":
        S, rep = dr.merge(load(files, D, hi + 0.1, out=lambda *a: None))
        br, pts = refine(S, lo, hi)
        if not br or len(br) > 4:
            print(f"refine: {len(br)} brackets {br}", file=sys.stderr); sys.exit(4)
        print(",".join(f"{p:.2f}" for p in pts))
        sys.exit(0)
    print(f"window D {D:g} {lo:.2f}-{hi:.2f}:"); S, rep = dr.merge(load(files, D, hi + 0.1))
    window(S, rep, lo, hi)
    W = [r for r in S if lo - 1e-9 <= r["lam"] <= hi + 1e-9]
    fc = [(a["lam"], b["lam"]) for a, b in zip(W, W[1:]) if a["f64_sign"] != b["f64_sign"]]
    print(f"float64 in the window: sign changes {fc or 'none'}; differs from the hybrid at {sum(r['f64_sign'] != r['sign'] for r in W)} of {len(W)} points")
