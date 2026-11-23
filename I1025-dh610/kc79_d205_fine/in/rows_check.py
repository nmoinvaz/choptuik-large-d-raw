#!/usr/bin/env python3
"""#1025 kc79_d205_fine (dh610) rows_check.py ROWS.jsonl REF.jsonl LAM [LAM ...] | selftest [--mutate]: this machine's d18_hybsign rows of dh170's k_c 79 D 20.5 state at the given lambdas against dh170's rows of the same state
(I1025-dh170/kc79_d205 at 249571b8, copied as in/ref_dh170_k79_scan_D20.5.jsonl, blob b68c0f6d). Passes (exit 0) only if at every lambda the hybrid sign is equal and ln|det| is equal to 1e-9 relative (the bar of
../kc79_d195/in/control_check.py); it also prints whether the ln is bit-identical, the noise signs, the float64 sign and ln. Exit 1 otherwise. selftest: agreeing rows (a + and a - reference) and a 5e-10 relative shift must pass; a sign flip
(both ways) and a 1e-8 relative shift must each fail; --mutate raises the bar to 1e-6, which the 1e-8 case must then fail to catch (exit 1)."""
import sys, json

BAR = 1e-9


def check(row, ref, bar=BAR):
    d = abs(row["ln"] - ref["ln"]) / abs(ref["ln"])
    ok = row["sign"] == ref["sign"] and d <= bar
    return ok, f"lambda {row['lam']}: sign {row['sign']:+.0f} (dh170 {ref['sign']:+.0f}), ln|det| {row['ln']!r} (dh170 {ref['ln']!r}), relative difference {d:.3e} (bar {bar:g}), bit-identical ln {row['ln'] == ref['ln']}, noise {row.get('noise')} (dh170 {ref.get('noise')}), float64 sign {row.get('f64_sign'):+.0f} ln {row.get('f64_ln')!r} (dh170 {ref.get('f64_sign'):+.0f}, {ref.get('f64_ln')!r})"


def selftest(mutate):
    bar = 1e-6 if mutate else BAR
    ref = dict(lam=1.06, sign=-1.0, ln=-2388.144894, noise=[-1, -1], f64_sign=-1.0, f64_ln=-2385.0)
    refm = dict(ref, sign=1.0)
    cases = [("agreeing, - reference", dict(ref), ref, True), ("agreeing, + reference", dict(refm), refm, True),
             ("ln shift 5e-10 relative", dict(ref, ln=ref["ln"] * (1 + 5e-10)), ref, True),
             ("a sign flip (- reference)", dict(ref, sign=1.0), ref, False), ("a sign flip (+ reference)", dict(refm, sign=-1.0), refm, False),
             ("ln shift 1e-8 relative", dict(ref, ln=ref["ln"] * (1 + 1e-8)), ref, False)]
    bad = 0
    for name, row, rf, want in cases:
        got, msg = check(row, rf, bar)
        ok = got == want
        bad += not ok
        print(f"  {name}: {'pass' if got else 'fail'} (expected {'pass' if want else 'fail'}): {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    rd = lambda f: [json.loads(l) for l in open(f) if l.strip()]
    rows, refs = rd(sys.argv[1]), rd(sys.argv[2])
    allok = True
    for lam in map(float, sys.argv[3:]):
        mine = [r for r in rows if abs(r["lam"] - lam) < 1e-9]
        ref = [r for r in refs if abs(r["lam"] - lam) < 1e-9]
        if not mine or not ref:
            print(f"FAIL: lambda {lam}: no row ({len(mine)} mine, {len(ref)} dh170's)")
            allok = False
            continue
        ok, msg = check(mine[-1], ref[-1])
        print(("PASS: " if ok else "FAIL: ") + msg)
        allok &= ok
    sys.exit(0 if allok else 1)
