"""#1078: the smallest pivots of jac_diag.py's row by block, as small_count.py does for the mode matrix (the Jacobian has one more unknown, Delta, index 4M(K+1)).

    python3 jac_count.py jac_diag.jsonl      |      python3 jac_count.py selftest [--mutate=delta]"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import small_map as SM  # noqa: E402

MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)


def block(i, M, K):
    if i == 4 * M * (K + 1) + (1 if MUT == "delta" else 0):
        return "Delta"
    blk, f, j = SM.where(i, M, K)
    return blk + (f"/{f}" if f else "")


def counts(small, M, K):
    out = {}
    for t in (1e-15, 1e-12, 1e-9):
        sel = [(i, v) for i, v in small if abs(v) < t]
        out[t] = (len(sel), Counter(block(i, M, K) for i, _ in sel))
    return out


def selftest():
    M, K = 96, 21
    n = 4 * M * (K + 1)
    small = [[n, 3e-19], [8352 + 4, 5e-17], [8256, 2e-12], [192, 4e-8]]
    try:
        c = counts(small, M, K)
    except AssertionError:
        print("selftest --mutate=delta: FAIL (the shifted Delta index fell outside the layout)")
        return 1
    ok = c[1e-15][0] == 2 and c[1e-15][1] == Counter({"Delta": 1, "horizon data a_h": 1}) and c[1e-12][0] == 2 and c[1e-9][0] == 3
    print(f"selftest{' --mutate=delta' if MUT else ''}: {'PASS' if ok else 'FAIL'} (counts {[c[t][0] for t in c]}, below 1e-15 by block {dict(c[1e-15][1])})")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest())
    for line in open(sys.argv[1]):
        r = json.loads(line)
        M, K = r["M"], r["n"] // (4 * r["M"]) - 1
        c = counts(r["small"], M, K) if r["n"] == 4 * M * (K + 1) + 1 else None
        print(f"{r['state']}: n {r['n']} (K = {K}); |F| {r['F']:.2e}; Newton step |dz| {r['dz']:.2e}, dDelta {r['dDelta']:+.2e}, dd LU pivots {r['newton_pmin']:.3e} .. {r['newton_pmax']:.3e}; "
              f"scaled float64 pivots {r['pmin']:.3e} .. {r['pmax']:.3e}; the {len(r['small'])} smallest span {abs(r['small'][0][1]):.3e} .. {abs(r['small'][-1][1]):.3e}")
        sel = Counter(block(i, M, K) for i, _ in r["small"])
        print(f"  the {len(r['small'])} smallest by block: {dict(sel.most_common(8))}")
        for t in (1e-15, 1e-12, 1e-9):
            print(f"  below {t:g}: {c[t][0]}; by block {dict(c[t][1])}")
