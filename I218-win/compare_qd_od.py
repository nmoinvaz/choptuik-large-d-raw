"""#218: the quad-double and octo-double correctors on the same saved state, read from the logs of #215.

    python3 compare_qd_od.py [RAW_ROOT] LOG [LOG ...] [--mutate=shift=5e-18] [--selftest]

Each log holds a qd run followed by an od run (appended with >>). The od run's first Newton solve re-corrects its
base state, which is the state the qd run saved, so the od block that ends at a `base ... corrector od` line is the
od correction of the qd result. The pair is accepted only when the od block's starting max|F| equals the qd
converged line's (the same state, at the log's three digits). Reported per pair:

    Delta_qd, Delta_od (hi + lo, exact decimals), their difference, the same difference from the od steps' dDelta
    column (a second field of the log: the two must agree to 1e-20), the od first step's |dz|, the final max|F|.

Criteria (#218): od reaches max|F| < 1e-40, and |Delta_od - Delta_qd| < 1e-18. Exits 1 when any check fails.
--mutate=shift=X adds X to every od Delta before the comparison (the control: it must trip the criterion and the
dDelta consistency check). --selftest runs the planted cases and the control and exits 0 only if they behave."""
import re
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60
CONV = re.compile(r"^\s+(qn|on) (\d+): \|F\| (\S+) converged, Delta (\d\.\d+) ([+-]\d\.\d+e[+-]\d+)")
ONSTEP = re.compile(r"^\s+on (\d+): \|F\| (\S+) -> (\S+), \|dz\| (\S+) -> (\S+), lam (\S+), dDelta ([+-]\S+?),")
BASE = re.compile(r"^base (\S+): D (\S+), .*corrector od")
F_MAX, DD_MAX, CONSIST = Decimal("1e-40"), Decimal("1e-18"), Decimal("1e-20")


def pairs(lines):
    """[(base path, D, qd conv, od conv, od steps)] for every od base polish in the log"""
    out, qd, od, steps = [], [], None, []
    for i, ln in enumerate(lines):
        if ln.startswith("held values from the fit"):
            od, steps = [], []
        m = CONV.match(ln)
        if m:
            kind, k, f, hi, lo = m.groups()
            e = dict(k=int(k), F=f, delta=Decimal(hi) + Decimal(lo), line=i + 1)
            if kind == "qn":
                qd.append(e)
            elif od is not None:
                od.append(e)
        m = ONSTEP.match(ln)
        if m and od is not None:
            n, f0, f1, dz0, dz1, lam, dd = m.groups()
            steps.append(dict(k=int(n), F0=f0, F1=f1, dz0=Decimal(dz0), dDelta=Decimal(dd), line=i + 1))
        m = BASE.match(ln)
        if m and od:
            if not steps or steps[0]["k"] != 0:
                raise SystemExit(f"line {i + 1}: od block without a step 0")
            match = [q for q in qd if q["F"] == steps[0]["F0"]]
            if not match:
                raise SystemExit(f"line {i + 1}: no qd converged line with max|F| {steps[0]['F0']} (the od start)")
            out.append((m.group(1), m.group(2), match[-1], od[-1], list(steps)))
        if m:
            od, steps = None, []
    return out


def check(rows, shift=Decimal(0)):
    bad, res = 0, []
    for path, D, q, o, steps in rows:
        d_od = o["delta"] + shift
        diff = d_od - q["delta"]
        dsum = sum(s["dDelta"] for s in steps)
        fod = Decimal(o["F"])
        ok_f, ok_d, ok_c = fod < F_MAX, abs(diff) < DD_MAX, abs(diff - dsum) < CONSIST
        bad += (not ok_f) + (not ok_d) + (not ok_c)
        res.append(dict(path=path, D=D, qdF=q["F"], odF=o["F"], diff=diff, dsum=dsum, dz0=steps[0]["dz0"], n_od=len(steps),
                        ok_f=ok_f, ok_d=ok_d, ok_c=ok_c, qd_line=q["line"], od_line=o["line"]))
    return bad, res


def show(res):
    print(f"{'state':44} {'qd max|F|':>10} {'od max|F|':>10} {'steps taken':>11} {'od |dz|0':>9} {'D_od-D_qd':>11} {'sum dDelta':>11}  F<1e-40  |dD|<1e-18  consistent")
    for r in res:
        print(f"{r['path']:44} {r['qdF']:>10} {r['odF']:>10} {r['n_od']:>11} {float(r['dz0']):>9.1e} {float(r['diff']):>+11.3e} "
              f"{float(r['dsum']):>+11.3e}  {'ok' if r['ok_f'] else 'FAIL':7} {'ok' if r['ok_d'] else 'FAIL':11} {'ok' if r['ok_c'] else 'FAIL'}")


def selftest(rows):
    """planted: a synthetic log with a known shift; control: the mutation must flip the real d6 row"""
    syn = ["held values from the fit x\n",
           "  qn 0: |F| 1.00e-29 converged, Delta 1.5 +1.0000e-17\n",
           "held values from the fit x\n",
           "  on 0: |F| 1.00e-29 -> 1.0e-35, |dz| 3.0e-19 -> 1.0e-36, lam 1, dDelta +3.00e-19, piv 1, 1 s\n",
           "  on 1: |F| 1.0e-35 -> 1.0e-45, |dz| 1.0e-36 -> 1.0e-59, lam 1, dDelta -1.00e-36, piv 1, 1 s\n",
           "  on 2: |F| 1.00e-45 converged, Delta 1.5 +1.0300e-17\n",
           "base s.npz: D 1.0, M 32, corrector od (junk_only False)\n"]
    p = pairs(syn)
    bad, r = check(p)
    ok = [bad == 0, r[0]["diff"] == Decimal("3.0e-19")]
    bad_m, r_m = check(p, Decimal("5e-18"))
    ok += [bad_m == 2 and not r_m[0]["ok_d"] and not r_m[0]["ok_c"]]
    if rows:
        bad_c, r_c = check(rows, Decimal("5e-18"))
        d6 = [x for x in r_c if "chain_d6" in x["path"]]
        ok += [bool(d6) and not d6[0]["ok_d"] and not d6[0]["ok_c"]]
    print("selftest planted/control:", ok)
    return 0 if all(ok) else 1


def main(argv):
    mutate, run_self, args = Decimal(0), False, []
    for a in argv:
        if a.startswith("--mutate"):
            mutate = Decimal(a.split("shift=", 1)[1])
        elif a == "--selftest":
            run_self = True
        else:
            args.append(a)
    root = args[0] if args and not args[0].endswith(".log") else ""
    logs = [a for a in args if a.endswith(".log")]
    rows = []
    for lg in logs:
        with open(lg if not root else f"{root}/{lg}") as fh:
            rows += pairs(fh.readlines())
    if run_self:
        return selftest(rows)
    bad, res = check(rows, mutate)
    show(res)
    print(f"{len(res)} pairs, {bad} failed checks" + (f" (mutate shift {mutate})" if mutate else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
