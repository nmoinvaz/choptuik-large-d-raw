# glue (read only, no solver): the pass check of #1003's pilot. sigma_0..sigma_n of a pilot file against the reference's sigma_str, relative to 1e-19.
# Two numbers per order: the complex relative difference |s - r| / |r| (the check), and each part's relative difference where that part exceeds 1e-30 |r| (printed, the reference's
# last digit is the 20th, so a part below that is rounding of its stored digits, not a value). The selftest compares the reference with itself (must pass) and with sigma_7 scaled
# by 1 + 1e-15 (must fail), as the check has to be able to fail.
# usage: python -I cmp1003.py PILOT.json REF.json [N=12]     python -I cmp1003.py --selftest REF.json [N=12]
import json, sys
from mpmath import mp, mpf, mpc
mp.dps = 60
TOL = mpf('1e-19')


def load(p):
    return [mpc(mpf(a), mpf(b)) for a, b in json.load(open(p))['sigma_str']]


def compare(s, r, n, verbose=True):
    ok = True
    for k in range(n + 1):
        rel = abs(s[k] - r[k]) / abs(r[k])
        pr = abs(s[k].real - r[k].real) / abs(r[k].real) if abs(r[k].real) > mpf('1e-30') * abs(r[k]) else None
        pi = abs(s[k].imag - r[k].imag) / abs(r[k].imag) if abs(r[k].imag) > mpf('1e-30') * abs(r[k]) else None
        good = rel <= TOL and (pr is None or pr <= TOL) and (pi is None or pi <= TOL)
        ok = ok and good
        if verbose:
            print('sigma_%-2d complex %.3e  real part %s  imag part %s  %s' % (k, float(rel), ('%.3e' % pr) if pr is not None else 'n/a (below 1e-30 |r|)',
                  ('%.3e' % pi) if pi is not None else 'n/a (below 1e-30 |r|)', 'ok' if good else 'FAILS'))
    return ok


if __name__ == '__main__':
    if sys.argv[1] == '--selftest':
        r = load(sys.argv[2]); n = int(sys.argv[3]) if len(sys.argv) > 3 else 12
        a = compare(r, r, n, False)
        m = list(r); m[7] = m[7] * (1 + mpf('1e-15'))
        b = compare(m, r, n, False)
        print('selftest: reference against itself passes: %s; with sigma_7 x (1 + 1e-15) it passes: %s (must be False)' % (a, b))
        sys.exit(0 if a and not b else 1)
    s, r = load(sys.argv[1]), load(sys.argv[2]); n = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    ok = compare(s, r, n)
    print('PASS' if ok else 'FAIL', 'sigma_0..sigma_%d to 1e-19 relative' % n)
    sys.exit(0 if ok else 1)
