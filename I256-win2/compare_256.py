#!/usr/bin/env python3
"""I256-win2: K 33 -> K 39 and K 39 -> K 45 steps of sigma at omega/omega_inf 1.09, 1.10, 1.11 (issue #256).

    python -I compare_256.py [DIR]
        DIR holds sigF_w<wf>_K39_J1000_p1280.json (default: this folder). K 33, J 1000 from ../T155-win2 (1.09, 1.11) and
        ../I202-win2 (1.10); K 45, J 1500 from ../I82-win2. Steps, per node and n, from the 20 stored digits of sigma_str
        (mpmath, 50 digits), relative to |sigma_n(K 45)|:
            step1 = |sigma_n(K 39) - sigma_n(K 33)| / |sigma_n(K 45)|        step2 = |sigma_n(K 45) - sigma_n(K 39)| / |sigma_n(K 45)|
        Table 1 at n = 6, 7, 15, 16 (the issue's orders), table 2 for n = 1 to 16. Acceptance: step2 of 1.10 is at most the larger
        of step2 of 1.09 and 1.11 at n = 6, 7, 15, 16, or the orders where it is larger are named; a large step1 at 1.10 alone,
        with step2 in line, points to the K 33 error instead (printed as a second line per order).
        Exit 0: step2 of 1.10 is not above the neighbours' at any of the four orders. Exit 1: it is above at the orders named.
        Exit 2: a file is missing.
    python -I compare_256.py --selftest
        the code reproduces #82's posted K 45 against K 33 rows (n = 7, 9, 16 at 1.09, 1.11 and 1.10), a K 39 planted equal to K 45
        gives step2 = 0 at every node, a K 39 planted equal to K 33 gives step1 = 0, and a planted K 39 that sits at the K 33
        value only at 1.10 makes the verdict exit 1 (exit 1 inside if any of these fails)."""
import copy, json, os, sys
from mpmath import mp, mpf, mpc

mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
NODES = ("1.09", "1.10", "1.11")
ORDERS = (6, 7, 15, 16)
NS = list(range(1, 17))


def z(s): return mpc(mpf(s[0]), mpf(s[1]))


def sig(*p): return json.load(open(os.path.join(RAW, *p)))["sigma_str"]


def k33(w):
    return sig("I202-win2", "sigF_w1.10_K33_J1000.json") if w == "1.10" else sig("T155-win2", f"sigF_w{w}_K33_J1000.json")


def k45(w): return sig("I82-win2", f"sigF_w{w}_K45_J1500_p1280.json")


def steps(a33, a39, a45):
    """{n: (step1, step2)} for n = 1..16, relative to |sigma_n(K 45)|"""
    out = {}
    for n in NS:
        d = abs(z(a45[n]))
        out[n] = (abs(z(a39[n]) - z(a33[n])) / d, abs(z(a45[n]) - z(a39[n])) / d)
    return out


def fmt(v): return "0" if v == 0 else mp.nstr(v, 3)


def report(S, out=print):
    """S: {node: steps}. Returns 0 if the 1.10 step2 is not above the neighbours' at ORDERS, else 1."""
    out("table 1: relative steps at the issue's orders (step1 = K 33 -> K 39, step2 = K 39 -> K 45)")
    out(f"{'n':>3s} | " + " | ".join(f"{w} step1  step2" for w in NODES))
    for n in ORDERS:
        out(f"{n:3d} | " + " | ".join(f"{fmt(S[w][n][0]):>9s} {fmt(S[w][n][1]):>9s}" for w in NODES))
    out("table 2: n = 1 to 16, step1 / step2 per node")
    for n in NS:
        out(f"{n:3d} | " + " | ".join(f"{fmt(S[w][n][0]):>9s} {fmt(S[w][n][1]):>9s}" for w in NODES))
    above = []
    out("acceptance: step2 of 1.10 against the larger of step2 of 1.09 and 1.11")
    for n in ORDERS:
        mx = max(S["1.09"][n][1], S["1.11"][n][1])
        s2 = S["1.10"][n][1]
        s1x = max(S["1.09"][n][0], S["1.11"][n][0])
        ok = s2 <= mx
        if not ok:
            above.append(n)
        r = (mp.nstr(s2 / mx, 3) if mx != 0 else ("0" if s2 == 0 else "inf"))
        note = "" if S["1.10"][n][0] <= s1x else "  (step1 of 1.10 also above the neighbours')"
        out(f"  n {n:2d}: step2 1.10 {fmt(s2):>9s}, larger neighbour {fmt(mx):>9s}, ratio {r:>6s}  {'within' if ok else 'ABOVE'}{note}")
    out("step2 of 1.10 above the neighbours' at n = " + (str(above) if above else "none"))
    return 1 if above else 0


def selftest():
    q = lambda s: None
    ok = True
    # control: #82's posted K 45 against K 33 rows (n = 7, 9, 16), through the same sigma files
    posted = {"1.09": {7: "6.7e-20", 9: "3.2e-17", 16: "3.5e-16"}, "1.11": {7: "3.6e-19", 9: "3.3e-18", 16: "4.4e-16"},
              "1.10": {7: "1.2e-18", 9: "9.4e-18", 16: "1.2e-15"}}
    for w, d in posted.items():
        a45, a33 = k45(w), k33(w)
        for n, s in d.items():
            ok &= mp.nstr(abs(z(a45[n]) - z(a33[n])) / abs(z(a33[n])), 2) == s
    S45 = {w: steps(k33(w), k45(w), k45(w)) for w in NODES}
    ok &= all(S45[w][n][1] == 0 for w in NODES for n in NS)
    S33 = {w: steps(k33(w), k33(w), k45(w)) for w in NODES}
    ok &= all(S33[w][n][0] == 0 for w in NODES for n in NS)
    # planted: K 39 at the K 33 value only at 1.10 -> step2 of 1.10 (= K 33 -> K 45 gap) is above the neighbours' (K 39 = K 45 there)
    S = {w: steps(k33(w), k45(w), k45(w)) for w in ("1.09", "1.11")}
    S["1.10"] = steps(k33("1.10"), k33("1.10"), k45("1.10"))
    ok &= report(S, out=q) == 1
    # planted: K 39 at the K 45 value everywhere -> verdict 0
    ok &= report(S45, out=q) == 0
    print("selftest:", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(selftest())
    d = sys.argv[1] if len(sys.argv) > 1 else HERE
    files = {w: os.path.join(d, f"sigF_w{w}_K39_J1000_p1280.json") for w in NODES}
    miss = [f for f in files.values() if not os.path.exists(f)]
    if miss:
        print("MISSING", *miss)
        sys.exit(2)
    S = {w: steps(k33(w), json.load(open(files[w]))["sigma_str"], k45(w)) for w in NODES}
    sys.exit(report(S))
