"""#1025 D 18: the hybrid M's det sign (float64 blocks 0-11, dd block 12; p4_hybrid.py's sd(), unchanged) at given lambda on a
stub record's state and discrete system, with p4_hybrid's 1e-15 noise test on blocks 0-11 (2 seeds) and the plain float64 sign beside it.
usage (venv-1025dd): d18_hybsign.py STUB.jsonl STATE.npy D LAMS OUT.jsonl   (LAMS comma-separated)"""
import sys, os, json, time, numpy as np
WTM = os.environ.get("P4_WT_MATTER", "/Users/nathan/Source/choptuik-1025/solver/matter")
sys.path.insert(0, WTM)
os.chdir(WTM)
from dss_ell import DSSEll, NODES_STD
import multidouble as md
import ell_ddm
recf, st, D, lams, outf = sys.argv[1], sys.argv[2], float(sys.argv[3]), [float(v) for v in sys.argv[4].split(",")], sys.argv[5]
rec = [json.loads(l) for l in open(recf) if json.loads(l).get("D") == D][-1]
z = np.load(st)
S = DSSEll(kc=rec["kc"], nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk", 1))
steps = S.freeze_from(z, rec["kappa"])
with np.errstate(all="ignore"):
    F = float(np.linalg.norm(S.residual(z[None, :])[0]))
same = abs(F - rec["F"]) <= max(1e-2 * rec["F"], 1e-13) and sum(steps.values()) == rec["steps"]
print(f"D {D} k_c {rec['kc']}: |F| {F:.10e} (record {rec['F']:.10e}), steps {sum(steps.values())} (record {rec['steps']}): "
      f"{'the record system' if same else 'NOT the record system'}", flush=True)
if not same:
    sys.exit(3)
E = ell_ddm.DDEll(S)
blocks, offs = S._block_list(); blk = 3 * S.n_odd + 2 * S.n_even
c0, nf, fun, tgt = blocks[12]; r0 = 12 * blk; sl = (slice(r0, r0 + blk), slice(c0, c0 + nf))
mask = np.zeros((S.layout()[2] - 1,) * 2, bool)
for b, (cc, nn, ff, tt) in enumerate(blocks[:12]):
    mask[b * blk:(b + 1) * blk, cc:cc + nn] = True
for l in lams:
    t0 = time.time()
    with np.errstate(all="ignore"):
        Mf = S.mode_matrix(z, l)
    sf, lf = np.linalg.slogdet(Mf)
    H, Hl = Mf.copy(), np.zeros_like(Mf)
    Md = E.mode_matrix(z, l, only=[12])
    H[sl] = Md.h[sl]; Hl[sl] = Md.l[sl]
    s, ld = md.dd_logdet(H, Hl, True)[:2]
    nz = [md.dd_logdet(H + 1e-15 * np.random.default_rng(100 + k).standard_normal(H.shape) * mask * H, Hl, True)[0] for k in range(2)]
    r = dict(D=D, kc=rec["kc"], lam=l, sign=float(s), ln=float(ld), noise=[float(x) for x in nz], noise_robust=all(x == s for x in nz),
             f64_sign=float(sf), f64_ln=float(lf), state=os.path.basename(st), sec=round(time.time() - t0))
    print(f"  lam {l!r}: hybrid {s:+.0f} ln|det| {ld:.10f} (noise 1e-15 on blocks 0-11: {r['noise']}); float64 {sf:+.0f} {lf:.10f} "
          f"({r['sec']} s)", flush=True)
    open(outf, "a").write(json.dumps(r) + "\n")
