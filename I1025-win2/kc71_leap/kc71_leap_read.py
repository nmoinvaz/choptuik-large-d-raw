#!/usr/bin/env python3
"""kc71_leap_read.py DIR D PATH | --selftest [--break]: the reading of one D of #1025 kc71_leap (the coordinator's hc of 2026-11-22 ~03:00 UTC): the hybrid scan of lambda LO to HI at 0.01 at k_c 71 (scan_D<D>_P1..P4.jsonl in DIR),
four processes, the pairs (P1, P2) and (P3, P4) each repeating one point (the check lambdas in checks_D<D>.json) evaluated first in both. xfkappa's reader (the pinned d18d_read.py 6b608903) reads the four files together.
THE READING (fixed before the run): the robust minus-to-plus root nearest the extrapolated path PATH is lambda_1 at that D; its delta against lambda_0(D) (ell_delta.lam0_at) is reported. "A missing root, or two within 0.03, is reported,
not read": there is NO minus-to-plus robust root in the window; or two or more minus-to-plus robust roots are within 0.03 of PATH; or two robust roots (of either orientation) are within 0.03 of each other and one of them is the nearest to PATH
(a near-tangent pair). In those cases every root is listed and no lambda_1 is read. The distance of the root to PATH is reported (no bar on it). Orientation labels are each scan's own det-sign convention; a robust root of the other orientation
nearest PATH is listed too. --selftest runs the chooser on planted root lists (a clear root, two minus-to-plus roots within 0.03 of the path, a missing minus-to-plus root, a near-tangent pair, a root far from the path) with the expected verdicts;
--break flips one expectation and must exit 1.
Added after the coordinator's rule of 2026-11-22 (hc): the scan files of a D are scan_D<D>_P1..P4.jsonl and any extension files scan_D<D>_X*.jsonl (kcl_ext.sh); the window is the lambda range of all the points; **if the root read sits within 0.03 of a
window edge, the line EDGE LOW or EDGE HIGH is printed and the window is to be extended on that side by 0.10 before the root is read** (that line means: not read yet); a repeated point that disagrees (the extension's edge point is a repeat) is STOP-level."""
import json
import os
import sys

ARGS = sys.argv[1:]
BAR = 0.03


def edge_side(x, lo, hi):
    """'low' or 'high' when x is within 0.03 of the window edge (<= 0.03), else None."""
    if x - lo <= BAR + 1e-9:
        return "low"
    if hi - x <= BAR + 1e-9:
        return "high"
    return None


def choose(roots, path):
    """roots: list of (x, orient) robust changes. Returns (verdict, root or None, why)."""
    mp = [r for r in roots if r[1] == "- to +"]
    if not mp:
        return "not read", None, "no robust minus-to-plus root in the window"
    near = sorted(mp, key=lambda r: abs(r[0] - path))
    within = [r for r in near if abs(r[0] - path) <= BAR]
    if len(within) >= 2:
        return "not read", None, "two minus-to-plus roots within 0.03 of the path: %s" % [round(r[0], 6) for r in within]
    best = near[0]
    for r in roots:
        if r is not best and abs(r[0] - best[0]) <= BAR:
            return "not read", None, "a robust root (%s) within 0.03 of the nearest minus-to-plus root %.6f: a near-tangent pair" % (r[1], best[0])
    return "read", best, "the robust minus-to-plus root nearest the path, %.6f away" % abs(best[0] - path)


