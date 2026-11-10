#!/usr/bin/env python3
"""I295-win2: the J steps of sigma_n at n = 6, 7, 15, 16 from existing files, once step 1 shows sigma is independent of K at J 1500.

    python -I jstep_295.py
        For wf = 1.09, 1.10, 1.11 and n = 6, 7, 15, 16 prints, relative to |sigma_n| (the 20 stored digits, mpmath 50 digits):
          a = |K 45 J 1500 - K 33 J 1000|   (the gap of #202 and #228)
          b = |K 45 J 1250 - K 33 J 1000|   (#213's J 1250 files)
          c = |K 45 J 1500 - K 45 J 1250|
        K 33 J 1000: T155-win2 (1.09, 1.11) and I202-win2 (1.10). K 45 J 1500: I82-win2. K 45 J 1250: I213-win2.
    python -I jstep_295.py --selftest
        a file against itself gives 0 at every n, and a planted digit in n = 7 gives a nonzero entry at n = 7 only."""
import copy, json, os, sys

from mpmath import mp, mpf, mpc, nstr

mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
NS = (6, 7, 15, 16)
FILES = {
    "K33J1000": {"1.09": "T155-win2/sigF_w1.09_K33_J1000.json", "1.10": "I202-win2/sigF_w1.10_K33_J1000.json", "1.11": "T155-win2/sigF_w1.11_K33_J1000.json"},
    "K45J1250": {w: f"I213-win2/sigF_w{w}_K45_J1250_p1280.json" for w in ("1.09", "1.10", "1.11")},
    "K45J1500": {w: f"I82-win2/sigF_w{w}_K45_J1500_p1280.json" for w in ("1.09", "1.10", "1.11")},
}


def z(s): return mpc(mpf(s[0]), mpf(s[1]))


def rel(a, b, n): return abs(z(a[n]) - z(b[n])) / abs(z(b[n]))


def load(p):
    with open(os.path.join(RAW, p), encoding="utf-8") as f:
        return json.load(f)["sigma_str"]


def fmt(x): return "0" if x == 0 else nstr(x, 2)


def main():
    print("relative to |sigma_n|; a = K45 J1500 - K33 J1000, b = K45 J1250 - K33 J1000, c = K45 J1500 - K45 J1250")
    print(f"{'wf':>5} {'':>2}" + "".join(f"{'n=' + str(n):>10}" for n in NS))
    for w in ("1.09", "1.10", "1.11"):
        s33, s125, s150 = (load(FILES[k][w]) for k in ("K33J1000", "K45J1250", "K45J1500"))
        for name, (x, y) in (("a", (s150, s33)), ("b", (s125, s33)), ("c", (s150, s125))):
            print(f"{w:>5} {name:>2}" + "".join(f"{fmt(rel(x, y, n)):>10}" for n in NS))


def selftest():
    s = load(FILES["K45J1500"]["1.10"])
    bad = copy.deepcopy(s)
    t = bad[7][0]
    bad[7][0] = t[:-2] + ("0" if t[-2] != "0" else "1") + t[-1]
    zero = all(rel(s, s, n) == 0 for n in range(1, 17))
    hit = [n for n in range(1, 17) if rel(bad, s, n) != 0]
    ok = zero and hit == [7]
    print("selftest: ok" if ok else f"selftest FAILED: self zero {zero}, planted hit at {hit}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else (main() or 0))
