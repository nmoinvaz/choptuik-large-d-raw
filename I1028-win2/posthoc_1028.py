"""#1028, added AFTER the pre-registered reading (17:27 UTC, once the four end values were read): descriptive only, not part of the decision.
The reading's error figure std_norm / sigma_min(J) is a worst-case bound (the whole scatter taken along J's weakest direction). Here the same r_1 values are mapped through J^-1
(#1012's J, rows re/im, columns A, w/w_inf) to the shift each one implies for the zero in (A, w/w_inf), and the scatter of those shifts is reported per axis.

    python posthoc_1028.py LOG [LOG ...]      (the logs whose FIXED-A r_1 enter, stage 1 first)
    python posthoc_1028.py --selftest [--mutate=sign]
"""
import re, sys
import numpy as np

J = np.array([[3231770000.0, -17235660000.0], [25042500000.0, 49981000000.0]])     # #1012's m9_outer_result.txt


def r1_of(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"FIXED-A M \d+: A ([0-9.]+)\s+w/w_inf ([0-9.]+).*?r_1 ([+-][0-9.]+e[+-]\d+)([+-][0-9.]+e[+-]\d+)i", t)
    return None if not m else np.array([float(m.group(3)), float(m.group(4))])


def shifts(R, Jm=J):
    """zero-shift implied by each r_1: -J^-1 r_1, as (dA, dw/w_inf) rows."""
    return -np.linalg.solve(Jm, np.asarray(R, float).T).T


def selftest(mut):
    rng = np.random.default_rng(1028)
    d = rng.normal(0, 1e-4, size=(50, 2))                         # planted shifts of the zero
    R = -(J @ d.T).T                                              # the r_1 they would produce
    back = shifts(R, J * np.array([[1, -1], [1, -1]]) if mut == "sign" else J)
    err = np.abs(back - d).max() / np.abs(d).max()
    print(f"planted shifts recovered through J^-1: max relative error {err:.1e} -> {'ok' if err < 1e-9 else 'FAIL'}")
    sv = np.linalg.svd(J, compute_uv=False)
    sd = shifts(rng.normal(0, 1e6 / np.sqrt(2), size=(20000, 2))).std(axis=0, ddof=1)
    bound = 1e6 / sv[-1]
    ok2 = np.hypot(*sd) <= bound * 1.02
    print(f"white r_1 noise of norm 1e6: shifts' norm {np.hypot(*sd):.2e} <= worst-case bound sigma/sigma_min {bound:.2e} -> {'ok' if ok2 else 'FAIL'}")
    print("PASS" if err < 1e-9 and ok2 else "FAIL")
    return 0 if err < 1e-9 and ok2 else 1


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest("sign" if "--mutate=sign" in a else None))
    R, names = [], []
    for p in a:
        r = r1_of(p)
        if r is not None:
            R.append(r); names.append(p.replace("\\", "/").split("/")[-1][-30:])
    R = np.array(R)
    S = shifts(R)
    print(f"n = {len(R)}; shifts of the zero implied by each r_1, -J^-1 r_1, (dA, dw/w_inf):")
    for n, s in zip(names, S):
        print(f"  {n:32s} ({s[0]:+.3e}, {s[1]:+.3e})")
    sd, sdn = S.std(axis=0, ddof=1), None
    print(f"std of the shifts (ddof 1): dA {sd[0]:.3e}, dw/w_inf {sd[1]:.3e}; mean shift ({S.mean(axis=0)[0]:+.3e}, {S.mean(axis=0)[1]:+.3e})")
    print(f"std of r_1 per component {R.std(axis=0, ddof=1)[0]:.3e}, {R.std(axis=0, ddof=1)[1]:.3e}; worst-case bound std_norm / sigma_min = {np.hypot(*R.std(axis=0, ddof=1)) / np.linalg.svd(J, compute_uv=False)[-1]:.3e}")
    U, s, Vt = np.linalg.svd(J)
    print(f"principal axes of the r_1 scatter (eigenvalues of the covariance): " + ", ".join(f"{np.sqrt(max(v, 0)):.2e}" for v in np.linalg.eigvalsh(np.cov(R.T))[::-1]))


if __name__ == "__main__":
    main()
