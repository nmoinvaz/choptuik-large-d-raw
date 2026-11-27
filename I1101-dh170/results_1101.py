"""#1101 dh170: reads d18_secant.py scan records (one jsonl per lambda in a folder, scan_*_p*.jsonl) of the control (R0's
state B at lambda 0.045 and 0.050, on the Rust block 12) or of R2's state, against the bars written in README.md.

usage: results_1101.py control SCANDIR     exit 0 only if every control bar passes
       results_1101.py r2 SCANDIR          prints the table, the bracketing pair, delta, E_root and the verdict
       results_1101.py selftest [--mutate=shift|signs|e16]    planted cases; exit 0 only if each reads as written

The det-linear root of a pair is the zero of the straight line through f = sign * exp(ln|det| - ref), ref the larger of
the two ln|det| (the reader's and dh370's definition); defined only when the two hybrid signs differ."""
import glob
import json
import math
import sys

REF_LN = {0.045: -3902.5303054577, 0.050: -3901.1035170558}   # dh370's state B (I1101-dh370/results.md)
ROOT_B = 0.045967998                                         # dh370's det-linear root of state B
TOL_LN, TOL_ROOT = 1e-4, 1e-5                                # t5's control bars
BAR_HI, BAR_LO = 3e-3, 1e-3                                  # t5's bars on |E_root|
MUTATE = ""


def load(d):
    pts = {}
    for f in sorted(glob.glob(f"{d}/scan_*_p*.jsonl")):
        for line in open(f):
            if line.strip():
                w = json.loads(line)
                pts[round(w["lam"], 6)] = w
    return pts


def lin(r1, r2):
    if r1["sign"] == r2["sign"]:
        return None
    ref = max(r1["ln"], r2["ln"])
    f1 = r1["sign"] * math.exp(r1["ln"] - ref)
    f2 = r2["sign"] * math.exp(r2["ln"] - ref)
    return r1["lam"] + (r2["lam"] - r1["lam"]) * f1 / (f1 - f2)


def ok(w):
    return bool(w["noise_robust"]) and bool(w.get("robust"))


def table(pts):
    print("| lambda | hybrid sign | noise-robust | robust (dln <= 0.1) | dln | float64 sign | ln\\|det\\| | b12 | seconds |")
    print("|---|---|---|---|---|---|---|---|---|")
    for lam in sorted(pts):
        w = pts[lam]
        print(f"| {lam:.3f} | {w['sign']:+.0f} | {w['noise_robust']} | {w.get('robust')} | {w['dln']:.2e} | {w['f64_sign']:+.0f} "
              f"| {w['ln']:.10f} | {w.get('b12')} | {w['sec']} |")


def control(pts, quiet=False):
    """-> list of (bar, passed, text)"""
    out = []
    need = [0.045, 0.050]
    if any(l not in pts for l in need):
        return [("both points present", False, f"have {sorted(pts)}")]
    a, b = pts[0.045], pts[0.050]
    out.append(("signs + then -", a["sign"] == 1 and b["sign"] == -1, f"{a['sign']:+.0f}, {b['sign']:+.0f}"))
    out.append(("both robust", ok(a) and ok(b), f"{ok(a)}, {ok(b)}"))
    out.append(("on the Rust block 12 (b12 field)", a.get("b12") == "rust" and b.get("b12") == "rust", f"{a.get('b12')}, {b.get('b12')}"))
    for lam, w in ((0.045, a), (0.050, b)):
        d = w["ln"] - REF_LN[lam]
        out.append((f"ln|det| at {lam} within {TOL_LN:g} of dh370's", abs(d) <= TOL_LN, f"{w['ln']:.10f} - ({REF_LN[lam]}) = {d:+.3e}"))
    r = lin(a, b)
    out.append((f"det-linear root within {TOL_ROOT:g} of {ROOT_B}", r is not None and abs(r - ROOT_B) <= TOL_ROOT,
                "none" if r is None else f"{r:.9f}, difference {r - ROOT_B:+.3e}"))
    return out


def r2(pts):
    """-> dict: pair, root, delta, E, verdict, lines"""
    lams = sorted(pts)
    pairs = [(x, y) for x, y in zip(lams, lams[1:]) if ok(pts[x]) and ok(pts[y]) and pts[x]["sign"] != pts[y]["sign"]]
    res = {"pairs": pairs, "notes": []}
    bad = [l for l in lams if not ok(pts[l])]
    if bad:
        res["notes"].append(f"non-robust points {bad}: not used")
    if not pairs:
        res.update(pair=None, root=None, delta=None, E=None, verdict="no pair brackets: report and wait")
        return res
    pair = (0.045, 0.050) if (0.045, 0.050) in pairs else pairs[0]
    if pair != (0.045, 0.050):
        res["notes"].append("the 0.045/0.050 pair does not bracket: the estimator's bias does not cancel against state B's root")
    if len(pairs) > 1:
        res["notes"].append(f"{len(pairs)} bracketing pairs {pairs}: the first one is used, the others reported")
    root = lin(pts[pair[0]], pts[pair[1]])
    delta = root - ROOT_B
    E = delta * (1 if MUTATE == "e16" else 16 / 15)
    if abs(E) >= BAR_HI:
        v = f"|E_root| >= {BAR_HI:g}: the step error is real; thresholds must be extrapolated in kappa as well as k_c; the k_c-only zeros are withdrawn"
    elif abs(E) <= BAR_LO:
        v = f"|E_root| <= {BAR_LO:g}: the step error does not drive the late k_c steps; #1103's inference fails"
    else:
        v = f"between {BAR_LO:g} and {BAR_HI:g}: mixed, reported as measured"
    res.update(pair=pair, root=root, delta=delta, E=E, verdict=v)
    return res


