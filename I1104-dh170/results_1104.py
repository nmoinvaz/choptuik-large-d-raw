"""#1104 dh170 (t5's order, comment 7226665371): reads the scans of macm3's k_c 127 D 23.125 state at kappa 0.7 (the source) and at kappa 0.5 (the re-solve), their
secant roots, and forms delta(23.125) = root(kappa 0.5) - root(kappa 0.7) against delta(23.0) = +0.04904 (README, "Bars").

usage: results_1104.py scan SCANDIR... [--pair]
           the points of the folders together (scan_*_p*.jsonl); the first robust change (the lowest lambda, the others listed) gives the bracket;
           exit 0 a change, 2 no robust change; --pair prints "LO HI" only
       results_1104.py read --scan070=DIR --scan050=DIR --s070=FILE --s050=FILE
           the two secant records (d18_secant.py run, tol 5e-5) and the verdict; exit 0 formed, 4 a record is not read
       results_1104.py selftest [--mutate=sign|bar|ref|last]    planted cases; exit 0 only if each reads as written

A secant record is read only if its status is tol, both ends robust and of opposite hybrid signs, inside the scan's pair. The root is lam_lin (det-linear inside the
final bracket). delta is read on the ranges [a - d, b - c] of the final brackets [a, b] (kappa 0.5) and [c, d] (kappa 0.7): the whole range of delta / 0.04904 inside
0.9 .. 1.1 is 'equal within 10%', the whole range outside it 'not equal within 10%', anything else 'between, reported as measured'."""
import glob
import json
import math
import sys

DELTA_230 = 0.09500769 - 0.045967998      # R1 - R0 at D 23.0 (t5's #1101 comments): +0.04904
TOL = 0.10
MACM3_ROOT = -0.0419                      # macm3's kappa 0.7 root at D 23.125 (#1025), for the printout only
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


def changes(pts):
    lams = sorted(pts)
    return [(x, y) for x, y in zip(lams, lams[1:]) if ok(pts[x]) and ok(pts[y]) and pts[x]["sign"] != pts[y]["sign"]]


def first_pair(pts):
    ch = changes(pts)
    if not ch:
        return None, ch
    return (ch[-1] if MUTATE == "last" else ch[0]), ch


def table(pts):
    print("| lambda | hybrid sign | noise-robust | robust (dln <= 0.1) | dln | float64 sign | ln\\|det\\| | b12 | seconds |")
    print("|---|---|---|---|---|---|---|---|---|")
    for lam in sorted(pts):
        w = pts[lam]
        print(f"| {lam:+.3f} | {w['sign']:+.0f} | {w['noise_robust']} | {w.get('robust')} | {w['dln']:.2e} | {w['f64_sign']:+.0f} "
              f"| {w['ln']:.10f} | {w.get('b12')} | {w['sec']} |")


def readable(rec, pair=None):
    """-> (True, '') or (False, why)"""
    if rec is None or rec.get("kind") != "root":
        return False, "no root record"
    if rec.get("status") != "tol" or not all(rec["robust"]) or rec["signs"][0] == rec["signs"][1]:
        return False, f"status {rec.get('status')}, robust {rec['robust']}, signs {rec['signs']}"
    if pair is not None and not (pair[0] - 1e-9 <= rec["bracket"][0] and rec["bracket"][1] <= pair[1] + 1e-9):
        return False, f"bracket {rec['bracket']} outside the scan's {pair}"
    return True, ""


def compare(k5, k7):
    """k5, k7: root records (kappa 0.5, kappa 0.7) -> dict(diff, lo, hi, rlo, rhi, verdict)"""
    ref = k7
    if MUTATE == "ref":
        ref = dict(k7, lam_lin=MACM3_ROOT, bracket=[MACM3_ROOT, MACM3_ROOT])         # macm3's value instead of the re-measured root
    a, b = k5["bracket"]
    c, d = ref["bracket"]
    lo, hi = a - d, b - c
    sgn = -1.0 if MUTATE == "sign" else 1.0
    if sgn < 0:
        lo, hi = -hi, -lo
    tol = 1.0 if MUTATE == "bar" else TOL
    rlo, rhi = lo / DELTA_230, hi / DELTA_230
    if 1 - tol <= rlo and rhi <= 1 + tol:
        v = f"delta(23.125) equal to delta(23.0) = {DELTA_230:+.5f} within {TOL:.0%}: the correction is D-independent near the zero; the kappa-corrected zero follows from one more D"
    elif rhi < 1 - tol or rlo > 1 + tol:
        v = f"delta(23.125) not equal to delta(23.0) within {TOL:.0%} (ratio {rlo:.3f} .. {rhi:.3f}): reported as measured"
    else:
        v = f"between: the ratio range {rlo:.3f} .. {rhi:.3f} straddles {1 - TOL:.2f} or {1 + TOL:.2f}: reported as measured"
    return dict(diff=sgn * (k5["lam_lin"] - ref["lam_lin"]), lo=lo, hi=hi, rlo=rlo, rhi=rhi, verdict=v)


