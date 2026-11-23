#!/usr/bin/env python3
"""#1025 repro_d1975 (dh610) repro_read.py read STATE8 STATE6 REC8 REC6 COND6.json ROW6_1.32 ROW6_1.33 ROW8_1.32 ROW8_1.33 | selftest [--mutate]
The reproducibility test: the same ell_refine run from dh170's state (352107a8) with 8 threads (linRe, ../reconv_d1975) and with 6 (linRe6). Prints whether the two states are bit for bit equal, their difference (L2, Delta included, max entry, Delta entry), the
records, ell_cond's dz beside the computed one, ln|det| of both at 1.32 and 1.33, the two-point det-linear root of each and its move, and the reading by the rules written before the run:
  R0: the two states are equal bit for bit (the move of linRe from dh170's state came from the re-convergence itself, not from rounding);
  R1: 5e-11 <= norm dz <= 2e-9 (the coordinator's about 1e-10 to 1e-9, a factor 2 either side) and the root moves by 2e-4 or more (one regrid at D 19.75 is reproducible only to about 0.002);
  R2: anything else; the numbers are reported.
Exit 0 after printing. selftest exits 0 only if every planted case reads as written; --mutate widens R1's band to [1e-13, 1], which the 3e-9 case must then fail to catch (exit 1)."""
import sys, json, math
import numpy as np

LO, HI, ROOT_BAR = 5e-11, 2e-9, 2e-4


def classify(equal, dz, rootmove, lo=LO, hi=HI):
    if equal:
        return "R0"
    if rootmove is not None and lo <= dz <= hi and abs(rootmove) >= ROOT_BAR:
        return "R1"
    return "R2"


def root2(r1, r2):
    if r1["sign"] == r2["sign"]:
        return None
    return 1.32 + 0.01 / (1.0 + math.exp(r2["ln"] - r1["ln"]))


def last(f, lam=None):
    rows = [json.loads(l) for l in open(f) if l.strip()]
    return [r for r in rows if lam is None or abs(r["lam"] - lam) < 1e-9][-1]


def selftest(mutate):
    lo, hi = (1e-13, 1.0) if mutate else (LO, HI)
    cases = [("bit for bit equal", True, 0.0, 0.0, "R0"), ("3e-10 apart, root moves 5e-4", False, 3e-10, 5e-4, "R1"), ("3e-10 apart, root moves 1e-4", False, 3e-10, 1e-4, "R2"),
             ("3e-9 apart, root moves 5e-4 (outside the band)", False, 3e-9, 5e-4, "R2"), ("1e-11 apart, root moves 5e-4 (outside the band)", False, 1e-11, 5e-4, "R2"),
             ("3e-10 apart, no root", False, 3e-10, None, "R2"), ("equal wins over a root move", True, 0.0, 9.0, "R0")]
    bad = 0
    for name, eq, dz, rm, want in cases:
        got = classify(eq, dz, rm, lo, hi)
        ok = got == want
        bad += not ok
        print(f"  {name}: read {got}, wanted {want}: {'ok' if ok else 'WRONG'}")
    a = np.arange(5.0); b = a.copy(); b[3] += 1e-12
    for name, got, want in [("array_equal on equal arrays", bool(np.array_equal(a, a.copy())), True), ("array_equal after a 1e-12 change", bool(np.array_equal(a, b)), False)]:
        ok = got == want
        bad += not ok
        print(f"  {name}: {got}: {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    s8f, s6f, r8f, r6f, cf, m132, m133, o132, o133 = sys.argv[2:11]
    z8, z6 = np.load(s8f), np.load(s6f)
    equal = bool(np.array_equal(z8, z6))
    d = z6 - z8
    dz = float(np.linalg.norm(d))
    nd = int(np.count_nonzero(d))
    imax = int(np.argmax(np.abs(d)))
    print(f"states: {len(z8)} entries; bit for bit equal: {equal}; entries that differ: {nd}; norm dz (L2, Delta included) {dz:.4e}; max entry {abs(d[imax]):.4e} (index {imax}); Delta entry of dz {d[-1]:+.4e} (Delta {z8[-1]!r} against {z6[-1]!r})")
    r8, r6 = last(r8f), last(r6f)
    print("| record | 8 threads (linRe) | 6 threads (linRe6) |")
    print("|---|---|---|")
    for k in ("F_start", "F", "steps", "constraint", "Delta", "dDelta_dF", "lam_gauge", "seconds"):
        print(f"| {k} | {r8.get(k)!r} | {r6.get(k)!r} |")
    try:
        c = json.load(open(cf))
        print(f"ell_cond: norm dz {c['dz']:.4e} (computed here {dz:.4e}, relative difference {abs(c['dz'] - dz) / max(dz, 1e-300):.1e}), norm F(A) {c['FA']:.4e}, norm F(B) {c['FB']:.4e}, part of dz outside the 8 smallest right singular vectors {c['rest']:.4e}, norm J dz {c['lin']:.4e}, norm F(B) - F(A) {c['dF']:.4e}")
    except Exception as e:
        print(f"ell_cond json not read ({type(e).__name__}); norm dz computed here")
    a132, a133, b132, b133 = last(o132, 1.32), last(o133, 1.33), last(m132, 1.32), last(m133, 1.33)
    sg = lambda s: "+" if s > 0 else "-"
    print("| lambda | ln of abs det, 8 threads (linRe) | ln of abs det, 6 threads (linRe6) | difference | signs (8, 6) | noise robust (8, 6) | float64 sign (8, 6) |")
    print("|---|---|---|---|---|---|---|")
    for lam, a, b in ((1.32, a132, b132), (1.33, a133, b133)):
        print(f"| {lam:.2f} | {a['ln']!r} | {b['ln']!r} | {b['ln'] - a['ln']:+.3e} | {sg(a['sign'])}, {sg(b['sign'])} | {a['noise_robust']}, {b['noise_robust']} | {sg(a['f64_sign'])}, {sg(b['f64_sign'])} |")
    ra, rb = root2(a132, a133), root2(b132, b133)
    rm = None if ra is None or rb is None else rb - ra
    print(f"two-point det-linear root in (1.32, 1.33): 8 threads {ra if ra is None else format(ra, '.6f')}, 6 threads {rb if rb is None else format(rb, '.6f')}, move (6 minus 8) {rm if rm is None else format(rm, '+.6f')}")
    print(f"reading by the rules written before the run: {classify(equal, dz, rm)}  [R0 bit for bit equal; R1 5e-11 <= norm dz <= 2e-9 and root move >= 2e-4; R2 otherwise]")
