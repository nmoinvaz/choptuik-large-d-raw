"""#1025: lambda_1 at fixed state with the horizon series started at u0 (Ks 30), u0test_criteria.log.
usage (venv-1025dd): u0test.py STATE D kc GUESS u0[,u0...] f64|hybrid [--signs]"""
import sys, os, json, time, numpy as np
from scipy.optimize import brentq
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
os.chdir("/Users/nathan/Source/choptuik-1025/solver/matter")
from dss_ell import DSSEll, NODES_STD
st, D, kc, guess = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
u0s = [float(v) for v in sys.argv[5].split(",")]; mode = sys.argv[6]; dosigns = "--signs" in sys.argv
out = "data/ell_u0test_1025.jsonl"
z = np.load(st)
if mode == "hybrid":
    import multidouble as md
    import ell_ddm


def signs(M, nq=3, seed=11):                       # signtest.py's check, unchanged
    g = np.random.default_rng(seed)
    s0, l0 = np.linalg.slogdet(M)
    o = [float(s0)]
    for _ in range(nq):
        Q = np.linalg.qr(g.standard_normal(M.shape))[0]
        o.append(float(np.linalg.slogdet(Q @ M)[0] * np.linalg.slogdet(Q)[0]))
    return o


def lam_root(sd, guess):                           # ell_refine.lam_root, unchanged but for sd passed in
    cache = {}

    def c(l):
        if l not in cache:
            cache[l] = sd(l)
        return cache[l]
    for w in (0.02, 0.06, 0.15, 0.35):
        grid = guess * (1 + w * np.array([-1.0, 0.0, 1.0]))
        sg = [c(l)[0] for l in grid]
        ch = [i for i in range(2) if sg[i] != sg[i + 1]]
        if ch:
            i = ch[0] if len(ch) == 1 else min(ch, key=lambda i: abs(0.5 * (grid[i] + grid[i + 1]) - guess))
            ref = 0.5 * (c(grid[i])[1] + c(grid[i + 1])[1])
            r = brentq(lambda l: c(l)[0] * np.exp(c(l)[1] - ref), grid[i], grid[i + 1], xtol=2e-8 * guess, rtol=1e-12)
            return r, len(cache), len(ch), {f"{l:.10f}": c(l) for l in grid}
    return None, len(cache), 0, {}


for u0 in u0s:
    t0 = time.time()
    S = DSSEll(kc=kc, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=30, u0=u0)
    S.freeze_from(z, 0.7)
    with np.errstate(all="ignore"):
        F = float(np.linalg.norm(S.residual(z[None, :])[0]))
    print(f"D {D} k_c {kc} u0 {u0}: |F| at the state {F:.6e}", flush=True)
    if mode == "hybrid":
        E = ell_ddm.DDEll(S)
        blocks, offs = S._block_list(); blk = 3 * S.n_odd + 2 * S.n_even
        c0, nf, fun, tgt = blocks[12]; r0 = 12 * blk; sl = (slice(r0, r0 + blk), slice(c0, c0 + nf))
        mask = np.zeros((S.layout()[2] - 1,) * 2, bool)
        for b, (cc, nn, ff, tt) in enumerate(blocks[:12]):
            mask[b * blk:(b + 1) * blk, cc:cc + nn] = True

    noise = {}

    def sd(l):
        with np.errstate(all="ignore"):
            Mf = S.mode_matrix(z, l)
        if mode == "f64":
            s, ld = np.linalg.slogdet(Mf)
            return float(s), float(ld)
        Md = E.mode_matrix(z, l, only=[12])
        H, Hl = Mf.copy(), np.zeros_like(Mf); H[sl] = Md.h[sl]; Hl[sl] = Md.l[sl]
        s, ld = md.dd_logdet(H, Hl, True)[:2]
        noise[f"{l:.10f}"] = [md.dd_logdet(H + 1e-15 * np.random.default_rng(100 + k).standard_normal(H.shape) * mask * H, Hl, True)[0]
                              for k in range(2)]
        print(f"  lam {l:.10f}: hybrid {s:+.0f} ln|det| {ld:.10f} (noise 1e-15 on blocks 0-11: {noise[f'{l:.10f}']})", flush=True)
        return float(s), float(ld)
    r, nev, nch, grid = lam_root(sd, guess)
    rec = dict(D=D, kc=kc, u0=u0, Ks=30, mode=mode, state=os.path.basename(st), F=F, lam=r, lam_guess=guess, n_eval=nev,
               n_signchanges=nch, grid=grid, noise=noise or None, sec=round(time.time() - t0))
    if dosigns and r is not None:
        rec["signs"] = {}
        for l in (r - 0.02, r + 0.02):
            with np.errstate(all="ignore"):
                rec["signs"][f"{l:.10f}"] = signs(S.mode_matrix(z, l))
    print(f"D {D} k_c {kc} u0 {u0} ({mode}): lam {r} n_signchanges {nch} n_eval {nev} ({rec['sec']} s)"
          + (f"; signs at root -/+ 0.02 {list(rec['signs'].values())}" if "signs" in rec else ""), flush=True)
    open(out, "a").write(json.dumps(rec) + "\n")
