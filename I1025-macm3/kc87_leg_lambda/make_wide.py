#!/usr/bin/env python3
"""make_wide.py: the wide scans of D 22.25 and D 22.125 side by side (t5, hc 25 Nov: "Read every robust change by position, with orientation, and report both lists side by side"), from the scan files only.
usage: make_wide.py            markdown on stdout (a scan not finished yet is read from its per-process files)
       make_wide.py --selftest [--mutate=orient]   planted signs with known changes; the mutation reverses the orientation and must fail
A change is a pair of neighbouring lambda (sorted, repeats merged) whose hybrid signs differ; it is robust when both ends are noise-robust. Orientation is read from the two signs (- to + means the sign goes from - to + as lambda grows)."""
import glob, json, os, sys
L = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda")
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)

def load(folder, D):
    p = "%s/%s/scan/scan_D%s_1025.jsonl" % (L, folder, D)
    fs = [p] if os.path.exists(p) else sorted(glob.glob("%s/%s/scan/scan_D%s_p*.jsonl" % (L, folder, D)))
    rows = [json.loads(l) for f in fs for l in open(f) if l.strip()]
    by = {}
    for r in rows: by.setdefault(round(r["lam"], 4), []).append(r)
    return by

def changes(by):
    lams = sorted(by); out = []
    for a, b in zip(lams, lams[1:]):
        sa, sb = by[a][0]["sign"], by[b][0]["sign"]
        if sa != sb:
            ori = ("- to +" if sb > 0 else "+ to -") if MUT != "orient" else ("+ to -" if sb > 0 else "- to +")
            out.append((a, b, ori, all(r["noise_robust"] for r in by[a] + by[b])))
    return out

def sg(x): return "+" if x > 0 else "-"

def selftest():
    mk = lambda lam, s: {"lam": lam, "sign": s, "noise_robust": True}
    by = {round(0.20 + 0.02 * i, 4): [mk(0.20 + 0.02 * i, s)] for i, s in enumerate([1, 1, 1, -1, -1, 1, 1])}
    ch = changes(by)
    ok = ch == [(0.24, 0.26, "+ to -", True), (0.28, 0.3, "- to +", True)]     # signs at 0.20 0.22 0.24 0.26 0.28 0.30 0.32: + + + - - + +, so the changes lie between indices 2-3 and 4-5
    print("planted: signs + + + - - + + -> %s: %s" % (ch, "PASS" if ok else "FAIL"))
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    if "--selftest" in sys.argv: sys.exit(selftest())
    W = {"22.25": load("22.25_wide", "22.25"), "22.125": load("22.125_wide", "22.125")}
    F = {"22.125": ("first scan 0.485-0.505 by 0.005", load("22.125", "22.125")), "22.125 rescan": ("0.487-0.497 by 0.0025", load("22.125_rescan", "22.125")),
         "22.15625": ("0.470-0.490 by 0.005", load("22.15625", "22.15625")), "22.1875": ("0.455-0.475 by 0.005", load("22.1875", "22.1875")), "22.25": ("first scan 0.425-0.445 by 0.005", load("22.25", "22.25"))}
    P = print
    P("| lambda | D 22.125: hybrid sign | ln\\|det\\| | float64 sign | D 22.25: hybrid sign | ln\\|det\\| | float64 sign |\n|---|---|---|---|---|---|---|")
    for lam in sorted(set(W["22.25"]) | set(W["22.125"])):
        cell = lambda d: ("%s%s | %.4f | %s" % (sg(W[d][lam][0]["sign"]), " (two evaluations)" if len(W[d][lam]) > 1 else "", W[d][lam][0]["ln"], sg(W[d][lam][0]["f64_sign"]))) if lam in W[d] else "- | - | -"
        P("| %.2f | %s | %s |" % (lam, cell("22.125"), cell("22.25")))
    P("\n**Sign changes by position, with orientation** (neighbouring lambda whose hybrid signs differ; robust = both ends noise-robust):\n")
    P("| scan | lambda pair | orientation | robust |\n|---|---|---|---|")
    for d in ("22.25", "22.125"):
        ch = changes(W[d])
        P("| D %s wide (0.20-0.50 by 0.02) | %s | %s | %s |" % (d, "; ".join("(%.2f, %.2f)" % (a, b) for a, b, _, _ in ch) or "none", "; ".join(o for _, _, o, _ in ch) or "-", "; ".join(str(r) for _, _, _, r in ch) or "-"))
    for k, (what, by) in F.items():
        ch = changes(by)
        P("| D %s %s | %s | %s | %s |" % (k.split()[0], what + (" (rescan)" if "rescan" in k else ""), "; ".join("(%.4f, %.4f)" % (a, b) for a, b, _, _ in ch) or "none", "; ".join(o for _, _, o, _ in ch) or "-", "; ".join(str(r) for _, _, _, r in ch) or "-"))
    P("\n**Evaluations that are not noise-robust:** " + "; ".join("D %s: %s" % (d, ", ".join("%.2f" % l for l in sorted(W[d]) if not all(r["noise_robust"] for r in W[d][l])) or "none") for d in W))
    for d in W:
        if 0.44 in W[d] and len(W[d][0.44]) == 2:
            a, b = W[d][0.44]; same = {k: v for k, v in a.items() if k != "sec"} == {k: v for k, v in b.items() if k != "sec"}
            P("The repeat of 0.44 at D %s: %s (hybrid %+d, ln|det| %.10f)." % (d, "bit-identical in every field but the seconds" if same else "DIFFERENT", a["sign"], a["ln"]))
    f = F["22.25"][1].get(0.44)
    if f and 0.44 in W["22.25"]:
        a = f[0]; b = W["22.25"][0.44][0]; same = {k: v for k, v in a.items() if k != "sec"} == {k: v for k, v in b.items() if k != "sec"}
        P("The first scan's evaluation of 0.440 at D 22.25 and the wide scan's 0.44: %s." % ("bit-identical in every field but the seconds" if same else "DIFFERENT: %s" % {k: (a[k], b[k]) for k in a if k != "sec" and a[k] != b.get(k)}))
