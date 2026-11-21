"""#1025, the coordinator's sign-convention check, information beside it: which of the state's quantities change sign between
consecutive k_c 63 states. Per block of the state (dss_ell.layout: centre odd, centre even; per node p, m (odd), a, c (even),
psi (odd); the end's odd, even, odd; Delta last), the cosine between the two states and the share of entries whose sign
differs (entries above 1e-8 of the block's largest in both). A block read as flipped has cosine below -0.9.
usage: d18_state_signs.py STATE.npy,STATE.npy,...   (in D order; D and k_c 63 from the file names)"""
import sys, os, re, numpy as np
WTM = os.environ.get("P4_WT_MATTER", "/Users/nathan/Source/choptuik-1025/solver/matter")
sys.path.insert(0, WTM); os.chdir(WTM)
from dss_ell import DSSEll, NODES_STD
fs = sys.argv[1].split(",")
Z = [np.load(f) for f in fs]
Ds = [float(re.search(r"_D([0-9.]+?)0*\.npy$", os.path.basename(f)).group(1)) for f in fs]
S = DSSEll(kc=63, nodes=NODES_STD, n=Ds[0] - 2, ell=1, Delta_ref=Z[0][-1], Ks=30, u0=0.04)
sizes, K, L = S.layout()
assert all(len(z) == L for z in Z), "state length is not the k_c 63 layout's"
names = ["centre odd", "centre even"] + [f"node{i} {q}" for i in range(K) for q in ("p", "m", "a", "c", "psi")] + ["end odd", "end even", "end odd2"]
pars = S.parities()
cut = np.cumsum([0] + sizes)
groups = {"odd-parity blocks": [], "even-parity blocks": []}
for i, p in enumerate(pars):
    groups["odd-parity blocks" if p == "odd" else "even-parity blocks"].append(i)
print(f"k_c 63 layout: {len(sizes)} blocks, n_odd {sizes[0]}, n_even {sizes[1]}, length {L} (Delta last)")
print(f"phase entry (centre odd, index {len(S.kodd)}): " + ", ".join(f"D {D:g} {z[len(S.kodd)]:+.3e}" for D, z in zip(Ds, Z)))
print("Delta: " + ", ".join(f"D {D:g} {z[-1]:.10f}" for D, z in zip(Ds, Z)))
def cmp(a, b):
    m = (np.abs(a) > 1e-8 * np.abs(a).max()) & (np.abs(b) > 1e-8 * np.abs(b).max())
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b))), float(np.mean(np.sign(a[m]) != np.sign(b[m]))) if m.any() else float("nan")
for (Da, a), (Db, b) in zip(zip(Ds, Z), zip(Ds[1:], Z[1:])):
    per = [(names[i],) + cmp(a[cut[i]:cut[i + 1]], b[cut[i]:cut[i + 1]]) for i in range(len(sizes))]
    flipped = [n for n, c, _ in per if c < -0.9]
    g = {k: cmp(np.concatenate([a[cut[i]:cut[i + 1]] for i in ix]), np.concatenate([b[cut[i]:cut[i + 1]] for i in ix])) for k, ix in groups.items()}
    worst = min(per, key=lambda t: t[1])
    print(f"D {Da:g} -> {Db:g}: " + "; ".join(f"{k} cosine {c:+.6f}, sign differs {s:.3f}" for k, (c, s) in g.items())
          + f"; least block cosine {worst[1]:+.6f} ({worst[0]}); blocks flipped: {flipped or 'none'}")
