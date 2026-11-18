"""#961 line 5: Delta of a chain step's saved state, its eight parts summed exactly (the last entry of each part), and the
difference of two such states. Usage: delta_cmp961.py A.npz B.npz BOUND   prints Delta(A), Delta(B), |B - A|, and
exits 0 when |B - A| <= BOUND (pass mode), 1 when it is above. --expect-above makes the exits the other way (the control,
which must be above BOUND). `selftest` plants two eight-part values 3e-41 and 3e-39 apart (the first parts equal, so only
the lower parts carry the gap) and needs the bound check to say at-most for 1e-40 / above for the second, and a
two-part sum to miss the gap, as the mutation. Run with a worktree venv python."""
import sys

import mpmath as mp
import numpy as np


def delta_exact(parts):
    """the exact sum of the last entries of all the parts, at 64 x 53 bits"""
    with mp.workprec(64 * 53):
        return mp.fsum(mp.mpf(float(np.asarray(p)[-1])) for p in parts)


def delta_of(path, nparts=8):
    d = np.load(path)
    keys = ["zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7"][:nparts]
    missing = [k for k in keys if k not in d]
    if missing:
        raise SystemExit(f"{path}: no {missing}, not an eight-part state")
    return delta_exact(d[k] for k in keys)


def diff_bound(da, db, bound):
    with mp.workprec(64 * 53):
        return abs(db - da), abs(db - da) <= bound


def selftest():
    mp.mp.prec = 64 * 53
    base = mp.mpf(1) / 3
    def split(x, n=8):
        out = []
        for _ in range(n):
            f = float(x)
            out.append(np.array([0.0, f]))
            x -= mp.mpf(f)
        return out
    a = split(base)
    b1 = split(base + mp.mpf("3e-41"))
    b2 = split(base + mp.mpf("3e-39"))
    da, db1, db2 = delta_exact(a), delta_exact(b1), delta_exact(b2)
    ok = True
    d1, le1 = diff_bound(da, db1, mp.mpf("1e-40"))
    d2, le2 = diff_bound(da, db2, mp.mpf("1e-40"))
    print(f"planted 3e-41: |diff| {mp.nstr(d1, 6)} at most 1e-40: {le1}; planted 3e-39: |diff| {mp.nstr(d2, 6)} at most 1e-40: {le2}")
    ok &= le1 and not le2
    # mutation: two parts only cannot see the 3e-41 gap's lower digits (the sum differs from the exact one)
    two = delta_exact(a[:2]) - da
    print(f"mutation, two parts: error of the sum {mp.nstr(abs(two), 3)} (must be above 1e-40): {abs(two) > mp.mpf('1e-40')}")
    ok &= abs(two) > mp.mpf("1e-40")
    print("selftest", "ok" if ok else "FAILED")
    return 0 if ok else 1


def main(argv):
    if argv and argv[0] == "selftest":
        return selftest()
    above = "--expect-above" in argv
    argv = [a for a in argv if a != "--expect-above"]
    pa, pb, bound = argv[0], argv[1], mp.mpf(argv[2])
    mp.mp.prec = 64 * 53
    da, db = delta_of(pa), delta_of(pb)
    d, le = diff_bound(da, db, bound)
    print(f"Delta(A) {mp.nstr(da, 45)}\nDelta(B) {mp.nstr(db, 45)}\n|B - A| {mp.nstr(d, 8)}, bound {argv[2]}: "
          f"{'at most' if le else 'above'}")
    ok = (not le) if above else le
    print("pass" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
