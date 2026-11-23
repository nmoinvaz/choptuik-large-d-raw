"""#1078: compare two mequil_probe.py record files lambda by lambda.

    python3 mequil_compare.py bit A.jsonl B.jsonl          same sign, ln|det|, pmin and pmax bit for bit (unset against unset)
    python3 mequil_compare.py tol A.jsonl B.jsonl [--abs=1e-11]   same sign and |ln_A - ln_B| <= abs (HP_MODE_EQUIL=1 against unset)
    python3 mequil_compare.py resolved A.jsonl [--abs=1e-6]        within A, pairs of rows at lambdas listed with --pair=L1,L2: same sign and ln within abs
    python3 mequil_compare.py selftest

Exit 0 when every lambda passes, 1 otherwise (also on a lambda missing from one file). The differences are always printed."""
import json
import sys


def rows(path):
    return {r["lam"]: r for r in (json.loads(l) for l in open(path) if l.strip())}


def cmp_bit(a, b):
    bad = 0
    for lam in sorted(set(a) | set(b)):
        if lam not in a or lam not in b:
            print(f"lam {lam!r}: MISSING in {'A' if lam not in a else 'B'}")
            bad += 1
            continue
        x, y = a[lam], b[lam]
        same = (x["sign"] == y["sign"] and x["ln_hex"] == y["ln_hex"] and x["pmin_hex"] == y["pmin_hex"]
                and x["pmax_hex"] == y["pmax_hex"])
        print(f"lam {lam!r}: sign {x['sign']:+.0f} / {y['sign']:+.0f}, ln {x['ln']!r} / {y['ln']!r}, dln {y['ln'] - x['ln']:+.3e}, "
              f"pmin {x['pmin']:.6e} / {y['pmin']:.6e}, pmax {x['pmax']:.6e} / {y['pmax']:.6e}: {'BIT-IDENTICAL' if same else 'DIFFERENT'}")
        bad += not same
    return bad


def cmp_tol(a, b, tol):
    bad = 0
    for lam in sorted(set(a) | set(b)):
        if lam not in a or lam not in b:
            print(f"lam {lam!r}: MISSING in {'A' if lam not in a else 'B'}")
            bad += 1
            continue
        x, y = a[lam], b[lam]
        d = y["ln"] - x["ln"]
        ok = x["sign"] == y["sign"] and abs(d) <= tol
        print(f"lam {lam!r}: sign {x['sign']:+.0f} / {y['sign']:+.0f}, ln {x['ln']!r} / {y['ln']!r}, difference {d:+.3e} (bar {tol:g}), "
              f"pivots A {x['pmin']:.3e}..{x['pmax']:.3e}, B {y['pmin']:.3e}..{y['pmax']:.3e}: {'OK' if ok else 'FAIL'}")
        bad += not ok
    return bad


def cmp_pair(a, pair, tol):
    x, y = a[pair[0]], a[pair[1]]
    d = y["ln"] - x["ln"]
    ok = x["sign"] == y["sign"] and abs(d) <= tol
    print(f"pair {pair[0]!r}, {pair[1]!r}: sign {x['sign']:+.0f} / {y['sign']:+.0f}, ln {x['ln']!r} / {y['ln']!r}, difference {d:+.3e} "
          f"(bar {tol:g}): {'RESOLVED' if ok else 'NOT RESOLVED'}")
    return not ok


def row(lam, sign, ln, pmin=1e-4, pmax=1e3):
    return dict(lam=lam, sign=sign, ln=ln, ln_hex=float(ln).hex(), pmin=pmin, pmin_hex=float(pmin).hex(), pmax=pmax, pmax_hex=float(pmax).hex())


def selftest():
    import contextlib
    import io
    A = {1.0: row(1.0, 1.0, 2000.0), 2.0: row(2.0, -1.0, 2001.5)}
    quiet = io.StringIO()
    with contextlib.redirect_stdout(quiet):
        same = cmp_bit(A, {k: dict(v) for k, v in A.items()}) == 0
        ulp = {k: dict(v) for k, v in A.items()}
        ulp[2.0]["ln"] += 2.3e-13
        ulp[2.0]["ln_hex"] = float(ulp[2.0]["ln"]).hex()
        bit_ulp_fails = cmp_bit(A, ulp) == 1
        sign = {k: dict(v) for k, v in A.items()}
        sign[1.0]["sign"] = -1.0
        bit_sign_fails = cmp_bit(A, sign) == 1
        missing_fails = cmp_bit(A, {1.0: A[1.0]}) == 1
        tol_ok = cmp_tol(A, ulp, 1e-11) == 0
        shifted = {k: dict(v) for k, v in A.items()}
        shifted[1.0]["ln"] += 1e-9
        tol_shift_fails = cmp_tol(A, shifted, 1e-11) == 1
        tol_sign_fails = cmp_tol(A, sign, 1e-11) == 1
        pair_ok = cmp_pair({1.0: row(1.0, 1.0, 10.0), 2.0: row(2.0, 1.0, 10.0 + 1e-9)}, (1.0, 2.0), 1e-6) == 0
        pair_fails = cmp_pair({1.0: row(1.0, 1.0, 10.0), 2.0: row(2.0, -1.0, 12.97)}, (1.0, 2.0), 1e-6) == 1
    checks = dict(same=same, bit_ulp_fails=bit_ulp_fails, bit_sign_fails=bit_sign_fails, missing_fails=missing_fails, tol_ok=tol_ok,
                  tol_shift_fails=tol_shift_fails, tol_sign_fails=tol_sign_fails, pair_ok=pair_ok, pair_fails=pair_fails)
    print("selftest: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks.items()))
    return 0 if all(checks.values()) else 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    o = dict(a[2:].split("=", 1) if "=" in a else (a[2:], "1") for a in sys.argv[1:] if a.startswith("--"))
    if args[:1] == ["selftest"]:
        return selftest()
    if args[:1] == ["bit"] and len(args) == 3:
        bad = cmp_bit(rows(args[1]), rows(args[2]))
    elif args[:1] == ["tol"] and len(args) == 3:
        bad = cmp_tol(rows(args[1]), rows(args[2]), float(o.get("abs", 1e-11)))
    elif args[:1] == ["resolved"] and len(args) == 2 and "pair" in o:
        bad = cmp_pair(rows(args[1]), tuple(float(x) for x in o["pair"].split(",")), float(o.get("abs", 1e-6)))
    else:
        print(__doc__)
        return 2
    print("ALL PASS" if not bad else f"{bad} FAILED")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
