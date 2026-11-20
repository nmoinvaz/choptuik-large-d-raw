"""#1025 P4 control 2 (p4_criteria.log): the hybrid and float64 det signs at the five lambda of c1_scan.log on Fb, k_c 55, D 16."""
import sys, os, json, time, numpy as np
WTM = os.environ.get("P4_WT_MATTER", "/Users/nathan/Source/choptuik-1025/solver/matter")
sys.path.insert(0, WTM); os.chdir(WTM)
from dss_ell import DSSEll, NODES_STD
import multidouble as md
import ell_ddm
O = "/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac/out/"
rec = [json.loads(l) for l in open(O + "l1kc55Fb1025.jsonl") if json.loads(l).get("D") == 16.0 and json.loads(l).get("lam")][-1]
z = np.load(O + "sol_l1kc55Fb1025_D16.0000.npy")
S = DSSEll(kc=55, nodes=NODES_STD, n=14.0, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk", 1))
steps = S.freeze_from(z, rec["kappa"])
with np.errstate(all="ignore"):
    F = float(np.linalg.norm(S.residual(z[None, :])[0]))
same = abs(F - rec["F"]) <= max(1e-2 * rec["F"], 1e-13) and sum(steps.values()) == rec["steps"]
print(f"system: |F| {F:.10e} (record {rec['F']:.10e}), steps {sum(steps.values())} (record {rec['steps']}): {same}", flush=True)
if not same:
    sys.exit(3)
E = ell_ddm.DDEll(S)
blocks, offs = S._block_list(); blk = 3 * S.n_odd + 2 * S.n_even
c0, nf, fun, tgt = blocks[12]; r0 = 12 * blk; sl = (slice(r0, r0 + blk), slice(c0, c0 + nf))
mask = np.zeros((S.layout()[2] - 1,) * 2, bool)
for b, (cc, nn, ff, tt) in enumerate(blocks[:12]):
    mask[b * blk:(b + 1) * blk, cc:cc + nn] = True
rows = []
for l in (2.24250, 2.24254, 2.24258, 2.24262, 2.24266):
    t0 = time.time()
    with np.errstate(all="ignore"):
        Mf = S.mode_matrix(z, l)
    sf, lf = md.dd_logdet(Mf, np.zeros_like(Mf), True)[:2]
    Md = E.mode_matrix(z, l, only=[12])
    H, Hl = Mf.copy(), np.zeros_like(Mf); H[sl] = Md.h[sl]; Hl[sl] = Md.l[sl]
    s, ld = md.dd_logdet(H, Hl, True)[:2]
    nz = [md.dd_logdet(H + 1e-15 * np.random.default_rng(100 + k).standard_normal(H.shape) * mask * H, Hl, True)[0] for k in range(2)]
    rows.append(dict(lam=l, hybrid=[float(s), float(ld)], noise=nz, f64=[float(sf), float(lf)], sec=round(time.time() - t0)))
    print(f"lam {l:.5f}: hybrid {s:+.0f} ln|det| {ld:.10f} (noise {nz}); float64 {sf:+.0f} {lf:.10f} ({rows[-1]['sec']} s)", flush=True)
hs = [r["hybrid"][0] for r in rows]
ok = len(set(hs)) == 1 and all(all(x == r["hybrid"][0] for x in r["noise"]) for r in rows)
print(f"control 2: hybrid signs {['+' if v > 0 else '-' for v in hs]}, float64 {['+' if r['f64'][0] > 0 else '-' for r in rows]} -> "
      f"{'PASS' if ok else 'FAIL'}", flush=True)
open(os.path.join(WTM, "data", "ell_p4_ctrl2_1025.jsonl"), "a").write(json.dumps(dict(D=16.0, kc=55, F=F, rows=rows, verdict="PASS" if ok else "FAIL")) + "\n")
sys.exit(0 if ok else 1)
