#!/usr/bin/env python3
"""kc71_read.py [DIR] | --selftest [--break]: the reading of #1025 kc71_d185 (the coordinator's hc of 2026-11-21 ~23:05 UTC): D 18.5 at k_c 71, lambda 1.55 to 2.49 at 0.02 (48 points), four processes P1..P4 (scan_P1.jsonl ... scan_P4.jsonl in DIR),
the pairs (P1, P2) and (P3, P4) each sharing one repeated point (1.77 and 2.25) evaluated first in both. xfkappa's reader (d18d_read.py, the pinned copy in ../d18mid/pinned, blob 6b608903) reads the four files together: every robust
sign change with its bracket, orientation and estimator range, every ln|det| local minimum without a change, the float64 sign beside, and the repeated points (same sign, ln|det| within 1e-6: same machine, same code).
THE READING (fixed before the run): a k_c 71 root is its det-linear estimate x71. It is 63-near if |x71 - r63| <= 0.02 for a k_c 63 root r63 and |x71 - r55| > 0.02 for every k_c 55 root; 55-near the reverse; neither otherwise.
The reference roots (D 18.5, det-linear estimates by the same reader): k_c 63 1.677016 (- to +) and 2.420394 (+ to -) (xfkappa's three scans plus win2's windows of ../d185map, inputs/kc63_*), k_c 55 1.873934 (- to +) and 2.213669 (+ to -)
(win2b's merged scan, inputs/kc55_scan_merged.jsonl); recomputed here from the input files and checked against these numbers (a control). Overall: every k_c 71 root 63-near (and at least one): k_c 63 is nearer convergence; every root 55-near: k_c 55 is nearer;
anything else (a root near neither, a mix, or no root): neither, not converged at these k_c; each root is listed with its class. Orientation is reported and not compared across k_c.
--selftest runs the classifier on planted root lists (63-near, 55-near, neither, mixed, none) with the expected verdicts, exit 0 when all are as written; --break flips one expectation and must exit 1."""
import json
import os
import sys

ARGS = sys.argv[1:]
R63 = (1.677016, 2.420394)
R55 = (1.873934, 2.213669)
BAR = 0.02


def classify(x, r63=R63, r55=R55):
    d63 = min(abs(x - r) for r in r63)
    d55 = min(abs(x - r) for r in r55)
    if d63 <= BAR and d55 > BAR:
        return "63-near", d63, d55
    if d55 <= BAR and d63 > BAR:
        return "55-near", d63, d55
    if d63 <= BAR and d55 <= BAR:
        return "both", d63, d55
    return "neither", d63, d55


def overall(xs):
    cl = [classify(x)[0] for x in xs]
    if not cl:
        return "neither: no k_c 71 root in the window (not converged at these k_c)"
    if all(c == "63-near" for c in cl):
        return "k_c 63 is nearer convergence (every k_c 71 root is within 0.02 of a k_c 63 root and not of a k_c 55 root)"
    if all(c == "55-near" for c in cl):
        return "k_c 55 is nearer convergence (every k_c 71 root is within 0.02 of a k_c 55 root and not of a k_c 63 root)"
    return "neither: not converged at these k_c (classes: %s)" % ", ".join(cl)


