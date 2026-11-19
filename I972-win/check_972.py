#!/usr/bin/env python3
"""#972 (win): read-only, no rt_sigma run. Checks the four moved states against the stored K 0 samples a, b, c at D 40.020065 (32 x 121, zh + zl).
d = z' - z_C is formed in double-double (rt_perturb.dd_add) and rounded to a double vector; ac = a - c, bc = b - c the same way. For each state:
 - realised max|d| / max|z_C| (must equal delta to 1e-6),
 - cos(d, ac) and cos(d, bc),
 - the part of d outside the plane of ac and bc (QR of [ac, bc]), relative to |d|,
 - orth: cos(d, ac) below 1e-9 and the part outside the plane below 1e-9 (the issue's selftest bounds); sum: max| d / max|d| - r / max|r| | below 1e-9, r = ac / max|ac| + bc / max|bc|,
 - mu's share of d (|mu| / max|d|, mu the last entry of z).
Control: the same orth check on #969's along-b states (I969-win/states) must FAIL (cos with ac is about 0.234), and the sum check on the orth states must FAIL.

usage: python -I check_972.py [--selftest]      (venv-t151 python; the exit code is 1 if a check fails or a control passes)
--selftest: planted ac, bc, d orth and sum pass, planted d = bc fails the orth check, planted d = ac fails the sum check."""
import os
import sys

import numpy as np

sys.path.insert(0, r"C:\Users\nathan\Source\choptuik-i972\solver\rt")
import rt_perturb as P

R = r"C:\Users\nathan\Source\choptuik-large-d-raw"
HERE = os.path.dirname(os.path.abspath(__file__))
F = {"a": R + r"\I671-win\solves\k0_D40_mutnorows_D40.0201_32x121.npz",
     "b": R + r"\I701-win\solves\k0b_D40_mutnorows_D40.0201_32x121.npz",
     "c": R + r"\I951-win\solves\k0c_D40_mutnorows_D40.0201_32x121.npz"}
TOL = 1e-9


def cos(u, v):
    return float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)))


def outside(d, ac, bc):
    B = np.linalg.qr(np.c_[ac, bc])[0]
    return float(np.linalg.norm(d - B @ (B.T @ d)) / np.linalg.norm(d))


def sum_dir(ac, bc):
    r = ac / np.abs(ac).max() + bc / np.abs(bc).max()
    return r / np.abs(r).max()


def check(mode, d, ac, bc):
    """returns (ok, numbers)"""
    c1, out = abs(cos(d, ac)), outside(d, ac, bc)
    sdev = float(np.abs(d / np.abs(d).max() - sum_dir(ac, bc)).max())
    ok = (c1 < TOL and out < TOL) if mode == "orth" else sdev < TOL
    return ok, dict(cos_ac=cos(d, ac), cos_bc=cos(d, bc), out=out, sum_dev=sdev, mu_share=float(abs(d[-1]) / np.abs(d).max()))


def selftest():
    rng = np.random.default_rng(8)
    L = 4000
    ac, bc = rng.normal(size=L) * 1e-20, rng.normal(size=L) * 1e-20 + 0.2 * rng.normal(size=L) * 1e-20
    bc += 0.3 * ac
    o = bc - (bc @ ac) / (ac @ ac) * ac
    s = sum_dir(ac, bc)
    bad = 0
    for nm, mode, d, want in (("orth", "orth", o, True), ("sum", "sum", s, True), ("d = bc as orth", "orth", bc, False), ("d = ac as sum", "sum", ac, False), ("d = sum as orth", "orth", s, False), ("d = orth as sum", "sum", o, False)):
        ok, x = check(mode, d, ac, bc)
        good = ok == want
        print(f"  planted {nm}: check {'passes' if ok else 'fails'} (want {'pass' if want else 'fail'}), cos with ac {x['cos_ac']:+.2e}, outside the plane {x['out']:.1e}, sum deviation {x['sum_dev']:.1e}: {'ok' if good else 'WRONG'}")
        bad += not good
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    Z = {}
    for k, p in F.items():
        d = np.load(p)
        Z[k] = (np.asarray(d["zh"], float), np.asarray(d["zl"], float))
    scale = float(np.abs(Z["c"][0] + Z["c"][1]).max())

    def diffz(h, l):
        dh, dl = P.dd_add(h, l, -Z["c"][0], -Z["c"][1])
        return dh + dl

    ac, bc = diffz(*Z["a"]), diffz(*Z["b"])
    print(f"max|z_C| {scale:.7e}; max|a - c| {np.abs(ac).max() / scale:.4e}, max|b - c| {np.abs(bc).max() / scale:.4e} (over max|z_C|), cos(a - c, b - c) {cos(ac, bc):.9f}")
    print("\n| state | mode | delta | realised max abs (z' - z) / max abs z | cos with a - c | cos with b - c | part outside the plane | max abs deviation from the sum direction | mu / max-norm | check |\n|---|---|---|---|---|---|---|---|---|---|")
    bad = 0
    rows = [(f"states/c_{m}_d{dl}.npz", m, dl, True) for m in ("orth", "sum") for dl in ("1e-20", "1e-19")]
    rows += [(f"../I969-win/states/c_alongb_d{dl}.npz", "orth", dl, False) for dl in ("1e-20", "1e-19")]
    rows += [(f"states/c_orth_d{dl}.npz", "sum", dl, False) for dl in ("1e-20", "1e-19")]
    for rel, mode, dl, want in rows:
        z = np.load(os.path.join(HERE, rel))
        d = diffz(np.asarray(z["zh"], float), np.asarray(z["zl"], float))
        ok, x = check(mode, d, ac, bc)
        real = float(np.abs(d).max()) / scale
        if want:
            ok = ok and abs(real / float(dl) - 1) < 1e-6
        verdict = ("pass" if ok else "FAIL") if want else ("control: fails as it must" if not ok else "CONTROL PASSED, the check cannot see it")
        bad += (not ok) if want else ok
        print(f"| {os.path.basename(rel)} | {mode} | {dl} | {real:.6e} | {x['cos_ac']:+.3e} | {x['cos_bc']:+.3e} | {x['out']:.2e} | {x['sum_dev']:.2e} | {x['mu_share']:.4f} | {verdict} |")
    print("\ncheck_972", "FAILED" if bad else "passed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
