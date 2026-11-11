#!/usr/bin/env python3
"""#519, additions to analysis_519.py after its first result (the deviation of Delta from a polynomial in 1/n is dominated by the ends of the range, and no period was found by the scan):
1. the deviation of Delta from the degree 5 and degree 7 polynomials (fitted over all 40 states) at each state;
2. the amplitude of a sinusoid of FIXED period 2.74 (and 2.72, 2.24) fitted to the deviation (a line + the sinusoid, no scan) over D 228.13 to 237.13 and over D 224 to 242.5, with its error;
3. the polynomials fitted on narrower windows (D 224 to 242.53, D 228 to 237.2) and their difference between degree 5 and 7 at D 230 (the error bar over the degree depends on the window).
usage: python extra_519.py"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis_519 as a  # noqa: E402


def fixed_period_fit(D, y, P):
    Dm = D.mean()
    X = np.column_stack([np.ones_like(D), D - Dm, np.cos(2 * np.pi * D / P), np.sin(2 * np.pi * D / P)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ beta
    dof = len(D) - 4
    cov = (r @ r) / dof * np.linalg.inv(X.T @ X)
    A, B = beta[2], beta[3]
    amp = np.hypot(A, B)
    g = np.array([A, B]) / amp
    return amp, float(np.sqrt(g @ cov[2:4, 2:4] @ g)), float(np.sqrt(np.mean(r ** 2)))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    series = a.states()
    Ds = sorted(series)
    D = np.array(Ds)
    ref = series[Ds[-1]][0]
    dl = np.array([float(series[d][0] - ref) for d in Ds])
    dev5, m5 = a.polydev(D, dl, 5)
    dev7, m7 = a.polydev(D, dl, 7)
    print("1. deviation of Delta from the polynomials in 1/n fitted over all 40 states")
    print("| D | Delta - Delta(last) | dev degree 5 | dev degree 7 |")
    print("|---|---|---|---|")
    for d, v, e5, e7 in zip(D, dl, dev5, dev7):
        print(f"| {d:.4f} | {v:+.12e} | {e5:+.3e} | {e7:+.3e} |")
    print("\n2. sinusoid of fixed period fitted to the deviation (line + sinusoid, no scan); amplitude +- error, rms residual")
    for name, sel in (("D 228.13 to 237.13", (D >= 228.0) & (D <= 237.2)), ("D 224 to 242.53", D >= 224.0)):
        for deg, dev in ((5, dev5), (7, dev7)):
            for P in (2.74, 2.72, 2.24):
                amp, err, rms = fixed_period_fit(D[sel], dev[sel], P)
                print(f"  {name}, degree {deg}, P = {P}: amplitude {amp:.3e} +- {err:.1e} (ratio {amp / err:.1f}), rms residual {rms:.2e}")
    print("\n3. the polynomials fitted on windows: difference of the degree 5 and the degree 7 polynomial at D 230, and the rms deviation of each in the window")
    for name, lo, hi in (("D 216.13 to 242.53 (all)", 0, 1e9), ("D 224 to 242.53", 224.0, 1e9), ("D 228 to 237.2", 228.0, 237.2)):
        sel = (D >= lo) & (D <= hi)
        if sel.sum() < 9:
            continue
        d5, mm5 = a.polydev(D[sel], dl[sel], 5)
        d7, mm7 = a.polydev(D[sel], dl[sel], 7)
        diff230 = float(a.evalpoly(mm5, np.array([230.0]))[0] - a.evalpoly(mm7, np.array([230.0]))[0])
        print(f"  {name}: N {int(sel.sum())}, |poly5 - poly7| at D 230 = {abs(diff230):.3e}, rms deviation degree 5 {np.sqrt(np.mean(d5 ** 2)):.3e}, degree 7 {np.sqrt(np.mean(d7 ** 2)):.3e}")
