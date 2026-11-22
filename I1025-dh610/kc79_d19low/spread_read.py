#!/usr/bin/env python3
"""#1025 kc79_d19low (dh610) spread_read.py ROW1 ROW2 ROW4 LOG1 LOG2 LOG4 REF.jsonl LAM | selftest [--mutate]: this machine's own spread of the k_c 79 control point (D 19.0, lambda 1.54, winb's state
and record) over BLAS thread counts 1, 2, 4 (OMP, OPENBLAS, MKL = N; VECLIB and RAYON stay 1, as in the 1-thread control), against winb's row (a Windows build). Prints per thread count the hybrid sign,
ln|det|, the |F| of the system check, noise_robust and the float64 sign, the relative spread (max - min) / mean |ln| of the three, each value's relative difference from winb's and the cross-machine
difference (the 1-thread value against winb's, 1.914e-6 in the control). Reading fixed by the coordinator (hc, 22 Nov) before the runs: own spread >= 0.5 x the cross-machine difference -> 'build rounding at
this size: the k_c 79 bar is set from the measured spread'; own spread < 1e-7 -> 'the cross-machine difference is real: k_c 79 scans stay on winb's machine'; in between -> 'between: neither rule applies'.
Exit 0 and prints the verdict; exit 1 if a log is not the record system or a sign differs among the rows (the spread is then not read).
selftest: planted ln triples with spreads 0, 3e-7, 1e-6 and an unequal-sign triple must give 'real', 'between', 'rounding', refused. --mutate raises the lower bar to 1e-5, which must make the 3e-7 case give 'real' (the selftest exits 1)."""
import sys, json, re

LOW = 1e-7
HALF = 0.5


def verdict(spread, cross, low=LOW):
    if spread >= HALF * cross:
        return "rounding"
    if spread < low:
        return "real"
    return "between"


TEXT = {"rounding": "own spread >= half the cross-machine difference: build rounding at this size; the k_c 79 bar is set from the measured spread (the coordinator's)",
        "real": "own spread < 1e-7: the cross-machine difference is real; k_c 79 scans stay on winb's machine (the coordinator's)",
        "between": "own spread between 1e-7 and half the cross-machine difference: neither of the coordinator's rules applies; report and ask"}


def analyse(rows, logs, ref, low=LOW):
    ok_sys = all("the record system" in l and "NOT the record system" not in l for l in logs)
    signs = {r["sign"] for r in rows}
    if not ok_sys or len(signs) != 1:
        return None
    lns = [r["ln"] for r in rows]
    mean = sum(abs(x) for x in lns) / len(lns)
    spread = (max(lns) - min(lns)) / mean
    vs = [abs(x - ref["ln"]) / abs(ref["ln"]) for x in lns]
    cross = vs[0]
    return dict(spread=spread, vs=vs, cross=cross, verdict=verdict(spread, cross, low))


def selftest(mutate):
    low = 1e-5 if mutate else LOW
    ref = dict(ln=-2547.786620251229)
    base = -2547.7914967589
    row = lambda ln, s=-1.0: dict(ln=ln, sign=s)
    good = "D 19.0 k_c 79: the record system"
    def trip(rel):                                   # three values with spread about rel, the first at base
        return [row(base), row(base * (1 + rel / 2)), row(base * (1 + rel))]
    cases = [("spread 0", [row(base)] * 3, "real"), ("spread 3e-7", trip(3e-7), "between"), ("spread 1e-6", trip(1e-6), "rounding"),
             ("unequal signs", [row(base), row(base, 1.0), row(base)], None)]
    bad = 0
    for name, rows, want in cases:
        r = analyse(rows, [good] * 3, ref, low)
        got = None if r is None else r["verdict"]
        ok = got == want
        bad += not ok
        print(f"  {name}: {got} (expected {want}): {'ok' if ok else 'WRONG'}")
    r = analyse([row(base)] * 3, [good, good, "D 19.0 k_c 79: NOT the record system"], ref, low)
    ok = r is None
    bad += not ok
    print(f"  one log not the record system: {None if r is None else r['verdict']} (expected None): {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    rowf, logf, reff, lam = sys.argv[1:4], sys.argv[4:7], sys.argv[7], float(sys.argv[8])
    pick = lambda f: [json.loads(l) for l in open(f) if l.strip() and json.loads(l)["lam"] == lam][-1]
    rows, logs, ref = [pick(f) for f in rowf], [open(f).read() for f in logf], pick(reff)
    F = [re.search(r"\|F\| ([0-9.e+-]+)", l).group(1) for l in logs]
    for n, r, f in zip((1, 2, 4), rows, F):
        print(f"  {n} thread(s): sign {r['sign']:+.0f}, ln|det| {r['ln']:.10f}, |F| {f}, noise_robust {r['noise_robust']}, float64 sign {r['f64_sign']:+.0f} ln {r['f64_ln']:.10f}, {r['sec']} s")
    print(f"  winb (Windows): sign {ref['sign']:+.0f}, ln|det| {ref['ln']:.10f}, float64 sign {ref['f64_sign']:+.0f} ln {ref['f64_ln']:.10f}, {ref['sec']} s")
    a = analyse(rows, logs, ref)
    if a is None:
        print("REFUSED: a log is not the record system, or the hybrid signs differ among the thread counts")
        sys.exit(1)
    print(f"  relative differences from winb's ln|det| (1, 2, 4 threads): {a['vs'][0]:.3e}, {a['vs'][1]:.3e}, {a['vs'][2]:.3e}; cross-machine (1 thread) {a['cross']:.3e}, half of it {HALF * a['cross']:.3e}")
    print(f"  own relative spread (max - min) / mean |ln|: {a['spread']:.3e}")
    print("  VERDICT: " + TEXT[a["verdict"]])
