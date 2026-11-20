"""#1025 P1-prime-d (p1d_criteria.log): hybrid sign scan, and the hybrid root if it shows one robust change, on a re-solved state.
usage (venv-1025dd): p1d_scan.py RECORDS.jsonl STATE.npy D lam1,lam2,..."""
import sys, os, json, time, numpy as np
from scipy.optimize import brentq
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
os.chdir("/Users/nathan/Source/choptuik-1025/solver/matter")
from dss_ell import DSSEll, NODES_STD
import multidouble as md
import ell_ddm
recf, st, D = sys.argv[1], sys.argv[2], float(sys.argv[3]); lams = [float(v) for v in sys.argv[4].split(",")]
rec = [json.loads(l) for l in open(recf) if json.loads(l).get("D") == D][-1]
kc = rec["kc"]; z = np.load(st)
S = DSSEll(kc=kc, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk", 1))
steps = S.freeze_from(z, rec["kappa"])
with np.errstate(all="ignore"):
    F = float(np.linalg.norm(S.residual(z[None, :])[0]))
same = abs(F - rec["F"]) <= max(1e-2 * rec["F"], 1e-13) and sum(steps.values()) == rec["steps"]
print(f"D {D} k_c {kc} u0 {rec['u0']} ({os.path.basename(st)}): |F| {F:.10e} (record {rec['F']:.10e}), steps {sum(steps.values())} "
      f"(record {rec['steps']}): {'the record system' if same else 'NOT the record system: stop'}", flush=True)
if not same:
    sys.exit(3)
E = ell_ddm.DDEll(S)
blocks, offs = S._block_list(); blk = 3 * S.n_odd + 2 * S.n_even
c0, nf, fun, tgt = blocks[12]; r0 = 12 * blk; sl = (slice(r0, r0 + blk), slice(c0, c0 + nf))
mask = np.zeros((S.layout()[2] - 1,) * 2, bool)
for b, (cc, nn, ff, tt) in enumerate(blocks[:12]):
    mask[b * blk:(b + 1) * blk, cc:cc + nn] = True
ev = {}


def hyb(l):
    if l in ev:
        return ev[l]["sign"], ev[l]["ln"]
    with np.errstate(all="ignore"):
        Mf = S.mode_matrix(z, l)
    sf, lf = md.dd_logdet(Mf, np.zeros_like(Mf), True)[:2]
    Md = E.mode_matrix(z, l, only=[12])
    H, Hl = Mf.copy(), np.zeros_like(Mf); H[sl] = Md.h[sl]; Hl[sl] = Md.l[sl]
    s, ld = md.dd_logdet(H, Hl, True)[:2]
    nz = [md.dd_logdet(H + 1e-15 * np.random.default_rng(100 + k).standard_normal(H.shape) * mask * H, Hl, True)[0] for k in range(2)]
    ev[l] = dict(sign=float(s), ln=float(ld), noise=nz, f64=[float(sf), float(lf)])
    print(f"  lam {l:.12f}: hybrid {s:+.0f} ln|det| {ld:.10f} (noise 1e-15 on blocks 0-11: {nz}); float64 {sf:+.0f} {lf:.10f}", flush=True)
    return float(s), float(ld)


t0 = time.time()
sg = [hyb(l)[0] for l in lams]
ch = [i for i in range(len(lams) - 1) if sg[i] != sg[i + 1]]
robust = all(all(x == ev[l]["sign"] for x in ev[l]["noise"]) for l in lams)
print(f"scan: hybrid signs {['+' if s > 0 else '-' for s in sg]}, changes {len(ch)}, noise-robust {robust}", flush=True)
root, br = None, None
if len(ch) == 1 and robust:
    i = ch[0]
    ref = 0.5 * (hyb(lams[i])[1] + hyb(lams[i + 1])[1])
    root = brentq(lambda l: hyb(l)[0] * np.exp(hyb(l)[1] - ref), lams[i], lams[i + 1], xtol=2e-8 * lams[i], rtol=1e-12)
    ls = sorted(ev); ss = [ev[l]["sign"] for l in ls]
    cc = [(ls[j], ls[j + 1]) for j in range(len(ls) - 1) if ss[j] != ss[j + 1]]
    br = min(cc, key=lambda p: abs(0.5 * (p[0] + p[1]) - root))
    robust = all(all(x == e["sign"] for x in e["noise"]) for e in ev.values())
    print(f"root: hybrid lam {root!r}, final bracket {br} (width {br[1] - br[0]:.2e}), changes over all {len(ev)} evaluations "
          f"{len(cc)}, noise-robust {robust}", flush=True)
else:
    print("stop: not exactly one noise-robust change; no root search (p1d_criteria.log)", flush=True)
out = dict(D=D, kc=kc, u0=rec["u0"], state=os.path.basename(st), F=F, record_system=same, scan=lams, scan_signs=sg, scan_changes=len(ch),
           lam=root, bracket=br, bracket_width=(br[1] - br[0]) if br else None, noise_robust=robust, n_eval=len(ev), evals=ev,
           sec=round(time.time() - t0))
open("data/ell_p1d_1025.jsonl", "a").write(json.dumps(out) + "\n")
