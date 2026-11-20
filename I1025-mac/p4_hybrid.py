"""#1025 P4: re-root a lambda record with the hybrid M (float64 blocks 0-11, dd block 12) on its own state and discrete system
(p4_criteria.log). usage (venv-1025dd): p4_hybrid.py RECORDS.jsonl STATE.npy D [--mutate=f64]
--mutate=f64: the same search on the plain float64 M (the hybrid's control).
--quoted: the record is a stub from a report (no record file on raw): its F is checked to 1%, its steps only if given."""
import sys, os, json, time, numpy as np
from scipy.optimize import brentq
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
os.chdir("/Users/nathan/Source/choptuik-1025/solver/matter")
from dss_ell import DSSEll, NODES_STD
import multidouble as md
import ell_ddm
recf, st, D = sys.argv[1], sys.argv[2], float(sys.argv[3]); f64 = "--mutate=f64" in sys.argv; quoted = "--quoted" in sys.argv
rec = [json.loads(l) for l in open(recf) if json.loads(l).get("D") == D and json.loads(l).get("lam")][-1]
kc, guess = rec["kc"], rec["lam_guess"]
z = np.load(st)
S = DSSEll(kc=kc, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk", 1))
steps = S.freeze_from(z, rec["kappa"])
with np.errstate(all="ignore"):
    F = float(np.linalg.norm(S.residual(z[None, :])[0]))
if quoted:   # a record known only from a report: F quoted to 3 digits (1%), steps not printed on raw (not checked)
    same = abs(F - rec["F"]) <= 1e-2 * rec["F"] and (rec.get("steps") is None or sum(steps.values()) == rec["steps"])
else:
    same = abs(F - rec["F"]) <= 1e-6 * rec["F"] and sum(steps.values()) == rec["steps"]
print(f"D {D} k_c {kc} ({os.path.basename(st)}): |F| {F:.10e} (record {rec['F']:.10e}), steps {sum(steps.values())} (record "
      f"{rec['steps']}): {'the record system' if same else 'NOT the record system'}", flush=True)
E = ell_ddm.DDEll(S)
blocks, offs = S._block_list(); blk = 3 * S.n_odd + 2 * S.n_even
c0, nf, fun, tgt = blocks[12]; r0 = 12 * blk; sl = (slice(r0, r0 + blk), slice(c0, c0 + nf))
mask = np.zeros((S.layout()[2] - 1,) * 2, bool)
for b, (cc, nn, ff, tt) in enumerate(blocks[:12]):
    mask[b * blk:(b + 1) * blk, cc:cc + nn] = True
ev = {}


def sd(l):
    if l in ev:
        return ev[l]["sign"], ev[l]["ln"]
    with np.errstate(all="ignore"):
        Mf = S.mode_matrix(z, l)
    H, Hl = Mf.copy(), np.zeros_like(Mf)
    if not f64:
        Md = E.mode_matrix(z, l, only=[12])
        H[sl] = Md.h[sl]; Hl[sl] = Md.l[sl]
    s, ld = md.dd_logdet(H, Hl, True)[:2]
    nz = [md.dd_logdet(H + 1e-15 * np.random.default_rng(100 + k).standard_normal(H.shape) * mask * H, Hl, True)[0] for k in range(2)]
    ev[l] = dict(sign=float(s), ln=float(ld), noise=nz)
    print(f"  lam {l:.12f}: {'float64' if f64 else 'hybrid'} {s:+.0f} ln|det| {ld:.10f} (noise 1e-15 on blocks 0-11: {nz})", flush=True)
    return float(s), float(ld)


t0 = time.time()
root, nch = None, 0
for w in (0.02, 0.06, 0.15, 0.35):                          # ell_refine.lam_root's search, unchanged
    grid = guess * (1 + w * np.array([-1.0, 0.0, 1.0]))
    sg = [sd(l)[0] for l in grid]
    ch = [i for i in range(2) if sg[i] != sg[i + 1]]
    if ch:
        nch = len(ch)
        i = ch[0] if len(ch) == 1 else min(ch, key=lambda i: abs(0.5 * (grid[i] + grid[i + 1]) - guess))
        ref = 0.5 * (sd(grid[i])[1] + sd(grid[i + 1])[1])
        root = brentq(lambda l: sd(l)[0] * np.exp(sd(l)[1] - ref), grid[i], grid[i + 1], xtol=2e-8 * guess, rtol=1e-12)
        break
ls = sorted(ev); sgs = [ev[l]["sign"] for l in ls]
changes = [(ls[j], ls[j + 1]) for j in range(len(ls) - 1) if sgs[j] != sgs[j + 1]]
br = min(changes, key=lambda p: abs(0.5 * (p[0] + p[1]) - root)) if root is not None and changes else None
robust = all(all(x == e["sign"] for x in e["noise"]) for e in ev.values())
out = dict(D=D, kc=kc, mode="f64" if f64 else "hybrid", record=os.path.basename(recf), state=os.path.basename(st), F=F,
           record_system=same, quoted=quoted,
           system_check=("|F| within 1% of the quoted F; steps unchecked (stub record)" if quoted else "|F| within 1e-6 and equal steps"), lam_record=rec["lam"], lam_guess=guess, lam=root, minus_record=(root - rec["lam"]) if root else None,
           n_signchanges_grid=nch, n_changes_all=len(changes), bracket=br, bracket_width=(br[1] - br[0]) if br else None,
           noise_robust=robust, n_eval=len(ev), evals=ev, sec=round(time.time() - t0))
print(f"D {D} k_c {kc} {out['mode']}: lam {root} minus record {out['minus_record']}; grid changes {nch}, changes over all "
      f"{len(ev)} evaluations {len(changes)}, bracket width {out['bracket_width']}, noise-robust {robust} ({out['sec']} s)", flush=True)
open("data/ell_p4_hybrid_1025.jsonl", "a").write(json.dumps(out) + "\n")
