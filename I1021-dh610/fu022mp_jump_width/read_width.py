#!/usr/bin/env python3
"""#1076 fu022mp_jump_width (dh610) read_width.py reading L.jsonl R.jsonl MAP_L.jsonl MAP_R.jsonl | selftest [--mutate]: the reading of width_jump.py's two caches (L = the L root's seed at each row, R = the R root's).
Per row and offset in A from 3.7873456: the F_3 and |r_3| of the L and R solves; class two roots = both valued and F_3 differing by more than TWO (0.01), one root = within ONE (1e-3), between = in between, one seed only, none.
The two-valued width of a row = the largest |offset| such that every offset between 0 and it (both signs counted apart) is two roots. Repeat check (a control that can fail): at offset 0 the L solve and the R solve reproduce the map's roots
at that row (MAP_L, MAP_R) within REPEAT (1e-4), and are two roots; if not the reader exits 1.
selftest: planted rows must read the classes and widths as planted and the repeat check pass and fire; --mutate sets TWO to 10 and the selftest exits 1."""
import json, math, sys

ONE, TWO, REPEAT = 1e-3, 0.01, 1e-4
A0 = 3.7873456
OFFS = [-0.03125, -0.016, -0.004, -0.001, 0.0, 0.001, 0.004, 0.016, 0.03125]
ROWS = [0.24404321, 0.23154321]


def load(path):
    last = {}
    for l in open(path):
        if l.strip():
            r = json.loads(l)
            last[(round(r["A"], 7), round(r["wf"], 8))] = r
    return last


def valued(r):
    if r is None or not all(isinstance(r.get(k), float) and math.isfinite(r[k]) for k in ("F3re", "F3im")):
        return False
    return (isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))


def F3(r):
    return complex(r["F3re"], r["F3im"]) if valued(r) else None


def classify(fl, fr, two=TWO):
    if fl is None or fr is None:
        return "L seed only" if fl is not None else ("R seed only" if fr is not None else "none")
    d = abs(fl - fr)
    return "two roots" if d > two else ("one root" if d < ONE else "between")


def same(a, b):
    return a is not None and b is not None and abs(a - b) < REPEAT


def widths(cls_by_off):
    out = {}
    for sgn in (1, -1):
        w = 0.0
        for o in sorted((o for o in cls_by_off if o * sgn > 0), key=abs):
            if cls_by_off[o] != "two roots":
                break
            w = abs(o)
        out[sgn] = w
    return out


def selftest(mutate):
    two = 10.0 if mutate else TWO
    a, b = -0.04 - 0.49j, 0.0 - 0.51j
    got = [classify(a, b, two), classify(a, a + 1e-9, two), classify(a, a + 5e-3, two), classify(a, None, two), classify(None, None, two)]
    want = ["two roots", "one root", "between", "L seed only", "none"]
    c = {-0.03125: "one root", -0.016: "two roots", -0.004: "two roots", -0.001: "two roots", 0.0: "two roots", 0.001: "two roots", 0.004: "one root", 0.016: "two roots", 0.03125: "one root"}
    wd = widths(c)
    ok = got == want and wd == {1: 0.001, -1: 0.016} and same(a, a + 1e-6) and not same(a, a + 1e-3) and not same(a, None)
    print("selftest" + (" --mutate" if mutate else ""), got, wd, "PASS" if ok else "FAIL" + (" (FIRED)" if mutate else ""))
    return 0 if ok else 1


def reading(lp, rp, mlp, mrp):
    L, R = load(lp), load(rp)
    ML, MR = load(mlp), load(mrp)
    ok_rep = True
    print("| wf | A offset | A | L-seed F_3 (|r_3|) | R-seed F_3 (|r_3|) | class (abs difference) |")
    print("|---|---|---|---|---|---|")
    wid = {}
    for w in ROWS:
        cb = {}
        for o in OFFS:
            k = (round(A0 + o, 7), round(w, 8))
            fl, fr = F3(L.get(k)), F3(R.get(k))
            cls = classify(fl, fr)
            cb[o] = cls
            f = lambda z, x: "no value" if z is None else f"{z.real:+.6f} {z.imag:+.6f}i ({x[k]['info']:.1e})"
            d = "" if fl is None or fr is None else f" ({abs(fl - fr):.4f})"
            print(f"| {w!r} | {o:+.5f} | {k[0]!r} | {f(fl, L)} | {f(fr, R)} | {cls}{d} |")
        wid[w] = widths(cb)
    print("\nrepeat check (offset 0, the seeds' own roots reproduced within %g and two roots):" % REPEAT)
    for w in ROWS:
        k = (round(A0, 7), round(w, 8))
        # the seeds are the map's roots: recorded in each pass's first solve at offset 0, compared with the map's caches by the lane
        cl = classify(F3(L.get(k)), F3(R.get(k)))
        kk = (3.7873456, round(w, 8))
        dl = abs(F3(L[k]) - F3(ML[kk])) if F3(L.get(k)) is not None else None
        dr = abs(F3(R[k]) - F3(MR[kk])) if F3(R.get(k)) is not None else None
        print(f"  wf {w}: class at offset 0 {cl}; |dF_3| to the map's L root {dl}, to its R root {dr}")
        ok_rep = ok_rep and cl == "two roots" and same(F3(L.get(k)), F3(ML.get(kk))) and same(F3(R.get(k)), F3(MR.get(kk)))
    print("\ntwo-valued width in A (largest |offset| of the unbroken run of two-root offsets from 0):")
    for w in ROWS:
        print(f"  wf {w}: west {wid[w][-1]}, east {wid[w][1]}")
    return 0 if ok_rep else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["selftest"]:
        sys.exit(selftest("--mutate" in a))
    sys.exit(reading(a[1], a[2], a[3], a[4]))