def plant(lam, r, c=1.0, sign=None):
    """a record of a determinant linear in lambda: det = c (r - lam)"""
    d = c * (r - lam)
    return {"lam": lam, "sign": (1.0 if d > 0 else -1.0) if sign is None else sign, "ln": math.log(abs(d)), "dln": 1e-6, "noise_robust": True,
            "robust": True, "f64_sign": 1.0, "sec": 0, "b12": "rust"}


def selftest():
    bad = []

    def chk(name, cond):
        print(("pass " if cond else "FAIL ") + name)
        if not cond:
            bad.append(name)
    # control, dh370's own numbers: the root must come back as 0.045967998 and every bar pass
    pa = {"lam": 0.045, "sign": 1.0, "ln": REF_LN[0.045], "dln": 1.5e-5, "noise_robust": True, "robust": True, "f64_sign": -1.0, "sec": 0, "b12": "rust"}
    pb = {"lam": 0.050, "sign": -1.0, "ln": REF_LN[0.050], "dln": 2.5e-6, "noise_robust": True, "robust": True, "f64_sign": -1.0, "sec": 0, "b12": "rust"}
    if MUTATE == "shift":
        pa["ln"] += 2e-4
    if MUTATE == "signs":
        pb["sign"] = 1.0
    c = control({0.045: pa, 0.050: pb})
    chk("control passes on dh370's numbers", all(p for _, p, _ in c))
    chk("control root = 0.045967998 to 1e-8", lin(pa, pb) is not None and abs(lin(pa, pb) - ROOT_B) < 1e-8)
    c2 = control({0.045: dict(pa, ln=pa["ln"] + 2e-4), 0.050: pb})
    chk("control fails with ln|det| off by 2e-4", not all(p for _, p, _ in c2))
    c3 = control({0.045: pa, 0.050: dict(pb, sign=1.0)})
    chk("control fails with equal signs", not all(p for _, p, _ in c3))
    c4 = control({0.045: pa, 0.050: dict(pb, b12="ddm")})
    chk("control fails when a record is not the Rust block", not all(p for _, p, _ in c4))
    # planted roots recovered exactly from a linear det
    chk("planted root 0.0462 recovered", abs(lin(plant(0.045, 0.0462), plant(0.050, 0.0462)) - 0.0462) < 1e-12)
    # r2 verdicts at planted roots (0.045/0.050 pair brackets), E = delta * 16/15
    for dlt, want in ((6e-4, "fails"), (9.5e-4, "mixed"), (2.0e-3, "mixed"), (2.9e-3, "real"), (4.0e-3, "real")):
        out = r2({l: plant(l, ROOT_B + dlt) for l in (0.045, 0.050, 0.060, 0.070)})
        got = "real" if "step error is real" in out["verdict"] else "fails" if "inference fails" in out["verdict"] else "mixed" if "mixed" in out["verdict"] else out["verdict"]
        chk(f"R2 verdict at planted delta {dlt:g}: {want}", got == want and out["pair"] == (0.045, 0.050))
    # root near 0.065: only the 0.060/0.070 pair brackets
    pts = {l: plant(l, 0.065) for l in (0.045, 0.050, 0.060, 0.070)}
    out = r2(pts)
    chk("root 0.065: the 0.060/0.070 pair is used and recovered", out["pair"] == (0.060, 0.070) and abs(out["root"] - 0.065) < 1e-12)
    # no bracket
    out = r2({l: plant(l, 0.2) for l in (0.045, 0.050, 0.060, 0.070)})
    chk("no sign change: no pair brackets", out["pair"] is None and "wait" in out["verdict"])
    # a non-robust end is not used
    pts = {l: plant(l, 0.0475) for l in (0.045, 0.050, 0.060, 0.070)}
    pts[0.050]["robust"] = False
    out = r2(pts)
    chk("a non-robust point is not used", out["pair"] != (0.045, 0.050))
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
    pts = load(args[1])
    table(pts)
    print()
    if args[0] == "control":
        res = control(pts)
        for bar, p, t in res:
            print(f"- {'PASS' if p else 'FAIL'}: {bar}: {t}")
        sys.exit(0 if all(p for _, p, _ in res) else 1)
    if args[0] == "r2":
        out = r2(pts)
        for n in out["notes"]:
            print(f"- note: {n}")
        if out["pair"] is None:
            print(f"- {out['verdict']}")
            sys.exit(2)
        print(f"- pair {out['pair']}: det-linear root {out['root']:.9f}")
        print(f"- delta = root(R2) - root(B) = {out['delta']:+.6e} (root(B) = {ROOT_B})")
        print(f"- E_root = delta x 16/15 = {out['E']:+.6e}")
        print(f"- verdict: {out['verdict']}")
        sys.exit(0)
    sys.exit(__doc__)
