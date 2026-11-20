"""macm3b #1008: compare an eight-part state (NEW) with a reference state (REF): D from meta D_str, Delta (the last entry of z) and every
entry as the exact sum of its eight parts (zh, zl, z2..z7), plus each part's own difference. Usage: ab_compare.py REF NEW [tol]
Exit 0 when |dD| <= tol and |dDelta| <= tol (tol default 1e-30), else 1."""
import sys, json, numpy as np
import mpmath as mp
mp.mp.dps = 80
ref, new = sys.argv[1], sys.argv[2]
tol = mp.mpf(sys.argv[3]) if len(sys.argv) > 3 else mp.mpf("1e-30")
K = ["zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7"]
def load(p):
    z = np.load(p, allow_pickle=True)
    meta = json.loads(str(z["meta"]))
    return mp.mpf(meta["D_str"]), [z[k] for k in K], meta
Dr, Pr, mr = load(ref); Dn, Pn, mn = load(new)
n = len(Pr[0]); assert len(Pn[0]) == n
sumr = [mp.fsum(mp.mpf(float(p[i])) for p in Pr) for i in range(n)]
sumn = [mp.fsum(mp.mpf(float(p[i])) for p in Pn) for i in range(n)]
d = [abs(a - b) for a, b in zip(sumn, sumr)]
imax = max(range(n), key=lambda i: d[i])
dD = abs(Dn - Dr); dDl = d[-1]
print(f"D ref {mp.nstr(Dr, 34)}, new {mp.nstr(Dn, 34)}, |dD| {mp.nstr(dD, 4)}")
print(f"Delta ref {mp.nstr(sumr[-1], 40)}, new {mp.nstr(sumn[-1], 40)}, |dDelta| {mp.nstr(dDl, 4)}")
print("Delta's eight parts, new - ref: " + ", ".join(f"{k} {float(Pn[j][-1]) - float(Pr[j][-1]):.3e}" for j, k in enumerate(K)))
print(f"all {n} entries (each its eight parts' exact sum): max |dz| {mp.nstr(d[imax], 4)} at index {imax}; the {sum(1 for x in d if x > tol)} entries above {mp.nstr(tol, 2)}; ")
print("each part's own max difference over the entries: " + ", ".join(f"{k} {max(abs(float(Pn[j][i]) - float(Pr[j][i])) for i in range(n)):.3e}" for j, k in enumerate(K)))
ok = dD <= tol and dDl <= tol
print(f"criterion 2 (|dD| <= {mp.nstr(tol, 2)} and |dDelta| <= {mp.nstr(tol, 2)}): {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
