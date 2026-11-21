"""#1008 macm3b series check: bitwise comparison of two arcjet_*.npz (keys z0..z7, each (N+1, L), order k in row k; meta json).
Usage: compare_arcjet.py A.npz B.npz [OUT.txt]. Prints EQUAL or NOT EQUAL; if not, per order k the largest part-wise relative
difference |a-b|/|a| over the elements of each part (parts q = 0..7 of the octo-double expansion, element-wise, differing elements only),
the part and number of elements that differ, and the relative difference of the full value (the 8 parts summed at 90 digits),
element-wise maximum over the order. Exit 0 if equal, 1 if not, 2 on a structure mismatch."""
import sys, json
import numpy as np
import mpmath as mp
mp.mp.dps = 90
a_path, b_path = sys.argv[1], sys.argv[2]
out = open(sys.argv[3], "w") if len(sys.argv) > 3 else None
def P(*s):
    t = " ".join(str(x) for x in s)
    print(t)
    if out: out.write(t + "\n")
A, B = np.load(a_path, allow_pickle=False), np.load(b_path, allow_pickle=False)
P(f"A {a_path}\nB {b_path}")
if sorted(A.files) != sorted(B.files):
    P(f"STRUCTURE MISMATCH: keys {sorted(A.files)} vs {sorted(B.files)}"); sys.exit(2)
ma, mb = json.loads(str(A["meta"])), json.loads(str(B["meta"]))
meta_eq = {k: (ma[k] == mb[k]) for k in sorted(set(ma) & set(mb))}
only_a, only_b = {k: ma[k] for k in sorted(set(ma) - set(mb))}, {k: mb[k] for k in sorted(set(mb) - set(ma))}
P("meta fields in both files, equal (exact):", ", ".join(f"{k} {v}" for k, v in meta_eq.items()))
P(f"meta keys only in A: {only_a or 'none'}; only in B: {only_b or 'none'} (not compared; the code that wrote the newer file adds keys)")
Z = {}
for q in range(8):
    za, zb = np.ascontiguousarray(A[f"z{q}"]), np.ascontiguousarray(B[f"z{q}"])
    if za.shape != zb.shape or za.dtype != zb.dtype:
        P(f"STRUCTURE MISMATCH: z{q} {za.shape} {za.dtype} vs {zb.shape} {zb.dtype}"); sys.exit(2)
    Z[q] = (za, zb)
N1, L = Z[0][0].shape
bit_ne = {q: (Z[q][0].view(np.uint64) != Z[q][1].view(np.uint64)) for q in range(8)}
nd = {q: int(bit_ne[q].sum()) for q in range(8)}
P(f"shape per part ({N1}, {L}); elements that differ bitwise per part: " + ", ".join(f"z{q} {nd[q]}" for q in range(8)) + f" of {N1 * L} each")
equal = all(v == 0 for v in nd.values()) and all(meta_eq.values())
if equal:
    P("EQUAL: every part of every order is bit-identical, and the meta fields present in both files (" + ", ".join(meta_eq) + ") are identical.")
    sys.exit(0)
P("NOT EQUAL.")
P("\n| order k | parts that differ | elements that differ (of all parts) | largest part-wise relative difference \\|a-b\\|/\\|a\\| | at part | full-value relative difference, element-wise max | full-value relative difference, norm-wise (max-norm) |\n|---|---|---|---|---|---|---|")
overall = (0.0, None, None)
for k in range(N1):
    best = (0.0, None); nel = 0; parts = []
    for q in range(8):
        m = bit_ne[q][k]
        if m.any():
            parts.append(q); nel += int(m.sum())
            a, b = Z[q][0][k][m], Z[q][1][k][m]
            with np.errstate(divide="ignore", invalid="ignore"):
                r = np.where(a != 0, np.abs(a - b) / np.abs(a), np.inf)
            rm = float(np.max(r))
            if rm > best[0]: best = (rm, q)
    if not parts:
        continue
    rel_el, na, nb = 0.0, mp.mpf(0), mp.mpf(0)
    idx = sorted({int(i) for q in parts for i in np.nonzero(bit_ne[q][k])[0]})
    for i in idx:
        va = mp.fsum(mp.mpf(float(Z[q][0][k][i])) for q in range(8)); vb = mp.fsum(mp.mpf(float(Z[q][1][k][i])) for q in range(8))
        if va != 0: rel_el = max(rel_el, float(abs(va - vb) / abs(va)))
        na = max(na, abs(va - vb))
    nbm = max(abs(mp.fsum(mp.mpf(float(Z[q][0][k][i])) for q in range(8))) for i in range(L))
    rel_norm = float(na / nbm) if nbm != 0 else float("inf")
    P(f"| {k} | {','.join(map(str, parts))} | {nel} | {best[0]:.3e} | {best[1]} | {rel_el:.3e} | {rel_norm:.3e} |")
    if best[0] > overall[0]: overall = (best[0], k, best[1])
P(f"\nlargest part-wise relative difference over all orders: {overall[0]:.3e} at order {overall[1]}, part {overall[2]}; orders that differ: " + str(sum(1 for k in range(N1) if any(bit_ne[q][k].any() for q in range(8)))) + f" of {N1}")
sys.exit(1)