def read(pts7, pts5, s7=None, s5=None):
    """-> dict(status, pair7, pair5, cmp, verdict)"""
    p7, ch7 = first_pair(pts7)
    p5, ch5 = first_pair(pts5)
    res = dict(pair7=p7, pair5=p5, changes7=ch7, changes5=ch5, cmp=None, status="", verdict="")
    if p7 is None or p5 is None:
        res.update(status="nochange", verdict="no robust change in the kappa 0.7 scan" if p7 is None else "no robust change in the kappa 0.5 scan")
        return res
    for name, rec, pair in (("kappa 0.7", s7, p7), ("kappa 0.5", s5, p5)):
        g, why = readable(rec, pair)
        if not g:
            res.update(status="notread", verdict=f"the {name} secant record is not read: {why}")
            return res
    res.update(status="formed", cmp=compare(s5, s7))
    res["verdict"] = res["cmp"]["verdict"]
    return res


def plant(lam, r, c=1.0):
    d = c * (r - lam)
    return {"lam": lam, "sign": 1.0 if d > 0 else -1.0, "ln": math.log(abs(d)), "dln": 1e-6, "noise_robust": True, "robust": True, "f64_sign": 1.0, "sec": 0, "b12": "rust"}


def rootrec(lam, w=5e-5, status="tol", signs=(1.0, -1.0)):
    return dict(kind="root", status=status, bracket=[lam - w / 2, lam + w / 2], width=w, signs=list(signs), robust=[True, True], lam_lin=lam, lam_brent=lam, n_eval=9)


