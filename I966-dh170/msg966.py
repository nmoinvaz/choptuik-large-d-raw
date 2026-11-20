#!/usr/bin/env python3
"""#966 (dh170): the numbers of one near_null JSON in the form of the #949 relay's post (relay_dh370_949.py's picks and message, copied: that file runs its loop on import).

    msg966.py NAME.json            prints the numbers (sigma_Delta, sigma_2, Delta share, convergence, the pinned step's Delta component with its sign)
    msg966.py --selftest [--mutate|--mutate=sign]    a planted record gives the planted numbers (exit 1 if not; --mutate swaps sigma_Delta and sigma_2,
                                                     --mutate=sign flips the pinned Delta's sign: both must fail)
sigma_Delta = the vector with the largest Delta share; the pair = vectors whose top harmonic-3 components are p1 and m_h; sigma_2 = the smallest sigma of the rest."""
import json
import sys


def picks(rec, mutate=False):
    v = rec["vectors"]
    d = max(range(len(v)), key=lambda i: v[i]["delta"])
    pair = [i for i in range(len(v)) if i != d and {("p1", 3), ("m_h", 3)} <= {(b, k) for b, k, _ in v[i]["top"]}]
    rest = sorted((i for i in range(len(v)) if i != d and i not in pair), key=lambda i: v[i]["sigma"])
    s2 = rest[0]
    if mutate and mutate != "sign":
        d, s2 = s2, d
    return d, s2


def numbers(rec, mutate=False):
    d, s2 = picks(rec, mutate)
    v = rec["vectors"]
    return (f"sigma_Delta {v[d]['sigma']:.6e} (vector {d + 1}, Delta share {v[d]['delta']:.3f}, convergence {v[d]['conv']:.0e}), "
            f"sigma_2 {v[s2]['sigma']:.6e} (vector {s2 + 1}, Delta share {v[s2]['delta']:.3f}, convergence {v[s2]['conv']:.0e}), "
            f"sigma_2/sigma_Delta {v[s2]['sigma'] / v[d]['sigma']:.3f}; pinned step dz + J^-1 c, its Delta component (the first-order error of Delta, with its sign): "
            f"{rec['step_pinned']['delta'] * (-1 if mutate == 'sign' else 1):+.3e}")


def selftest(mutate):
    rec = dict(D=251.5, vectors=[
        dict(sigma=2.5e-18, delta=0.74, conv=1e-6, top=[["p1", 1, 0.1]]), dict(sigma=3.0e-18, delta=0.25, conv=2e-6, top=[["p1", 1, 0.1]]),
        dict(sigma=7e-13, delta=0.0, conv=1e-9, top=[["p1", 3, 0.1], ["m_h", 3, 0.1]]), dict(sigma=8e-13, delta=0.0, conv=1e-9, top=[["p1", 3, 0.1], ["m_h", 3, 0.1]]),
        dict(sigma=1e-10, delta=0.0, conv=0.3, top=[["c0", 4, 0.1]]), dict(sigma=2e-10, delta=0.0, conv=0.3, top=[["c0", 4, 0.1]])],
        step_pinned=dict(delta=-4.2e-27))
    m = numbers(rec, mutate)
    ok = ("sigma_Delta 2.500000e-18 (vector 1" in m and "sigma_2 3.000000e-18 (vector 2" in m and "sigma_2/sigma_Delta 1.200" in m and "with its sign): -4.200e-27" in m)
    print("selftest" + (f" --mutate={mutate}" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        mut = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), True if "--mutate" in sys.argv else False)
        sys.exit(0 if selftest(mut) else 1)
    rec = json.load(open(sys.argv[1]))
    print(f"D {rec['D']:.4f}, state {rec['state']}: " + numbers(rec))
