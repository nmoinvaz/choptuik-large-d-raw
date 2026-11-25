#!/usr/bin/env python3
"""#1076 fu022mp_jump_map (dh610) read_map.py reading SRC STD L R | selftest [--mutate]: the reading of map_jump.py's three caches (SRC = the recount's cache the STD pass started from).
Per location (5 x 5 grid and the two gap points): F_3 and |r_3| of the STD, L and R solves; a solve is valued when its record is (info < 1e-8 or the continuation's fix ok) with a finite F_3.
Classes of a location: two roots = the L and R solves are both valued and their F_3 differ by more than TWO (0.01); one root = both valued and within ONE (1e-3); between = in between (flagged); one seed only / none.
The STD label = the root (L's or R's, within ONE) that the STD solve landed on. Repeat check: the L solve at the gap's lower point and the R solve at its upper point reproduce the recount's F_3 of those points within REPEAT (1e-4); FIRES (exit 1) if not.
selftest: planted records must read two roots, one root, between, one seed only, and the labels; the repeat check must pass on planted equal values and FIRE on a planted mismatch; --mutate sets TWO to 10 and the selftest exits 1."""
import json, math, sys

ONE, TWO, REPEAT = 1e-3, 0.01, 1e-4
AS = [3.6623456, 3.7248456, 3.7873456, 3.8498456, 3.9123456]
WS = [0.20654321, 0.21904321, 0.23154321, 0.24404321, 0.25654321]
GAP_L, GAP_R = 0.239868405312, 0.239874508828


def key(a, w):
    return (round(a, 12), round(w, 12))


def load(path):
    last = {}
    for l in open(path):
        if l.strip():
            r = json.loads(l)
            last[key(r["A"], r["wf"])] = r
    return last


def valued(r):
    if r is None or not all(isinstance(r.get(k), float) and math.isfinite(r[k]) for k in ("F3re", "F3im")):
        return False
    return (isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))


def F3(r):
    return complex(r["F3re"], r["F3im"]) if valued(r) else None


def classify(fl, fr, fs, two=TWO):
    if fl is not None and fr is not None:
        d = abs(fl - fr)
        cls = "two roots" if d > two else ("one root" if d < ONE else "between")
    else:
        d = float("nan")
        cls = "L seed only" if fl is not None else ("R seed only" if fr is not None else "none")
    lab = "none"
    if fs is not None:
        near = [n for n, f in (("L", fl), ("R", fr)) if f is not None and abs(fs - f) < ONE]
        lab = "+".join(near) if near else "neither"
    return cls, d, lab


def repeat(src, L, R):
    out = []
    for w, name, S in ((GAP_L, "L seed at the gap's lower point", L), (GAP_R, "R seed at the gap's upper point", R)):
        k = key(3.7873456, w)
        a, b = F3(S.get(k)), F3(src.get(k))
        out.append((name, None if a is None or b is None else abs(a - b)))
    return out, all(d is not None and d < REPEAT for _, d in out)


def selftest(mutate):
    two = 10.0 if mutate else TWO
    mk = lambda f, info=1e-6, fix=dict(ok=True): dict(F3re=f.real, F3im=f.imag, info=info, re=1.0, im=1.0, fix=fix)
    a, b = -0.042 - 0.489j, 0.0003 - 0.5118j
    got = [classify(a, b, a, two)[::2], classify(a, a + 1e-6, a, two)[::2], classify(a, a + 5e-3, None, two)[::2],
           classify(a, None, b, two)[::2], classify(None, None, None, two)[::2]]
    want = [("two roots", "L"), ("one root", "L+R"), ("between", "none"), ("L seed only", "neither"), ("none", "none")]
    ok = got == want
    k1, k2 = key(3.7873456, GAP_L), key(3.7873456, GAP_R)
    src = {k1: mk(a), k2: mk(b)}
    _, good = repeat(src, {k1: mk(a + 1e-6)}, {k2: mk(b)})
    _, bad = repeat(src, {k1: mk(a + 1e-3)}, {k2: mk(b)})
    ok = ok and good and not bad and not valued(mk(a, 1e-3, None)) and valued(mk(a, 1e-3)) and valued(mk(a, 1e-9, None))
    print("selftest" + (" --mutate" if mutate else ""), got, good, bad, "PASS" if ok else "FAIL" + (" (FIRED)" if mutate else ""))
    return 0 if ok else 1


def reading(src_p, std_p, l_p, r_p):
    src, S, L, R = load(src_p), load(std_p), load(l_p), load(r_p)
    locs = [(a, w) for w in reversed(WS) for a in AS] + [(3.7873456, GAP_R), (3.7873456, GAP_L)]
    rp, okr = repeat(src, L, R)
    print("repeat check (the recount's F_3 of the gap's points, within %g):" % REPEAT, "PASS" if okr else "FIRES")
    for n, d in rp:
        print(f"  {n}: |dF_3| = {d if d is None else format(d, '.2e')}")
    fl0, fr0 = F3(L.get(key(3.7873456, GAP_L))), F3(R.get(key(3.7873456, GAP_R)))
    print(f"seeds: L = F_3 {fl0:.6f}, R = F_3 {fr0:.6f}, |L - R| = {abs(fl0 - fr0):.4f}")
    print("\n| A | wf | STD F_3 (|r_3|) | L-seed F_3 (|r_3|) | R-seed F_3 (|r_3|) | class | STD landed on |")
    print("|---|---|---|---|---|---|---|")
    sym, cnt = {}, {}
    for a, w in locs:
        k = key(a, w)
        fs, fl, fr = (F3(x.get(k)) for x in (S, L, R))
        cls, d, lab = classify(fl, fr, fs)
        cnt[cls] = cnt.get(cls, 0) + 1
        sym[(a, w)] = (cls, lab)
        f = lambda z, x: "no value" if z is None else f"{z.real:+.6f} {z.imag:+.6f}i ({x[k]['info']:.1e})"
        print(f"| {a!r} | {w!r} | {f(fs, S)} | {f(fl, L)} | {f(fr, R)} | {cls}{'' if math.isnan(d) else ' (%.4f)' % d} | {lab} |")
    print("\nclasses of the", len(locs), "locations:", cnt)
    print("\nmap of the grid (rows wf from high to low, columns A from low to high); class: 2 two roots, 1 one root, b between, l or r one seed only, - none; STD landed on: L, R, B (both), ? (neither), . (no value)")
    sc = {"two roots": "2", "one root": "1", "between": "b", "L seed only": "l", "R seed only": "r", "none": "-"}
    sl = {"L": "L", "R": "R", "L+R": "B", "neither": "?", "none": "."}
    print("            " + "  ".join(f"A {a:.4f}" for a in AS))
    for w in reversed(WS):
        print(f"wf {w:.5f}  " + "      ".join(f"{sc[sym[(a, w)][0]]}/{sl[sym[(a, w)][1]]}" for a in AS))
    return 0 if okr else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["selftest"]:
        sys.exit(selftest("--mutate" in a))
    sys.exit(reading(*a[1:5]))
