#!/usr/bin/env python3
"""make_track.py: the sign changes of lambda_1's neighbourhood against D, from every scan folder of a state (t5, hc 25 Nov: "track the new root's position against D"), from the scan files only.
Per D: the scans merged on lambda (a lambda in two scans is taken once; a disagreement of the sign or ln|det| between two evaluations of the same lambda is reported), the lambda range covered with its gaps (spacing above 0.0201), and every sign change by
position (the neighbouring lambda whose hybrid signs differ) with orientation and noise-robustness.
usage: make_track.py            markdown on stdout     |     make_track.py --selftest [--mutate=orient|gap]"""
import glob, json, os, sys
L = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda")
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
FOLDERS = {"22.0": ["22.0"], "22.125": ["22.125", "22.125_rescan", "22.125_low", "22.125_wide", "22.125_high"], "22.15625": ["22.15625", "22.15625_high"],
           "22.1875": ["22.1875", "22.1875_low", "22.1875_mid"], "22.21875": ["22.21875_full"], "22.25": ["22.25", "22.25_low", "22.25_wide", "22.25_refine"]}

def load(folder, D):
    p = "%s/%s/scan/scan_D%s_1025.jsonl" % (L, folder, D)
    fs = [p] if os.path.exists(p) else sorted(glob.glob("%s/%s/scan/scan_D%s_p*.jsonl" % (L, folder, D)))
    return [json.loads(l) for f in fs for l in open(f) if l.strip()]

def merge(rowsets):
    by, clash = {}, []
    for name, rows in rowsets:
        for r in rows:
            k = round(r["lam"], 4)
            if k in by:
                if (by[k]["sign"], round(by[k]["ln"], 6)) != (r["sign"], round(r["ln"], 6)): clash.append((k, name))
            else: by[k] = dict(r, src=name)
    return by, clash

def changes(by):
    ks = sorted(by); out = []
    for a, b in zip(ks, ks[1:]):
        if by[a]["sign"] != by[b]["sign"]:
            ori = ("- to +" if by[b]["sign"] > 0 else "+ to -") if MUT != "orient" else ("+ to -" if by[b]["sign"] > 0 else "- to +")
            out.append((a, b, ori, bool(by[a]["noise_robust"] and by[b]["noise_robust"])))
    return out

def coverage(by):
    ks = sorted(by); gaps = [(a, b) for a, b in zip(ks, ks[1:]) if b - a > (0.0201 if MUT != "gap" else 1.0)]
    return ks[0], ks[-1], gaps

def selftest():
    mk = lambda lam, s: {"lam": lam, "sign": s, "ln": -1.0 * lam, "noise_robust": True}
    by, clash = merge([("a", [mk(0.02, -1), mk(0.04, -1), mk(0.06, 1)]), ("b", [mk(0.06, 1), mk(0.10, 1), mk(0.12, -1)])])
    ch = changes(by); cv = coverage(by)
    ok = ch == [(0.04, 0.06, "- to +", True), (0.10, 0.12, "+ to -", True)] and not clash and cv == (0.02, 0.12, [(0.06, 0.10)])
    print("planted: two scans merged (a repeated lambda taken once): changes %s, coverage %s: %s" % (ch, cv, "PASS" if ok else "FAIL"))
    by2, clash2 = merge([("a", [mk(0.06, 1)]), ("b", [mk(0.06, -1)])])
    ok2 = clash2 == [(0.06, "b")]
    print("planted: two evaluations of one lambda that disagree are reported: %s" % ("PASS" if ok2 else "FAIL"))
    print("selftest:", "PASS" if ok and ok2 else "FAIL")
    return 0 if ok and ok2 else 1

if __name__ == "__main__":
    if "--selftest" in sys.argv: sys.exit(selftest())
    P = print
    P("| D | scans merged | lambda covered | gaps in the coverage (spacing above 0.0201) | sign changes by position | orientations | robust |\n|---|---|---|---|---|---|---|")
    for D, fol in FOLDERS.items():
        sets = [(f, load(f, D)) for f in fol]; sets = [(f, r) for f, r in sets if r]
        if not sets: continue
        by, clash = merge(sets); lo, hi, gaps = coverage(by); ch = changes(by)
        P("| %s | %s | %.4f to %.4f | %s | %s | %s | %s |" % (D, ", ".join("%s (%d)" % (f, len(r)) for f, r in sets), lo, hi, "; ".join("(%g, %g)" % g for g in gaps) or "none",
          "; ".join("(%g, %g)%s" % (a, b, " (an unscanned span: the position is only bracketed by the two neighbours)" if b - a > 0.0201 else "") for a, b, _, _ in ch) or "none", "; ".join(o for _, _, o, _ in ch) or "-", "; ".join(str(r) for _, _, _, r in ch) or "-"))
        if clash: P("\nDISAGREEMENT between scans of D %s at lambda %s" % (D, clash))
