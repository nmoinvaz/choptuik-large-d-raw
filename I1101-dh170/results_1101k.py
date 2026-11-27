"""#1101 dh170, Test K (t5's order, comment 7222591656): reads the scan of state B (R0's re-solve at kappa 0.7) with d18_secant.py --kappa_mm=0.35, its
secant root, and compares the root with R2's own secant root against t5's bars in README.md ("Test K").

usage: results_1101k.py scan SCANDIR... [--secant=FILE] [--r2=FILE] [--pair]
           the points of the folders together (scan_*_p*.jsonl); the first robust sign change (the lowest lambda, the others listed) gives the bracket;
           with the Test K secant record (d18_secant.py run, tol 5e-5) and R2's secant record, the difference of the roots and the verdict.
           exit 0 formed, 2 no robust change, 3 a change and no secant record yet, 4 a record is not read; --pair prints "LO HI" only
       results_1101k.py steps FILE...        the 'kappa_mm' lines of the scans' raw output against the expected step count (8351 +- 2%); exit 0 if all pass
       results_1101k.py selftest [--mutate=ref|bar|last]    planted cases; exit 0 only if each reads as written

A secant record is read only if its status is tol, both ends robust and of opposite hybrid signs (for the Test K record also inside the scan's bracket).
The root is lam_lin (det-linear inside the final bracket). The difference is read on the ranges [a - d, b - c] of the final brackets [a, b] (Test K) and
[c, d] (R2): within +-3e-3 over the whole range is 'the step error is the mode matrix's'; at least 1e-2 in size over the whole range is 'the state's kappa
matters too'; anything else is 'between, reported as measured'."""
import glob
import json
import math
import re
import sys

BAR_IN, BAR_OUT = 3e-3, 1e-2          # t5's bars on |root - r2|
STEPS, STEPS_TOL = 8351, 0.02         # R2's record steps at kappa 0.35; the line must be within 2%
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


