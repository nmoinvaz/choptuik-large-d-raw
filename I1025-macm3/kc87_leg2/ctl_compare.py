#!/usr/bin/env python3
"""ctl_compare.py [D1 D2 ...] [--a=DIR] [--ctl=DIR]: compares the control leap's states (h 0.03125, tag l1kc87Lmacm3ctl, kc87_leg2/ctl/) with part a's (h 0.0625, tag l1kc87Lmacm3, kc87_leg2/) at the common D
(default 21.3125 and 21.375): Delta, |F|, steps, psi-constraint (records) and the distance of the state vectors (L2, relative to |z_a|, L2 without the last component Delta, the largest component difference and its index).
Prints a markdown table; read-only. ctl_compare.py selftest [--mutate=l1]: planted vectors with a known L2 distance (the mutation uses the L1 distance and must fail)."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)

def dist(za, zb):
    d = zb - za
    return float(np.sum(np.abs(d)) if MUT == "l1" else np.linalg.norm(d))

def selftest():
    za = np.array([0.0, 0.0, 0.0, 1.0]); zb = np.array([3.0, 4.0, 0.0, 1.0])
    ok = abs(dist(za, zb) - 5.0) < 1e-12 and abs(dist(za[:-1], zb[:-1]) - 5.0) < 1e-12
    print("planted: |(3,4,0,0)| = 5 as the L2 distance: %s" % ("PASS" if ok else "FAIL"))
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

def rec(path, D):
    return [json.loads(l) for l in open(path) if l.strip() and abs(json.loads(l)["D"] - D) < 1e-9][-1]

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args and args[0] == "selftest": sys.exit(selftest())
    opt = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--") and "=" in a}
    A = opt.get("--a", HERE); C = opt.get("--ctl", HERE + "/ctl")
    Ds = [float(x) for x in args] or [21.3125, 21.375]
    print("| D | quantity | part a (h 0.0625) | control (h 0.03125) | control - part a |\n|---|---|---|---|---|")
    for D in Ds:
        ra, rc = rec(A + "/l1kc87Lmacm3.jsonl", D), rec(C + "/l1kc87Lmacm3ctl.jsonl", D)
        za = np.load("%s/sol_l1kc87Lmacm3_D%.6f.npy" % (A, D)); zc = np.load("%s/sol_l1kc87Lmacm3ctl_D%.6f.npy" % (C, D))
        assert za.shape == zc.shape, "state shapes differ"
        for name, k, f in (("Delta", "Delta", "%.12f"), ("\\|F\\|", "F", "%.4e"), ("steps", "steps", "%d"), ("psi-constraint", "constraint", "%.4e"), ("seconds", "seconds", "%d")):
            va, vc = ra[k], rc[k]
            print("| %r | %s | %s | %s | %s |" % (D, name, f % va, f % vc, ("%+.3e" % (vc - va)) if k in ("Delta", "F", "constraint") else "%+d" % (vc - va)))
        d = zc - za
        i = int(np.argmax(np.abs(d)))
        print("| %r | L2 distance of the states | | | %.4e (relative to \\|z_a\\| %.3e; without Delta %.4e; the largest component %.3e at index %d of %d) |" % (
            D, dist(za, zc), dist(za, zc) / float(np.linalg.norm(za)), dist(za[:-1], zc[:-1]), abs(d[i]), i, len(za)))

if __name__ == "__main__":
    main()
