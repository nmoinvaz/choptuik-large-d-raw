#!/usr/bin/env python3
"""xcheck1064.py A.npz B.npz DELTA.json [--mutate] | --planted REF.npz WORKDIR [--mutate]: check of exact_recip_check.py delta (#1064's Delta(K) - Delta(293)).
Pair mode: Delta of each state is its last component with the eight parts summed as exact rationals (cmp1060.py's exact(), Fractions, a second implementation of the
sum that exact_recip_check.py does at 600 bits in mpmath); passes when DELTA.json's Delta(b) - Delta(a) agrees with it to 1e-30 absolute and D_str of both
states agree to 50 digits (the issue's 'same D'). --mutate moves the Fraction side by 1e-25, which must fail. Planted mode (before the real states): REF with its exact
sums moved by cmp1060.py plant 1e-20 (known shift EPS*max|S|*s_last on the last component), exact_recip_check.py delta REF PLANT, which must give that shift to 1e-30
and pass the pair check; --mutate in planted mode expects a shift 1e-25 off, which must fail. Exit 0 pass, 1 fail, 2 unreadable input."""
import json
import os
import subprocess
import sys
from fractions import Fraction

import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "I1060-win2"))
import cmp1060  # noqa: E402

mp.mp.prec = 600
BOUND = mp.mpf("1e-30")


def frac_delta(path):
    d = cmp1060.load(path)
    return cmp1060.exact(d)[-1], cmp1060.meta(d)["D_str"]


def pair(a, b, jpath, mutate):
    (da, Da), (db, Db) = frac_delta(a), frac_delta(b)
    j = json.load(open(jpath))
    mine = mp.mpf(db.numerator) / db.denominator - mp.mpf(da.numerator) / da.denominator + (mp.mpf("1e-25") if mutate else 0)
    theirs = mp.mpf(j["Delta_b"]) - mp.mpf(j["Delta_a"])
    ok_d = abs(mine - theirs) <= BOUND
    ok_D = Da[:52] == Db[:52] and bool(j["same_D"])
    print(f"  Delta(b) - Delta(a): exact_recip_check {mp.nstr(theirs, 15)}, exact sums {mp.nstr(mine, 15)}{' (--mutate, moved by 1e-25)' if mutate else ''}: "
          f"difference {mp.nstr(mine - theirs, 3)} (bound 1e-30): {'ok' if ok_d else 'FAIL'}")
    print(f"  D_str to 50 digits equal {Da[:52] == Db[:52]}, same_D in the record {j['same_D']}: {'ok' if ok_D else 'FAIL'}")
    return ok_d and ok_D


def planted(ref, work, mutate):
    os.makedirs(work, exist_ok=True)
    eps = "1e-20"
    pl, js = f"{work}/planted_{eps}.npz", f"{work}/planted_{eps}.json"
    r = subprocess.run([sys.executable, os.path.join(HERE, "..", "I1060-win2", "cmp1060.py"), "plant", eps, ref, pl], capture_output=True, text=True)
    if r.returncode:
        print(r.stdout, r.stderr)
        return 2
    S = cmp1060.sums(cmp1060.load(ref))
    mx = max(abs(x) for x in S)
    s_last = mp.mpf(((len(S) - 1) * 7919) % 13 - 6) / 6
    truth = mp.mpf(eps) * mx * s_last
    r = subprocess.run([sys.executable, "exact_recip_check.py", "delta", ref, pl, "--out", js], capture_output=True, text=True)
    if r.returncode not in (0, 1):
        print(r.stdout, r.stderr)
        return 2
    j = json.load(open(js))
    got = mp.mpf(j["Delta_b"]) - mp.mpf(j["Delta_a"])
    want = truth + (mp.mpf("1e-25") if mutate else 0)
    ok_t = abs(got - want) <= BOUND and truth != 0
    print(f"planted: shift EPS*max|S|*s_last = {mp.nstr(truth, 10)}; exact_recip_check delta gives {mp.nstr(got, 10)}{' (--mutate, expected moved by 1e-25)' if mutate else ''}: "
          f"difference {mp.nstr(got - want, 3)} (bound 1e-30, truth nonzero): {'ok' if ok_t else 'FAIL'}")
    ok_p = pair(ref, pl, js, False)
    return 0 if ok_t and ok_p else 1


if __name__ == "__main__":
    mut = "--mutate" in sys.argv
    args = [x for x in sys.argv[1:] if x != "--mutate"]
    if args[0] == "--planted":
        rc = planted(args[1], args[2], mut)
    else:
        rc = 0 if pair(args[0], args[1], args[2], mut) else 1
    print("xcheck", {0: "PASS", 1: "FAIL", 2: "ERROR"}[rc])
    sys.exit(rc)
