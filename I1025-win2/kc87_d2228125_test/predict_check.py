#!/usr/bin/env python3
"""predict_check.py SCAN_DIR | --selftest [--mutate]   (#1025 kc87_d2228125_test; written and registered BEFORE the three points were evaluated)

The registered test of the coordinator (hc of 25 Nov ~10:30 UTC): "lambda -0.1990, -0.1985 and -0.1965 ... Prediction from your zero fit (lc -0.1976, background slope -79.6, q -3.1) ...: ln|det| at each point = the fit's background + ln|l - lc|
within 0.05; a pole predicts the opposite sign of that term (a rise of about the same size). Pass for 'zero' when all three are within 0.05 of the zero model and the sign changes between -0.1985 and -0.1965; 'pole' when they follow the pole model;
else undecided. No refit before reading."
The fit (fit_zero_pole.py on the seven hybrid values -0.20 to -0.08 of D 22.28125, k_c 87): best lc = -0.1976, a = -2397.4451203178, s = -79.6113350583, q = -3.0581771034 with B(l) = a + s (l + 0.18) + q (l + 0.18)^2.
Models: zero(l) = B(l) + ln|l - lc|, pole(l) = B(l) - ln|l - lc|. Predictions (hybrid ln|det|): l = -0.1990: zero -2402.5049, pole -2389.3623; -0.1985: zero -2402.9865, pole -2388.9602; -0.1965: zero -2402.9448, pole -2389.3199.
PRIMARY classification (as ordered): 'zero' if all three |ln_hybrid - zero(l)| <= 0.05 and the hybrid signs are -, -, + at -0.1990, -0.1985, -0.1965; 'pole' if all three |ln_hybrid - pole(l)| <= 0.05 (the signs are printed; no sign condition is added to the order's);
else 'undecided'. SECONDARY classification (mine, registered with the primary, because 0.05 is below the prediction's own uncertainty: lc on a 1e-4 grid moves the zero model by 0.07 to 0.11 at these points, and rms <= 0.02 allows lc in [-0.1977, -0.1975]):
'zero-like' if all three are within 0.5 of the zero model and each is at least 5 from the pole model, with the signs -, -, +; 'pole-like' if all three are within 0.5 of the pole model and each at least 5 from the zero model; else 'neither'.
The two models differ by about 13 at each point.
--selftest: planted triples (the zero model exactly; the pole model exactly; the zero model + 0.2; the zero model with the signs +, -, +; the smooth background alone) must classify as written; --mutate sets the primary tolerance to 5 instead of 0.05, which the zero + 0.2 case must then catch (exit 1)."""
import sys, os, glob, json
import math

A, S, Q, LC, L0 = -2397.4451203178, -79.6113350583, -3.0581771034, -0.1976, -0.18
LAMS = (-0.1990, -0.1985, -0.1965)
TOL = 5.0 if "--mutate" in sys.argv else 0.05


def bg(l):
    return A + S * (l - L0) + Q * (l - L0) ** 2


def zero(l):
    return bg(l) + math.log(abs(l - LC))


def pole(l):
    return bg(l) - math.log(abs(l - LC))


def classify(pts):
    """pts: list of (lambda, hybrid sign, hybrid ln|det|) at LAMS. Returns (primary, secondary, table lines)"""
    pts = sorted(pts)
    lines = []
    dz = [abs(p[2] - zero(p[0])) for p in pts]
    dp = [abs(p[2] - pole(p[0])) for p in pts]
    for p, a, b in zip(pts, dz, dp):
        lines.append("lambda %.4f sign %+d ln|det| %.4f | zero model %.4f (diff %+.4f) | pole model %.4f (diff %+.4f)" % (p[0], p[1], p[2], zero(p[0]), p[2] - zero(p[0]), pole(p[0]), p[2] - pole(p[0])))
    signs = [p[1] for p in pts]
    sign_ok = signs == [-1, -1, 1]
    primary = "zero" if (all(d <= TOL for d in dz) and sign_ok) else ("pole" if all(d <= TOL for d in dp) else "undecided")
    secondary = "neither"
    if all(d <= 0.5 for d in dz) and all(d >= 5 for d in dp) and sign_ok:
        secondary = "zero-like"
    elif all(d <= 0.5 for d in dp) and all(d >= 5 for d in dz):
        secondary = "pole-like"
    return primary, secondary, lines


def selftest():
    bad = []
    def mk(f, signs=(-1, -1, 1), off=0.0):
        return [(l, s, f(l) + off) for l, s in zip(LAMS, signs)]
    cases = [
        ("zero model exactly", mk(zero), "zero", "zero-like"),
        ("pole model exactly", mk(pole), "pole", "pole-like"),
        ("zero model + 0.2", mk(zero, off=0.2), "undecided", "zero-like"),
        ("zero model, signs + - +", mk(zero, signs=(1, -1, 1)), "undecided", "neither"),
        ("smooth background alone", mk(bg), "undecided", "neither"),
    ]
    for name, pts, wp, ws in cases:
        p, s, _ = classify(pts)
        if (p, s) != (wp, ws):
            bad.append("%s: primary %s secondary %s (wanted %s, %s)" % (name, p, s, wp, ws))
    for b in bad:
        print("SELFTEST FAIL:", b)
    print("selftest %s" % ("FAILS" if bad else "passes"))
    return 1 if bad else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    d = [a for a in sys.argv[1:] if not a.startswith("--")][0]
    rows = {}
    for f in glob.glob(os.path.join(d, "scan_*_p*.jsonl")):
        for l in open(f):
            if l.strip():
                r = json.loads(l)
                rows[round(r["lam"], 4)] = (r["lam"], int(r["sign"]), r["ln"], r["noise_robust"], int(r["f64_sign"]), r["f64_ln"])
    pts = [(rows[round(l, 4)][0], rows[round(l, 4)][1], rows[round(l, 4)][2]) for l in LAMS if round(l, 4) in rows]
    if len(pts) != 3:
        print("only %d of the three points are there: %s" % (len(pts), sorted(rows)))
        return 2
    p, s, lines = classify(pts)
    print("\n".join(lines))
    print("not noise-robust:", [round(l, 4) for l in LAMS if not rows[round(l, 4)][3]] or "none", "| float64 sign differs from hybrid:", [round(l, 4) for l in LAMS if rows[round(l, 4)][4] != rows[round(l, 4)][1]] or "none")
    print("PRIMARY (the order's, tolerance %g): %s" % (TOL, p))
    print("SECONDARY (registered with it): %s" % s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