def selftest(brk):
    cases = [("a clear root", [(1.55, "- to +"), (1.20, "+ to -")], 1.546, "read"),
             ("two minus-to-plus roots within 0.03 of the path", [(1.53, "- to +"), (1.56, "- to +")], 1.546, "not read"),
             ("no minus-to-plus root", [(1.60, "+ to -")], 1.546, "not read"),
             ("a near-tangent pair at the root", [(1.55, "- to +"), (1.57, "+ to -")], 1.546, "not read"),
             ("a root far from the path (read, distance reported)", [(1.75, "- to +")], 1.546, "read"),
             ("a second root beyond 0.03 of the nearest and of the path", [(1.55, "- to +"), (1.70, "- to +")], 1.546, "read")]
    ok = True
    for name, x, lo, hi, want in (("a root in the middle of the window", 1.42, 1.22, 1.62, None), ("a root 0.03 above the low edge", 1.25, 1.22, 1.62, "low"), ("a root 0.02 below the high edge", 1.60, 1.22, 1.62, "high"),
                                  ("a root 0.031 above the low edge", 1.251, 1.22, 1.62, None)):
        got = edge_side(x, lo, hi)
        if brk and name == "a root 0.03 above the low edge":
            want = None
        print("planted: %s: edge %s, expected %s: %s" % (name, got, want, "PASS" if got == want else "FAIL"))
        ok = ok and got == want
    for name, roots, path, want in cases:
        if brk and name == "a clear root":
            want = "not read"
        got = choose(roots, path)[0]
        print("planted: %s: %s, expected %s: %s" % (name, got, want, "PASS" if got == want else "FAIL"))
        ok = ok and got == want
    print("selftest: %s%s" % ("PASS" if ok else "FAIL", " [break]" if brk else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    if ARGS and ARGS[0] == "--selftest":
        sys.exit(selftest("--break" in ARGS))
    H = ARGS[0].replace("\\", "/").rstrip("/") + "/"
    D, PATH = float(ARGS[1]), float(ARGS[2])
    PIN = "D:/choptuik-i935-raw/I1025-win2/d18mid/pinned"
    WTM = "D:/choptuik-i1025k71/solver/matter"
    sys.path.insert(0, PIN)
    import d18d_read as rr  # noqa: E402
    sys.path.insert(0, WTM)
    import ell_delta  # noqa: E402
    tag = ("%g" % D)
    import glob
    files = [H + "scan_D%s_P%d.jsonl" % (tag, i) for i in (1, 2, 3, 4)] + sorted(glob.glob(H + "scan_D%s_X*.jsonl" % tag))
    rows = []
    for f in files:
        if os.path.exists(f):
            rows += [json.loads(x) for x in open(f) if x.strip()]
    checks = json.load(open(H + "checks_D%s.json" % tag))
    print("D %s, k_c 71, path %.6f, files %s" % (tag, PATH, [os.path.basename(f) for f in files]))
    ok = True
    for a, b, lam in ((1, 2, checks["c12"]), (3, 4, checks["c34"])):
        ra = next((json.loads(x) for x in open(files[a - 1]) if x.strip() and abs(json.loads(x)["lam"] - lam) < 1e-9), None) if os.path.exists(files[a - 1]) else None
        rb = next((json.loads(x) for x in open(files[b - 1]) if x.strip() and abs(json.loads(x)["lam"] - lam) < 1e-9), None) if os.path.exists(files[b - 1]) else None
        if ra and rb:
            g = ra["sign"] == rb["sign"] and abs(ra["ln"] - rb["ln"]) <= 1e-6
            ok = ok and g
            print("repeat %.2f (P%d, P%d): %+d %.10f and %+d %.10f, difference %+.2e (bar 1e-6): %s" % (lam, a, b, ra["sign"], ra["ln"], rb["sign"], rb["ln"], rb["ln"] - ra["ln"], "agree" if g else "DISAGREE"))
        else:
            ok = False
            print("repeat %.2f (P%d, P%d): missing" % (lam, a, b))
    if not ok:
        print("STOP-level: a repeated point does not agree or is missing: no reading")
        sys.exit(3)
    l0, l0e = ell_delta.lam0_at(D, *ell_delta.lam0_table())
    S, rep = rr.merge(rows)
    print("lambda_0(D %s) = %.10f (error %.1e); %d points, %.2f to %.2f" % (tag, l0, l0e, len(S), S[0]["lam"], S[-1]["lam"]))
    res = rr.read(S, rep, None, print, l0=l0)
    fc = [(a["lam"], b["lam"]) for a, b in zip(S, S[1:]) if a["f64_sign"] != b["f64_sign"]]
    print("float64 sign changes: %d in %s; float64 differs from the hybrid at %d of %d points" % (len(fc), [(round(a, 2), round(b, 2)) for a, b in fc], len([x for x in S if x["f64_sign"] != x["sign"]]), len(S)))
    if res["v"] == "repeat disagrees":
        print("NOT READ: a repeated point disagrees with its earlier evaluation (STOP-level)")
        sys.exit(3)
    roots = [(x["lin"], x["orient"]) for x in res["roots"]]
    LO, HI = S[0]["lam"], S[-1]["lam"]
    print("window: lambda %.2f to %.2f (%d points)" % (LO, HI, len(S)))
    verdict, best, why = choose(roots, PATH)
    print()
    print("THE READING (fixed before the run): the robust minus-to-plus root nearest the extrapolated path %.6f is lambda_1 at D %s; two within 0.03 or a missing root: reported, not read" % (PATH, tag))
    for x in res["roots"]:
        print("  robust root in (%.2f, %.2f), %s: det-linear %.6f, range [%.6f, %.6f], %+.6f from the path, delta from lambda_0 %+.6f" % (x["br"][0], x["br"][1], x["orient"], x["lin"], x["lo"], x["hi"], x["lin"] - PATH, x["lin"] - l0))
    if verdict == "read":
        print("LAMBDA_1: %.6f (bracket (%.2f, %.2f), range [%.6f, %.6f]), %s; delta against lambda_0 = %+.6f" % (
            best[0], *next(x["br"] for x in res["roots"] if x["lin"] == best[0]), *next((x["lo"], x["hi"]) for x in res["roots"] if x["lin"] == best[0]), why, best[0] - l0))
        side = edge_side(best[0], LO, HI)
        if side:
            print("EDGE %s: the root read (%.6f) is within 0.03 of the window's %s edge (%.2f): the rule says extend that side by 0.10 and read again; NOT READ YET" % (side.upper(), best[0], side, LO if side == "low" else HI))
    else:
        print("NOT READ: " + why)
