"""#1078: map a mode_scale.py --small row's unknown indices to hp's unknowns.

    python3 small_map.py modescale_small.jsonl     one table per row
    python3 small_map.py selftest [--mutate=shift]  planted indices through the same map (exit 0 iff every planted index reads as written; shift must exit 1)

Layout (hp/src/model.rs lines 12-17, driver.py's docstring, multishoot 4.1.0 mode.rs: the mode matrix's column cj is the z index, Delta (the global) dropped; all-outward
shooting, match_node = K - 1):  z = [ p1 (M) | c0 (M) | node_0: p m a c (4M) | ... | node_{K-1}: p m a c | m_h (M) | a_h (M) ] ; n = 4M(K+1) = 2M + 4MK + 2M.
Each of the M entries of a field block is the field's value at the half-grid point j (theta_j = 2 pi j / N = pi j / M, N = 2M, odd fields folded), NOT a harmonic: a harmonic is a
linear combination of the M entries. Node a (x = nodes[a]) is the target of segment a (node a-1 -> a; for a = 0 the centre-series block) and the source of segment a+1; the last
node is also the target of the horizon block. The pivot k of a row-interchange LU (scipy lu_factor) belongs to column k."""
import json
import math
import sys

NODES = [0.000157, 0.000313, 0.000625, 0.00125, 0.0025, 0.005, 0.01, 0.02, 0.05, 0.1, 0.16, 0.23, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.975]
FIELDS = "pmac"
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)


def where(i, M, K):
    i = i + (1 if MUT == "shift" else 0)
    assert 0 <= i < 4 * M * (K + 1), i
    if i < M:
        return ("centre data p1", None, i)
    if i < 2 * M:
        return ("centre data c0", None, i - M)
    if i < 2 * M + 4 * M * K:
        a, r = divmod(i - 2 * M, 4 * M)
        return (f"node {a}", FIELDS[r // M], r % M)
    r = i - (2 * M + 4 * M * K)
    return ("horizon data m_h" if r < M else "horizon data a_h", None, r % M)


def describe(i, M=96, nodes=NODES):
    K = len(nodes)
    blk, f, j = where(i, M, K)
    th = math.pi * j / M
    if blk.startswith("node"):
        a = int(blk.split()[1])
        seg = f"target of segment {a}" if a > 0 else "target of the centre-series block"
        seg += f", source of segment {a + 1}" if a + 1 < K else ", also the horizon block's target"
        return f"unknown {i}: {blk} (x = {nodes[a]}), field {f}, grid point j = {j} of {M} (theta = {th:.4f}); {seg}"
    return f"unknown {i}: {blk}, grid point j = {j} of {M} (theta = {th:.4f})"


def selftest():
    M, K = 96, 21
    n = 4 * M * (K + 1)
    cases = {0: ("centre data p1", None, 0), 95: ("centre data p1", None, 95), 96: ("centre data c0", None, 0), 191: ("centre data c0", None, 95),
             192: ("node 0", "p", 0), 192 + 96: ("node 0", "m", 0), 192 + 2 * 96 + 5: ("node 0", "a", 5), 192 + 3 * 96 + 95: ("node 0", "c", 95),
             192 + 384 * 3 + 96 * 2 + 5: ("node 3", "a", 5), 192 + 384 * 20 + 3 * 96 + 7: ("node 20", "c", 7),
             8256: ("horizon data m_h", None, 0), 8351: ("horizon data m_h", None, 95), 8352: ("horizon data a_h", None, 0), n - 1: ("horizon data a_h", None, 95)}
    def safe(i):
        try:
            return where(i, M, K)
        except AssertionError:
            return None
    bad = [i for i, w in cases.items() if safe(i) != w]
    ok = not bad and n == 8448 and 2 * M + 4 * M * K + 2 * M == n
    print(f"selftest{' --mutate=shift' if MUT else ''}: {'PASS' if ok else 'FAIL'} ({len(cases)} planted indices, n = {n}; wrong: {bad})")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest())
    for line in open(sys.argv[1]):
        r = json.loads(line)
        print(f"lambda {r['lam']}, n {r['n']}, M {r['M']}, scaled pivot range {r['pmin']:.3e} .. {r['pmax']:.3e}; the ten smallest scaled float64 pivots:")
        for rank, (i, v) in enumerate(r["small"], 1):
            print(f"  {rank:2d}. pivot {v:+.3e}  {describe(i, r['M'])}")