def table(pts):
    print("| lambda | hybrid sign | noise-robust | robust (dln <= 0.1) | dln | float64 sign | ln\\|det\\| | b12 | seconds |")
    print("|---|---|---|---|---|---|---|---|---|")
    for lam in sorted(pts):
        w = pts[lam]
        print(f"| {lam:.3f} | {w['sign']:+.0f} | {w['noise_robust']} | {w.get('robust')} | {w['dln']:.2e} | {w['f64_sign']:+.0f} "
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


def compare(k, r2):
    """k, r2: root records -> dict(diff, lo, hi, verdict)"""
    ref = r2
    if MUTATE == "ref":
        ref = dict(r2, lam_lin=0.045967998, bracket=[0.045967998, 0.045967998])        # B's own kappa 0.7 root instead of R2's
    a, b = k["bracket"]
    c, d = ref["bracket"]
    lo, hi = a - d, b - c
    bi, bo = (BAR_IN * 10, BAR_OUT * 10) if MUTATE == "bar" else (BAR_IN, BAR_OUT)
    if -bi <= lo and hi <= bi:
        v = (f"|root - r2| <= {BAR_IN:g} over the whole range: the state's kappa does not matter, the step error is the mode matrix's; "
             "#1104 uses --kappa_mm on the stored states, without re-solves")
    elif lo >= bo or hi <= -bo:
        v = f"|root - r2| >= {BAR_OUT:g} over the whole range: the state's kappa matters too"
    else:
        v = f"between {BAR_IN:g} and {BAR_OUT:g}, or a range that straddles a bar: reported as measured"
    return dict(diff=k["lam_lin"] - ref["lam_lin"], lo=lo, hi=hi, verdict=v)


def read(pts, secant=None, r2rec=None):
    """-> dict(status, changes, pair, cmp, notes, verdict)"""
    ch = changes(pts)
    res = dict(changes=ch, pair=None, cmp=None, notes=[], verdict="", status="")
    bad = [l for l in sorted(pts) if not ok(pts[l])]
    if bad:
        res["notes"].append(f"non-robust points {bad}: not used")
    if not ch:
        res.update(status="nochange", verdict=f"no robust change in [{min(pts):g}, {max(pts):g}]: reported as measured")
        return res
    res["pair"] = pair = ch[-1] if MUTATE == "last" else ch[0]
    if len(ch) > 1:
        res["notes"].append(f"{len(ch)} robust changes {ch}: the lowest-lambda one gives the bracket, the others are reported")
    if secant is None:
        res.update(status="nosecant", verdict=f"bracket {pair}: run d18_secant.py run on it at tol 5e-5")
        return res
    g, why = readable(secant, pair)
    if not g:
        res.update(status="notread", verdict=f"the Test K secant record is not read: {why}")
        return res
    g, why = readable(r2rec)
    if not g:
        res.update(status="notread", verdict=f"R2's secant record is not read: {why}; its robust bracket bounds the difference only outside the rule")
        return res
    res.update(status="formed", cmp=compare(secant, r2rec), verdict="")
    res["verdict"] = res["cmp"]["verdict"]
    return res


def steps_check(paths):
    out = []
    for p in paths:
        txt = open(p).read()
        m = re.search(r"kappa_mm ([\d.]+): the mode matrix on the steps of kappa [\d.]+, (\d+) steps \(the record's kappa ([\d.]+): (\d+)\)", txt)
        if not m:
            out.append((p, False, "no kappa_mm line"))
            continue
        n = int(m.group(2))
        out.append((p, abs(n - STEPS) <= STEPS_TOL * STEPS, f"kappa_mm {m.group(1)}: {n} steps (record kappa {m.group(3)}: {m.group(4)}); wanted {STEPS} +- {STEPS_TOL:.0%}"))
    return out


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
    r2 = 0.115
    for diff, want in ((0.0, "within"), (2.5e-3, "within"), (-2.5e-3, "within"), (2.99e-3, "between"), (5e-3, "between"), (-9.9e-3, "between"),
                       (1.01e-2, "outside"), (-1.01e-2, "outside"), (0.07, "outside")):
        t = compare(rootrec(r2 + diff), rootrec(r2))["verdict"]
        got = "within" if "does not matter" in t else "outside" if "matters too" in t else "between" if "between" in t else t
        chk(f"planted root - r2 = {diff:+.3g}: {want}", got == want)
    # a wide bracket straddling a bar is not read as within
    chk("a 4e-3 bracket on 1e-3 straddles 3e-3: between", "between" in compare(rootrec(r2 + 1e-3, 4e-3), rootrec(r2))["verdict"])
    # planted scans through read(): the first change, no change, no secant, a secant outside the pair, R2's secant not tol
    pts = {l: plant(l, 0.1025) for l in (0.085, 0.100, 0.115, 0.130)}
    r = read(pts)
    chk("planted root 0.1025: the change is (0.100, 0.115)", r["changes"] == [(0.1, 0.115)] and r["status"] == "nosecant")
    r = read(pts, rootrec(0.1025), rootrec(r2))
    chk("planted secant inside the pair, R2 tol: formed", r["status"] == "formed" and abs(r["cmp"]["diff"] - (0.1025 - r2)) < 1e-12)
    r = read(pts, rootrec(0.125), rootrec(r2))
    chk("a secant root outside the scan's pair: not read", r["status"] == "notread")
    r = read(pts, rootrec(0.1025), rootrec(r2, status="nonrobust"))
    chk("R2's record not tol: not read", r["status"] == "notread")
    r = read(pts, rootrec(0.1025, signs=(1.0, 1.0)), rootrec(r2))
    chk("same-signed ends: not read", r["status"] == "notread")
    r = read({l: plant(l, 0.2) for l in (0.085, 0.100, 0.115, 0.130)})
    chk("no root in the scan: no change", r["status"] == "nochange")
    pts2 = {l: dict(plant(l, 0.1025), sign=sg) for l, sg in ((0.085, 1.0), (0.100, -1.0), (0.115, -1.0), (0.130, 1.0))}
    r = read(pts2)
    chk("two changes: the lowest-lambda pair is the bracket", len(r["changes"]) == 2 and r["pair"] == r["changes"][0])
    bad_pt = dict(plant(0.1, 0.1025), robust=False)
    r = read({**pts, 0.1: bad_pt})
    chk("a non-robust point makes no change at its pair", (0.1, 0.115) not in r["changes"])
    # the steps line
    import os
    import tempfile
    d = tempfile.mkdtemp()
    for name, n in (("ok", 8351), ("edge", 8351 + 160), ("bad", 8351 + 200), ("low", 4175)):
        open(f"{d}/{name}.raw", "w").write(f"kappa_mm 0.35: the mode matrix on the steps of kappa 0.35, {n} steps (the record's kappa 0.7: 4175); the state and its record system are unchanged\n")
    open(f"{d}/none.raw", "w").write("D 23.0 k_c 127: |F| 3e-10\n")
    res = {os.path.basename(p): g for p, g, _ in steps_check(sorted(glob.glob(f"{d}/*.raw")))}
    chk("steps 8351: pass", res["ok.raw"])
    chk("steps 8511 (+1.9%): pass", res["edge.raw"])
    chk("steps 8551 (+2.4%): fail", not res["bad.raw"])
    chk("steps 4175 (the record's own): fail", not res["low.raw"])
    chk("no kappa_mm line: fail", not res["none.raw"])
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
    if args[0] == "steps":
        res = steps_check(args[1:])
        for p, g, t in res:
            print(f"- {'PASS' if g else 'FAIL'}: {p}: {t}")
        sys.exit(0 if all(g for _, g, _ in res) else 1)
    if args[0] == "scan":
        def lastroot(path):
            rows = [json.loads(l) for l in open(path) if l.strip()]
            rows = [r for r in rows if r.get("kind") == "root"]
            return rows[-1] if rows else None
        opt = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--") and "=" in a}
        pts = load(*args[1:])
        out = read(pts, lastroot(opt["--secant"]) if "--secant" in opt else None, lastroot(opt["--r2"]) if "--r2" in opt else None)
        if "--pair" in sys.argv:
            if out["pair"] is None:
                sys.exit(2)
            print(f"{out['pair'][0]:g} {out['pair'][1]:g}")
            sys.exit(0)
        table(pts)
        print()
        for n in out["notes"]:
            print(f"- note: {n}")
        print(f"- robust changes: {out['changes'] if out['changes'] else 'none'}")
        if out["status"] == "nochange":
            print(f"- {out['verdict']}")
            sys.exit(2)
        print(f"- bracket (first robust change): {out['pair']}")
        if out["status"] == "nosecant":
            print(f"- {out['verdict']}")
            sys.exit(3)
        if out["status"] == "notread":
            print(f"- {out['verdict']}")
            sys.exit(4)
        c = out["cmp"]
        k, r = lastroot(opt["--secant"]), lastroot(opt["--r2"])
        print(f"- Test K secant root (lam_lin of {opt['--secant']}): {k['lam_lin']:.9f}, final bracket ({k['bracket'][0]!r}, {k['bracket'][1]!r})")
        print(f"- R2's secant root (lam_lin of {opt['--r2']}): {r['lam_lin']:.9f}, final bracket ({r['bracket'][0]!r}, {r['bracket'][1]!r})")
        print(f"- root(K) - root(R2) = {c['diff']:+.6e}; range from the brackets {c['lo']:+.6e} .. {c['hi']:+.6e}")
        print(f"- verdict: {c['verdict']}")
        sys.exit(0)
    sys.exit(__doc__)
