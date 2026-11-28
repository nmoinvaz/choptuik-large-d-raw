"""#1101 dh170, R3: reads d18_secant.py scan records (one jsonl per lambda in a folder, scan_*_p*.jsonl) of R3's state (the kappa 0.25
re-solve of R1's state, mm5) and its secant record, against the reading of t5's comment 7231154979: the root against 0.1272 (the single
power, p = 2.39), within 2e-3 the model stands, otherwise a second term is needed.

usage: results_r3.py scan DIR... [--pair]
           all points of the folders together; the first robust sign change (the lowest lambda, the others listed) gives the bracket.
           exit 0 a change, 2 none; --pair prints "LO HI" only
       results_r3.py read DIR... --secant=FILE
           the secant record (d18_secant.py run, tol 5e-5) read against 0.1272: exit 0 formed, 2 no robust change, 3 a change and no
           secant record, 4 the secant record is not read
       results_r3.py selftest [--mutate=tol|pred|last|sign]     planted cases; exit 0 only if each reads as written

The det-linear root of a pair is the zero of the straight line through f = sign * exp(ln|det| - ref), ref the larger of the two ln|det|
(the reader's and dh370's definition); defined only when the two hybrid signs differ. A secant record is read only if its status is
`tol`, both bracket ends are robust with opposite signs, and its bracket lies inside the scan's pair; the root is its `lam_lin`."""
import glob
import json
import math
import sys

PRED, TOL = 0.1272, 2e-3          # t5's prediction (single power p = 2.39) and its reading band, comment 7231154979
R2_ROOT = 0.117824909             # R2's secant root (kappa 0.35), for the table only
MUTATE = ""


def load(*dirs):
    pts = {}
    for d in dirs:
        for f in sorted(glob.glob(f"{d}/scan_*_p*.jsonl")):
            for line in open(f):
                if line.strip():
                    w = json.loads(line)
                    pts[round(w["lam"], 6)] = w
    return pts


def ok(w):
    return bool(w["noise_robust"]) and bool(w.get("robust"))


def table(pts):
    print("| lambda | hybrid sign | noise-robust | robust (dln <= 0.1) | dln | float64 sign | ln\\|det\\| | b12 | seconds |")
    print("|---|---|---|---|---|---|---|---|---|")
    for lam in sorted(pts):
        w = pts[lam]
        print(f"| {lam:.3f} | {w['sign']:+.0f} | {w['noise_robust']} | {w.get('robust')} | {w['dln']:.2e} | {w['f64_sign']:+.0f} "
              f"| {w['ln']:.10f} | {w.get('b12')} | {w['sec']} |")


def changes(pts):
    """robust sign changes between neighbouring points, lowest lambda first"""
    lams = sorted(pts)
    return [(x, y) for x, y in zip(lams, lams[1:]) if ok(pts[x]) and ok(pts[y]) and pts[x]["sign"] != pts[y]["sign"]]


def verdict(root, lo, hi):
    """-> (kind, text): kind 'stands', 'second' or 'edge'; the band is PRED +- TOL (t5's reading)"""
    tol = 2e-2 if MUTATE == "tol" else TOL
    pred = 0.1172 if MUTATE == "pred" else PRED
    d = root - pred
    side = ("below" if d < 0 else "above") if MUTATE != "sign" else ("above" if d < 0 else "below")
    inside = [abs(x - pred) <= tol for x in (lo, hi)]
    if abs(d) <= tol and all(inside):
        return "stands", f"|root - {PRED}| = {abs(d):.5f} <= {TOL:g}: the single power stands"
    if abs(d) > tol and not any(inside):
        return "second", f"|root - {PRED}| = {abs(d):.5f} > {TOL:g} ({side} the prediction): a second term is needed"
    return "edge", f"root - {PRED} = {d:+.5f}, the bracket reaches the edge of the band {TOL:g}: reported as measured"


