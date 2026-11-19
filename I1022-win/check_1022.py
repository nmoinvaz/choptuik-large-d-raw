#!/usr/bin/env python3
"""#1022 (win): read-only, no rt_sigma run. Checks the four directional moved states (1e-18, 1e-17) against the stored K 0 samples a, b, c at D 40.020065 (32 x 121, zh + zl), Q_c24.npz (rt_angles --complement) and the x file T1_c24.npz.
d = z' - z_C is formed in double-double (rt_perturb.dd_add) and rounded to a double vector; ac = a - c, bc = b - c the same way; B = p_1 .. p_4 of T1_c24.npz (rt_xcount.count). For each state, with q = Q's row k:
 - realised max|d| / max|z_C| (must equal delta to 1e-6),
 - parallel: max| d / max|d| - q / max|q| | below 1e-9,
 - plane: the part of d inside the plane of ac and bc (QR of [ac, bc]), relative to |d|, below 1e-9 (d is out of the plane),
 - span: the part of d outside span(B), relative to |d|, below 1e-9 (d is in the deep span),
 - mu's share of d (|mu| / max|d|, mu the last entry of z); also |q_0 . q_1| (below 1e-12) and the norms of the rows.
Controls (must FAIL the same check): #972's sum moves (in the plane, so the plane check fails) and this task's two random moves (outside the span, so the span check fails and so does the parallel check). Also: the random move at 1e-18 must equal #963's stored state (I963-win/states/c_d1e-18.npz) in zh and zl (same seed 977).

usage: python -I check_1022.py [--selftest]      (venv-t151 python; the exit code is 1 if a check fails or a control passes)
--selftest: a planted move along a planted q passes, planted d = ac, d = a random combination of the deep span, d = a random vector and d = q plus 1e-6 of noise each fail the right check."""
import os
import sys

import numpy as np

sys.path.insert(0, r"C:\Users\nathan\Source\choptuik-i1018\solver\rt")
import rt_perturb as P
import rt_xcount as XC

R = r"C:\Users\nathan\Source\choptuik-large-d-raw"
HERE = os.path.dirname(os.path.abspath(__file__))
F = {"a": R + r"\I671-win\solves\k0_D40_mutnorows_D40.0201_32x121.npz",
     "b": R + r"\I701-win\solves\k0b_D40_mutnorows_D40.0201_32x121.npz",
     "c": R + r"\I951-win\solves\k0c_D40_mutnorows_D40.0201_32x121.npz"}
XFILE = R + r"\I1006-win\x\T1_c24.npz"
TOL = 1e-9


def cos(u, v):
    return float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)))


def parts(d, q, ac, bc, B):
    E = np.linalg.qr(np.c_[ac, bc])[0]
    return dict(par=float(np.abs(d / np.abs(d).max() - q / np.abs(q).max()).max()),
                plane=float(np.linalg.norm(E.T @ d) / np.linalg.norm(d)),
                span=float(np.linalg.norm(d - B @ (B.T @ d)) / np.linalg.norm(d)),
                cos_q=cos(d, q), cos_ac=cos(d, ac), cos_bc=cos(d, bc), mu_share=float(abs(d[-1]) / np.abs(d).max()))


def ok_of(x):
    return x["par"] < TOL and x["plane"] < TOL and x["span"] < TOL


