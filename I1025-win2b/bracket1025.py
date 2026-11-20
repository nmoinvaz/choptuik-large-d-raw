"""#1025: where does an ell_refine.py lambda root sit in its bracket? ell_refine's lam_root (wip/ell1-highD 5c9d001c) looks at the grid guess * (1 + w * [-1, 0, 1]) for w in 0.02, 0.06, 0.15, 0.35 and
brackets the sign change in [lower, guess] or [guess, upper] of the first window that has one, then brentq. This recomputes that bracket from a record's lam_guess and lam (the record does not store it) and reports the root's distance
to each edge in grid steps (one step = the bracket's width, w * guess; the two distances add to 1) and in lambda. Reads only the record. The selftest plants roots at known places and must also fail a root outside every window.
usage: python -I bracket1025.py RECORDS.jsonl D       python -I bracket1025.py --selftest"""
import json
import sys

WINDOWS = (0.02, 0.06, 0.15, 0.35)


def bracket(guess, lam):
    for w in WINDOWS:
        lo, hi = guess * (1 - w), guess * (1 + w)
        if lo <= lam <= hi:
            a, b = (lo, guess) if lam <= guess else (guess, hi)
            return dict(w=w, lower=a, upper=b, step=b - a, to_lower=(lam - a) / (b - a), to_upper=(b - lam) / (b - a))
    return None


def selftest():
    ok = True
    g = 2.0
    cases = [(1.97, 0.02, 0.25, 0.75), (2.01, 0.02, 0.25, 0.75), (1.96, 0.02, 0.0, 1.0), (1.85, 0.15, None, None), (3.5, None, None, None)]
    for lam, w, tl, tu in cases:
        r = bracket(g, lam)
        if w is None and tl is None and r is not None and lam > g * 1.35:
            good = False
        elif tl is None and w is not None:
            good = r is not None and r["w"] == w                 # lam 1.85 is 7.5% off: window 0.15
        elif w is None:
            good = r is None
        else:
            good = r is not None and r["w"] == w and abs(r["to_lower"] - tl) < 1e-12 and abs(r["to_upper"] - tu) < 1e-12
        print("selftest lam %.2f against guess %.1f: %s -> %s" % (lam, g, r and ("window %.2f, %.3f / %.3f steps" % (r["w"], r["to_lower"], r["to_upper"])), "ok" if good else "WRONG"))
        ok &= good
    print("selftest", "passes" if ok else "FAILS")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    fn, D = sys.argv[1], float(sys.argv[2])
    for line in open(fn):
        r = json.loads(line)
        if r["D"] == D and r.get("lam"):
            b = bracket(r["lam_guess"], r["lam"])
            if b is None:
                print("D %g: lam %.10f is outside every window of guess %.10f (+-35%%)" % (D, r["lam"], r["lam_guess"]))
                continue
            print("D %g k_c %d: lam %.10f, guess %.10f (%.3f%% off), n_signchanges %s; window w %.2f, bracket [%.6f, %.6f] (step %.6f): root is %.3f steps (%.6f) above the lower edge and %.3f steps (%.6f) below the upper edge"
                  % (D, r["kc"], r["lam"], r["lam_guess"], 100 * (r["lam"] / r["lam_guess"] - 1), r.get("n_signchanges"), b["w"], b["lower"], b["upper"], b["step"],
                     b["to_lower"], r["lam"] - b["lower"], b["to_upper"], b["upper"] - r["lam"]))