def selftest():
    bad = []

    def chk(name, cond):
        print(("pass " if cond else "FAIL ") + name)
        if not cond:
            bad.append(name)
    r7 = -0.0430                               # not macm3's value, so that the ref mutation moves the ratio
    for ratio, want in ((1.0, "equal"), (0.95, "equal"), (1.09, "equal"), (0.91, "equal"), (0.8, "not"), (1.3, "not"), (0.0, "not"), (-1.0, "not"), (0.9, "between"), (1.1, "between")):
        t = compare(rootrec(r7 + ratio * DELTA_230), rootrec(r7))["verdict"]
        got = "equal" if t.startswith("delta(23.125) equal") else "not" if "not equal" in t else "between" if t.startswith("between") else t
        chk(f"planted delta/delta(23.0) = {ratio}: {want}", got == want)
    # a wide bracket on a ratio of 1.095 straddles 1.1: between
    t = compare(rootrec(r7 + 1.095 * DELTA_230, 1e-3), rootrec(r7))["verdict"]
    chk("a 1e-3 bracket on ratio 1.095 straddles 1.10: between", t.startswith("between"))
    # a planted pair of scans: kappa 0.7 root -0.0419, kappa 0.5 root +0.0071
    pts7 = {l: plant(l, r7) for l in (-0.045, -0.040)}
    pts5 = {l: plant(l, r7 + DELTA_230) for l in (-0.02, -0.005, 0.01, 0.025)}
    r = read(pts7, pts5, rootrec(r7), rootrec(r7 + DELTA_230))
    chk("planted scans and secants at ratio 1: formed, equal", r["status"] == "formed" and r["verdict"].startswith("delta(23.125) equal"))
    chk("the pairs are (-0.045, -0.04) and (-0.005, 0.01)", r["pair7"] == (-0.045, -0.04) and r["pair5"] == (-0.005, 0.01))
    r = read(pts7, pts5, rootrec(r7), rootrec(0.02))
    chk("a kappa 0.5 secant root outside the scan's pair: not read", r["status"] == "notread")
    r = read(pts7, pts5, rootrec(r7, status="nonrobust"), rootrec(r7 + DELTA_230))
    chk("the kappa 0.7 record not tol: not read", r["status"] == "notread")
    r = read(pts7, pts5, rootrec(r7), rootrec(r7 + DELTA_230, signs=(1.0, 1.0)))
    chk("same-signed ends: not read", r["status"] == "notread")
    r = read({l: plant(l, 0.2) for l in (-0.045, -0.04)}, pts5)
    chk("no root in the kappa 0.7 scan: no change", r["status"] == "nochange")
    pts2 = {l: dict(plant(l, 0.0), sign=sg) for l, sg in ((-0.02, 1.0), (-0.005, -1.0), (0.01, -1.0), (0.025, 1.0))}
    p, ch = first_pair(pts2)
    chk("two changes: the lowest-lambda pair is the bracket", len(ch) == 2 and p == ch[0])
    bad_pt = dict(plant(-0.005, 0.0), robust=False)
    chk("a non-robust point makes no change at its pair", (-0.02, -0.005) not in changes({**{l: plant(l, 0.0) for l in (-0.02, 0.01)}, -0.005: bad_pt}))
    print("selftest:", "FAIL " + "; ".join(bad) if bad else "all cases read as written")
    return 1 if bad else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for a in sys.argv[1:]:
        if a.startswith("--mutate="):
            MUTATE = a.split("=", 1)[1]
    opt = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--") and "=" in a}
    if not args:
        sys.exit(__doc__)
    if args[0] == "selftest":
        sys.exit(selftest())

    def lastroot(path):
        rows = [json.loads(l) for l in open(path) if l.strip()]
        rows = [r for r in rows if r.get("kind") == "root"]
        return rows[-1] if rows else None
    if args[0] == "scan":
        pts = load(*args[1:])
        pair, ch = first_pair(pts)
        if "--pair" in sys.argv:
            if pair is None:
                sys.exit(2)
            print(f"{pair[0]:g} {pair[1]:g}")
            sys.exit(0)
        table(pts)
        print()
        bad = [l for l in sorted(pts) if not ok(pts[l])]
        if bad:
            print(f"- note: non-robust points {bad}: not used")
        print(f"- robust changes: {ch if ch else 'none'}")
        if pair is None:
            print(f"- no robust change in [{min(pts):g}, {max(pts):g}]: reported as measured")
            sys.exit(2)
        if len(ch) > 1:
            print(f"- note: {len(ch)} robust changes: the lowest-lambda one gives the bracket, the others are reported")
        print(f"- bracket (first robust change): {pair}")
        sys.exit(0)
    if args[0] == "read":
        pts7, pts5 = load(opt["--scan070"]), load(opt["--scan050"])
        s7, s5 = lastroot(opt["--s070"]), lastroot(opt["--s050"])
        out = read(pts7, pts5, s7, s5)
        if out["status"] != "formed":
            print(f"- {out['verdict']}")
            sys.exit(4 if out["status"] == "notread" else 2)
        c = out["cmp"]
        print(f"- kappa 0.7 root (lam_lin of {opt['--s070']}): {s7['lam_lin']:.9f}, final bracket ({s7['bracket'][0]!r}, {s7['bracket'][1]!r}); macm3's {MACM3_ROOT} differs by {s7['lam_lin'] - MACM3_ROOT:+.4f}")
        print(f"- kappa 0.5 root (lam_lin of {opt['--s050']}): {s5['lam_lin']:.9f}, final bracket ({s5['bracket'][0]!r}, {s5['bracket'][1]!r}); sign {'+' if s5['lam_lin'] > 0 else '-'}")
        print(f"- delta(23.125) = root(kappa 0.5) - root(kappa 0.7) = {c['diff']:+.6e}; range from the brackets {c['lo']:+.6e} .. {c['hi']:+.6e}; "
              f"ratio to delta(23.0) = {DELTA_230:+.6f}: {c['diff'] / DELTA_230:.4f} (range {c['rlo']:.4f} .. {c['rhi']:.4f})")
        print(f"- verdict: {c['verdict']}")
        sys.exit(0)
    sys.exit(__doc__)