def selftest():
    rng = np.random.default_rng(1018)
    L, k = 4000, 4
    B = np.linalg.qr(rng.normal(size=(L, k)))[0]
    ac, bc = B @ rng.normal(size=k) * 1e-20, B @ rng.normal(size=k) * 1e-20
    E = np.linalg.qr(np.c_[ac, bc])[0]
    Bp = B - E @ (E.T @ B)
    Q = np.linalg.svd(Bp, full_matrices=False)[0][:, :2]
    q = Q[:, 0]
    bad = 0
    cases = (("planted move along q (relative noise 1e-12)", q + 1e-12 * rng.normal(size=L) * np.abs(q).max(), True),
             ("d = ac", ac, False), ("d = a random combination of the deep span", B @ rng.normal(size=k), False),
             ("d = a random vector", rng.normal(size=L), False), ("d = q plus 1e-6 of noise", q + 1e-6 * rng.normal(size=L) * np.abs(q).max(), False),
             ("d = q1 (the other complement direction, not parallel to q0)", Q[:, 1], False))
    for nm, d, want in cases:
        x = parts(d, q, ac, bc, B)
        ok = ok_of(x)
        good = ok == want
        print(f"  {nm}: check {'passes' if ok else 'fails'} (want {'pass' if want else 'fail'}), parallel {x['par']:.1e}, in the plane {x['plane']:.1e}, outside the span {x['span']:.1e}: {'ok' if good else 'WRONG'}")
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
    X, V, _, _ = XC.read_x(XFILE)
    res = XC.count(X, V)
    B = res["P"][:, :res["d"]]
    Qf = np.load(os.path.join(HERE, "Q_c24.npz"))["q"]
    print(f"max|z_C| {scale:.7e}; max|a - c| {np.abs(ac).max() / scale:.4e}, max|b - c| {np.abs(bc).max() / scale:.4e} (over max|z_C|); T1_c24: d = {res['d']}, B is {B.shape[0]} x {B.shape[1]}")
    print(f"Q_c24 rows: norms {np.linalg.norm(Qf[0]):.15f} and {np.linalg.norm(Qf[1]):.15f}, q_0 . q_1 = {float(Qf[0] @ Qf[1]):.2e}")
    bad = 0 if abs(float(Qf[0] @ Qf[1])) < 1e-12 and abs(np.linalg.norm(Qf[0]) - 1) < 1e-12 and abs(np.linalg.norm(Qf[1]) - 1) < 1e-12 else 1
    print("\n| state | row | delta | realised max abs (z' - z) / max abs z | max abs of d / max abs d - q / max abs q | part in the plane of a - c, b - c | part outside the deep span | cos with a - c | cos with b - c | mu / max-norm | check |\n|---|---|---|---|---|---|---|---|---|---|---|")
    rows = [(f"states/c_q{kq}_d{dl}.npz", kq, dl, True) for kq in (0, 1) for dl in ("1e-18", "1e-17")]
    rows += [(f"../I972-win/states/c_sum_d{dl}.npz", 0, dl, False) for dl in ("1e-20", "1e-19")]
    rows += [(f"states/c_rand_d{dl}.npz", 0, dl, False) for dl in ("1e-18", "1e-17")]
    for rel, kq, dl, want in rows:
        z = np.load(os.path.join(HERE, rel))
        d = diffz(np.asarray(z["zh"], float), np.asarray(z["zl"], float))
        x = parts(d, Qf[kq], ac, bc, B)
        ok = ok_of(x)
        real = float(np.abs(d).max()) / scale
        if want:
            ok = ok and abs(real / float(dl) - 1) < 1e-6
        verdict = ("pass" if ok else "FAIL") if want else ("control: fails as it must" if not ok else "CONTROL PASSED, the check cannot see it")
        bad += (not ok) if want else ok
        print(f"| {os.path.basename(rel)} | {kq if want else 'q_0'} | {dl} | {real:.6e} | {x['par']:.2e} | {x['plane']:.2e} | {x['span']:.2e} | {x['cos_ac']:+.2e} | {x['cos_bc']:+.2e} | {x['mu_share']:.4f} | {verdict} |")
    r63 = np.load(os.path.join(HERE, "..", "I963-win", "states", "c_d1e-18.npz"))
    mine = np.load(os.path.join(HERE, "states", "c_rand_d1e-18.npz"))
    same = np.array_equal(r63["zh"], mine["zh"]) and np.array_equal(r63["zl"], mine["zl"])
    print(f"\nthe random move at 1e-18 against #963's stored c_d1e-18.npz: zh and zl {'equal bit for bit' if same else 'DIFFERENT'}")
    bad += not same
    print("\ncheck_1022", "FAILED" if bad else "passed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