def selftest(brk):
    cases = [("two roots at the k_c 63 places", [1.68, 2.42], "k_c 63 is nearer"),
             ("two roots at the k_c 55 places", [1.875, 2.215], "k_c 55 is nearer"),
             ("two roots near neither", [1.78, 2.32], "neither"),
             ("one 63-near and one 55-near root", [1.68, 2.215], "neither"),
             ("no root", [], "neither"),
             ("one root at 1.69 (within 0.02 of 1.677016), none other", [1.69], "k_c 63 is nearer"),
             ("a root at 1.70 (0.023 from 1.677016)", [1.70, 2.42], "neither")]
    ok = True
    for name, xs, want in cases:
        if brk and name == "two roots at the k_c 63 places":
            want = "k_c 55 is nearer"
        got = overall(xs)
        good = got.startswith(want)
        print("planted: %s: %s: %s" % (name, got[:60], "PASS" if good else "FAIL"))
        ok = ok and good
    print("selftest: %s%s" % ("PASS" if ok else "FAIL", " [break]" if brk else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    if ARGS and ARGS[0] == "--selftest":
        sys.exit(selftest("--break" in ARGS))
    H = (ARGS[0] if ARGS else os.path.dirname(os.path.abspath(__file__))).replace("\\", "/").rstrip("/") + "/"
    PIN = "D:/choptuik-i935-raw/I1025-win2/d18mid/pinned"
    WTM = "D:/choptuik-i1025k71/solver/matter"
    sys.path.insert(0, PIN)
    import d18d_read as rr  # noqa: E402
    sys.path.insert(0, WTM)
    import ell_delta  # noqa: E402

    def rows(files):
        out = []
        for f in files:
            if os.path.exists(f):
                out += [json.loads(x) for x in open(f) if x.strip()]
        return out

    def roots_of(files):
        S, rep = rr.merge(rows(files))
        r = rr.read(S, rep, None, lambda *a: None)
        return S, r["roots"]

    I = H + "inputs/"
    # the controls: the reference roots recomputed from the input files
    S63, r63 = roots_of([I + "d185_scan_1025.jsonl", I + "d185_scanhi_1025.jsonl", I + "d185_scanup_1025.jsonl", I + "kc63_map_A_new.jsonl", I + "kc63_map_B_new.jsonl"])
    S55, r55 = roots_of([I + "kc55_scan_merged.jsonl"])
    c63 = [round(x["lin"], 6) for x in r63]
    c55 = [round(x["lin"], 6) for x in r55]
    print("reference roots recomputed from the input files: k_c 63 %s (expected %s), k_c 55 %s (expected %s)" % (c63, list(R63), c55, list(R55)))
    if c63 != list(R63) or c55 != list(R55):
        print("CONTROL FAILED: the reference roots do not match the fixed numbers: no reading")
        sys.exit(2)
    files = [H + "scan_P%d.jsonl" % i for i in (1, 2, 3, 4)]
    print("scan files: " + ", ".join("%s %d rows" % (os.path.basename(f), len(rows([f]))) for f in files))
    pairs = []
    for a, b, lam in ((1, 2, 1.77), (3, 4, 2.25)):
        ra = next((x for x in rows([files[a - 1]]) if abs(x["lam"] - lam) < 1e-9), None)
        rb = next((x for x in rows([files[b - 1]]) if abs(x["lam"] - lam) < 1e-9), None)
        if ra and rb:
            ok = ra["sign"] == rb["sign"] and abs(ra["ln"] - rb["ln"]) <= 1e-6
            pairs.append(ok)
            print("repeat %.2f (P%d, P%d): %+d %.10f and %+d %.10f, difference %+.2e (bar 1e-6): %s" % (lam, a, b, ra["sign"], ra["ln"], rb["sign"], rb["ln"], rb["ln"] - ra["ln"], "agree" if ok else "DISAGREE"))
        else:
            pairs.append(False)
            print("repeat %.2f (P%d, P%d): missing" % (lam, a, b))
    if not all(pairs):
        print("STOP-level: a repeated point does not agree or is missing: no reading")
        sys.exit(3)
    D = 18.5
    l0, l0e = ell_delta.lam0_at(D, *ell_delta.lam0_table())
    S, rep = rr.merge(rows(files))
    print()
    print("D %g, k_c 71, files %s; lambda_0 %.10f (error %.1e)" % (D, [os.path.basename(f) for f in files], l0, l0e))
    res = rr.read(S, rep, None, print, l0=l0)
    fc = [(a["lam"], b["lam"]) for a, b in zip(S, S[1:]) if a["f64_sign"] != b["f64_sign"]]
    print("float64 sign changes: %d in %s; float64 differs from the hybrid at %d of %d points" % (len(fc), [(round(a, 2), round(b, 2)) for a, b in fc], len([x for x in S if x["f64_sign"] != x["sign"]]), len(S)))
    xs = [x["lin"] for x in res["roots"]]
    print()
    print("THE READING (fixed before the run): each k_c 71 root against the k_c 63 roots %s and the k_c 55 roots %s, bar %.2f:" % (list(R63), list(R55), BAR))
    for x in res["roots"]:
        c, d63, d55 = classify(x["lin"])
        print("  k_c 71 root in (%.2f, %.2f), %s: det-linear %.6f, range [%.6f, %.6f]: nearest k_c 63 root %.6f away, nearest k_c 55 root %.6f away: %s" % (
            x["br"][0], x["br"][1], x["orient"], x["lin"], x["lo"], x["hi"], d63, d55, c))
    print("OVERALL: " + overall(xs))
    print()
    print("information:")
    sg = {round(r["lam"], 2): r["sign"] for r in S}
    k63 = {round(r["lam"], 2): r["sign"] for r in rows([I + "d185_scan_1025.jsonl", I + "d185_scanhi_1025.jsonl", I + "d185_scanup_1025.jsonl", I + "kc63_map_A_new.jsonl"])}
    k55 = {round(r["lam"], 2): r["sign"] for r in rows([I + "kc55_scan_merged.jsonl"])}
    for nm, ref in (("k_c 63", k63), ("k_c 55", k55)):
        com = [l for l in sg if l in ref]
        same = sum(1 for l in com if sg[l] == ref[l])
        print("  hybrid signs at the %d lambda points of this grid that %s also has: equal at %d, opposite at %d (the orientation labels are each scan's own det-sign convention: no reading from them)" % (len(com), nm, same, len(com) - same))
    print("  signs by lambda (k_c 71): " + " ".join("%.2f%s" % (l, "+" if sg[l] > 0 else "-") for l in sorted(sg)))
