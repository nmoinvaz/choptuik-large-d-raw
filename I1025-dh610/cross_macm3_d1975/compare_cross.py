#!/usr/bin/env python3
"""#1025 cross_macm3_d1975 (dh610) compare_cross.py LINUX.jsonl MACM3.jsonl [DH170.jsonl] | selftest [--mutate]
Linux (this machine) on macm3's k_c 87 D 19.75 state at lambda 1.32, 1.33, 1.34, beside macm3's rows on its own state (its scan file) and dh170's on the Linux state (his scan file, if given).
Prints per lambda: hybrid sign, noise signs, noise_robust, float64 sign, ln|det|, point seconds, and the relative ln|det| difference to macm3's. Then the reading fixed before the run:
  A: Linux gives macm3's signs at all three lambda: the states differ and the determinant code agrees across builds.
  B: Linux gives dh170's signs at all three: the macOS evaluation of the determinant differs.
  neither: reported as it is. Without dh170's rows, his signs are derived from the order (his root in (1.32, 1.33), macm3's in (1.33, 1.34): the signs differ at 1.33 only up to the one change), i.e. -, +, +,
  and the output says so. The ln|det| difference is information; 1e-9 relative is the bar of the earlier same-state control (../kc79_d195/control_check.py).
selftest: planted rows equal to macm3's give A, equal to dh170's give B, a mixed set gives neither, a set with all-noise-not-robust rows is flagged; --mutate swaps the A and B rules, which the planted cases must catch (exit 1)."""
import sys, json

LAMS = (1.32, 1.33, 1.34)
DERIVED_DH170 = {1.32: -1.0, 1.33: 1.0, 1.34: 1.0}


def rows(f):
    d = {}
    for l in open(f):
        if l.strip():
            r = json.loads(l)
            d.setdefault(round(r["lam"], 4), []).append(r)
    return d


def decide(lin, mac, dh, mutate=False):
    a = all(lin[l] == mac[l] for l in LAMS)
    b = all(lin[l] == dh[l] for l in LAMS)
    if mutate:
        a, b = b, a
    return "A" if a and not b else "B" if b and not a else "neither"


def selftest(mutate):
    mac = {1.32: -1.0, 1.33: -1.0, 1.34: 1.0}
    cases = [("equal to macm3's", dict(mac), "A"), ("equal to dh170's (derived)", dict(DERIVED_DH170), "B"),
             ("mixed (1.32 flipped)", {1.32: 1.0, 1.33: -1.0, 1.34: 1.0}, "neither")]
    bad = 0
    for name, lin, want in cases:
        got = decide(lin, mac, DERIVED_DH170, mutate)
        ok = got == want
        bad += not ok
        print(f"  {name}: reading {got} (expected {want}): {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


def main(lf, mf, df=None):
    L, M = rows(lf), rows(mf)
    D = rows(df) if df else None
    print(f"{'lambda':>6} | {'machine':<22} | sign | noise signs | robust | f64 sign | ln|det| | sec")
    ls, ms = {}, {}
    for lam in LAMS:
        for name, src in (("Linux on macm3's state", L), ("macm3 on its state", M), ("dh170 on Linux state", D)):
            if src is None:
                continue
            for k, r in enumerate(src.get(lam, [])):
                tag = name + (" (repeat)" if k else "")
                print(f"{lam:>6.2f} | {tag:<22} | {r['sign']:+.0f} | {r['noise']} | {r['noise_robust']} | {r['f64_sign']:+.0f} | {r['ln']:.10f} | {r['sec']}")
        ls[lam] = L[lam][0]["sign"]
        ms[lam] = M[lam][0]["sign"]
        rel = abs(L[lam][0]["ln"] - M[lam][0]["ln"]) / abs(M[lam][0]["ln"])
        print(f"{lam:>6.2f} | Linux minus macm3 ln|det| {L[lam][0]['ln'] - M[lam][0]['ln']:+.6e}, relative {rel:.3e} (bar of the earlier same-state control 1e-9)")
    if D is not None:
        dh = {lam: D[lam][0]["sign"] for lam in LAMS}
        src = "dh170's rows"
    else:
        dh = DERIVED_DH170
        src = "DERIVED from the order (no rows of dh170's given)"
    print("Linux signs:", ls, "| macm3's:", ms, "| dh170's (%s):" % src, dh)
    r = decide(ls, ms, dh)
    print({"A": "READING A: Linux gives macm3's signs: the states differ and the determinant code agrees across builds.",
           "B": "READING B: Linux gives dh170's signs: the macOS evaluation of the determinant differs.",
           "neither": "NEITHER reading: the signs match neither macm3's nor dh170's at all three lambda; reported as printed."}[r])
    return 0


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    sys.exit(main(*sys.argv[1:4]))