def r3(pts, secant=None):
    """-> dict(changes, pair, status, root, diff, kind, verdict, notes); status formed | nochange | nosecant | notread"""
    ch = changes(pts)
    res = {"changes": ch, "notes": [], "pair": None, "root": None, "diff": None, "kind": None, "verdict": ""}
    bad = [lam for lam in sorted(pts) if not ok(pts[lam])]
    if bad:
        res["notes"].append(f"non-robust points {bad}: not used")
    if not ch:
        res.update(status="nochange", verdict=f"no robust change in [{min(pts):g}, {max(pts):g}]: reported as measured")
        return res
    pair = ch[-1] if MUTATE == "last" else ch[0]
    res["pair"] = pair
    if len(ch) > 1:
        res["notes"].append(f"{len(ch)} robust changes {ch}: the lowest-lambda one gives the bracket, the others are reported")
    if secant is None:
        res.update(status="nosecant", verdict=f"bracket {pair}: run d18_secant.py run on it at tol 5e-5")
        return res
    good = (secant.get("kind") == "root" and secant.get("status") == "tol" and all(secant["robust"]) and secant["signs"][0] != secant["signs"][1]
            and pair[0] - 1e-9 <= secant["bracket"][0] and secant["bracket"][1] <= pair[1] + 1e-9)
    if not good:
        res.update(status="notread", verdict=f"the secant record is not read: status {secant.get('status')}, robust {secant.get('robust')}, "
                   f"signs {secant.get('signs')}, bracket {secant.get('bracket')} against {pair}")
        return res
    kind, text = verdict(secant["lam_lin"], *secant["bracket"])
    res.update(status="formed", root=secant["lam_lin"], diff=secant["lam_lin"] - PRED, kind=kind, verdict=text)
    return res


def plant(lam, r, c=1.0):
    """a record of a determinant linear in lambda: det = c (r - lam)"""
    d = c * (r - lam)
    return {"lam": lam, "sign": 1.0 if d > 0 else -1.0, "ln": math.log(abs(d)), "dln": 1e-6, "noise_robust": True, "robust": True,
            "f64_sign": 1.0, "sec": 0, "b12": "rust"}


