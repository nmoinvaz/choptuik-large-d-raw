#!/usr/bin/env python3
"""I213-win2: max |sigma_n(J 1250) - sigma_n(J 1500)| / |sigma_n| for n = 18..22 at omega/omega_inf 1.09, 1.10, 1.11 (issue #213).

    python compare_213.py [DIR_J1250 [DIR_J1500]]
        defaults: this folder and ../I82-win2. Files sigF_w<wf>_K45_J<J>_p1280.json. sigma_n is the complex number of the
        pair of strings sigma_str[n]; the relative difference is |difference| / |sigma_n(J 1500)|, in mpmath at 50 digits
        (the strings carry 20). Prints a table per node and n, then the maximum per node. Exit 0 when every maximum is
        below LIMIT (1e-10), exit 1 when one is not (the issue then asks for the crossing's uncertainty with that noise).
    python compare_213.py --selftest
        the J 1500 file against itself gives 0 at every n; one sigma_20 changed in its 9th significant digit is found at
        n = 20 and exceeds LIMIT; a change of 1e-12 relative stays below it (exit 1 inside if any of these fails)."""
import copy, json, os, sys, tempfile
from mpmath import mp, mpf, mpc, fabs

mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
LIMIT = mpf("1e-10")
NODES = ("1.09", "1.10", "1.11")
NS = range(18, 23)


def sig(obj, n):
    re, im = obj["sigma_str"][n]
    return mpc(mpf(re), mpf(im))


def rel(a, b):
    return {n: abs(sig(a, n) - sig(b, n)) / abs(sig(b, n)) for n in NS}


def load(d, wf, J):
    with open(os.path.join(d, f"sigF_w{wf}_K45_J{J}_p1280.json")) as f:
        return json.load(f)


def table(pairs, out=print):
    ok = True
    for wf, (a, b) in pairs.items():
        r = rel(a, b)
        m = max(r.values())
        out(f"w {wf}  K {a['K']} J {a['J']} vs J {b['J']}  prec {a['prec']} / {b['prec']}")
        for n, v in r.items():
            out(f"   n {n}  rel diff {mp.nstr(v, 4):>10}  sigma_err(J {a['J']}) {a['sigma_err'][n]}  (J {b['J']}) {b['sigma_err'][n]}")
        out(f"   max over n = 18..22: {mp.nstr(m, 4)}  {'below' if m < LIMIT else 'ABOVE'} {mp.nstr(LIMIT, 2)}")
        ok &= m < LIMIT
    return 0 if ok else 1


def selftest():
    d = os.path.join(os.path.dirname(HERE), "I82-win2")
    b = load(d, "1.10", 1500)
    same = rel(b, b)
    ok = all(v == 0 for v in same.values())
    c = copy.deepcopy(b)
    s = mpc(mpf(c["sigma_str"][20][0]), mpf(c["sigma_str"][20][1])) * (1 + mpf("1e-9"))
    c["sigma_str"][20] = [mp.nstr(s.real, 25), mp.nstr(s.imag, 25)]
    r = rel(c, b)
    ok &= r[20] > LIMIT and all(r[n] == 0 for n in NS if n != 20)
    c2 = copy.deepcopy(b)
    s = mpc(mpf(c2["sigma_str"][20][0]), mpf(c2["sigma_str"][20][1])) * (1 + mpf("1e-12"))
    c2["sigma_str"][20] = [mp.nstr(s.real, 25), mp.nstr(s.imag, 25)]
    ok &= rel(c2, b)[20] < LIMIT
    ok &= table({"1.10": (c, b)}, out=lambda s: None) == 1 and table({"1.10": (b, b)}, out=lambda s: None) == 0
    print("selftest:", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(selftest())
    d1 = sys.argv[1] if len(sys.argv) > 1 else HERE
    d2 = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(HERE), "I82-win2")
    sys.exit(table({wf: (load(d1, wf, 1250), load(d2, wf, 1500)) for wf in NODES}))