def selftest():
    bad = []

    def chk(name, cond):
        print(("pass " if cond else "FAIL ") + name)
        if not cond:
            bad.append(name)
    first = (0.115, 0.125, 0.135, 0.145)
    six = (0.105,) + first + (0.155,)

    def pts(r, lams=first):
        return {lam: plant(lam, r) for lam in lams}

    def sec(lo, hi, root, **kw):
        d = dict(kind="root", status="tol", bracket=[lo, hi], signs=[1, -1], robust=[True, True], lam_lin=root, lam_brent=root)
        d.update(kw)
        return d
    for r, want in ((0.1272, (0.125, 0.135)), (0.1195, (0.115, 0.125)), (0.1405, (0.135, 0.145))):
        o = r3(pts(r))
        chk(f"planted root {r}: the bracket is {want}, status nosecant", o["pair"] == want and o["status"] == "nosecant")
    chk("planted root 0.3: no change in the four, reported as measured", r3(pts(0.3))["status"] == "nochange" and "reported as measured" in r3(pts(0.3))["verdict"])
    o = r3(pts(0.1075, six))
    chk("planted root 0.1075: the widened point 0.105 gives the bracket (0.105, 0.115)", o["pair"] == (0.105, 0.115))
    o = r3(pts(0.150, six))
    chk("planted root 0.150: the widened point 0.155 gives the bracket (0.145, 0.155)", o["pair"] == (0.145, 0.155))
    chk("planted root 0.3 over the six: nochange", r3(pts(0.3, six))["status"] == "nochange")
    two = pts(0.1272, six)
    two[0.105] = dict(two[0.105], sign=-two[0.105]["sign"])
    o = r3(two)
    chk("two changes: the lowest-lambda one is the bracket, both reported", o["changes"] == [(0.105, 0.115), (0.125, 0.135)] and o["pair"] == (0.105, 0.115))
    nr = pts(0.1272)
    nr[0.135]["robust"] = False
    chk("a non-robust end gives no change", r3(nr)["status"] == "nochange" and "0.135" in " ".join(r3(nr)["notes"]))
    # the secant record against 0.1272 +- 2e-3 (t5's reading): a scan pair 0.005 either side of the planted root, the bracket 2.5e-5 wide on it
    def S(root, **kw):
        scan = {lam: plant(lam, root) for lam in (round(root - 0.005, 6), round(root + 0.005, 6))}
        return r3(scan, sec(root - 1.25e-5, root + 1.25e-5, root, **kw))
    for root, want in ((0.1272, "stands"), (0.1253, "stands"), (0.1291, "stands"), (0.1250, "second"), (0.1294, "second"), (0.1180, "second"), (0.1331, "second")):
        o = S(root)
        chk(f"secant root {root}: {want}", o["status"] == "formed" and o["kind"] == want and abs(o["diff"] - (root - PRED)) < 1e-12)
    chk("secant root 0.1250 is read 'below'", "below" in S(0.1250)["verdict"] and "above" not in S(0.1250)["verdict"])
    chk("secant root 0.1294 is read 'above'", "above" in S(0.1294)["verdict"] and "below" not in S(0.1294)["verdict"])
    o = S(0.12522, bracket=[0.1251, 0.1254])
    chk("a bracket across the lower edge of the band (root inside) is 'edge'", o["status"] == "formed" and o["kind"] == "edge")
    o = S(0.1291, bracket=[0.1290, 0.1293])
    chk("a bracket across the upper edge of the band (root inside) is 'edge'", o["status"] == "formed" and o["kind"] == "edge")
    chk("a secant record with status maxev is not read", S(0.1272, status="maxev")["status"] == "notread")
    chk("a secant record with a non-robust end is not read", S(0.1272, robust=[True, False])["status"] == "notread")
    chk("a secant record with equal signs is not read", S(0.1272, signs=[1, 1])["status"] == "notread")
    chk("a secant bracket outside the scan's pair is not read", r3(pts(0.1272), sec(0.14, 0.1401, 0.14005))["status"] == "notread")
    print("selftest:", "FAIL " + "; ".join(bad) if bad else "all cases read as written")
    return 1 if bad else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for a in sys.argv[1:]:
        if a.startswith("--mutate="):
            MUTATE = a.split("=", 1)[1]
    if not args:
        sys.exit(__doc__)
    if args[0] == "selftest":
        sys.exit(selftest())
    if args[0] not in ("scan", "read"):
        sys.exit(__doc__)
    sc = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--secant=")), None) if args[0] == "read" else None
    points = load(*args[1:])
    if not points:
        sys.exit("no points in " + " ".join(args[1:]))
    rec = None
    if sc is not None:
        roots = [json.loads(line) for line in open(sc) if line.strip() and json.loads(line).get("kind") == "root"]
        rec = roots[-1] if roots else {"kind": "none"}
    out = r3(points, rec)
    if "--pair" in sys.argv:
        if out["pair"] is None:
            sys.exit(2)
        print(f"{out['pair'][0]:g} {out['pair'][1]:g}")
        sys.exit(0)
    table(points)
    print()
    for n in out["notes"]:
        print(f"- note: {n}")
    print(f"- robust changes: {out['changes'] if out['changes'] else 'none'}")
    if out["status"] == "nochange":
        print(f"- {out['verdict']}")
        sys.exit(2)
    print(f"- bracket (first robust change): {out['pair']}")
    if args[0] == "scan" or out["status"] == "nosecant":
        print(f"- {out['verdict']}")
        sys.exit(0 if args[0] == "scan" else 3)
    if out["status"] == "notread":
        print(f"- {out['verdict']}")
        sys.exit(4)
    print(f"- secant root (lam_lin of {sc}): {out['root']:.9f}; bracket {rec['bracket']}")
    print(f"- root - {PRED} = {out['diff']:+.6f}; against R2's root {R2_ROOT}: {out['root'] - R2_ROOT:+.6f}")
    print(f"- verdict: {out['verdict']}")
    sys.exit(0)
