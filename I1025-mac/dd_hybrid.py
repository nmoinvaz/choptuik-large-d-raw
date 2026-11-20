import sys, os, json, time, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
os.chdir("/Users/nathan/Source/choptuik-1025/solver/matter")
import multidouble as md
import ell_ddm
lams = [float(v) for v in sys.argv[1].split(",")]
S, z = ell_ddm._setup("data/sol_l1kc55Fs1025_D17.5000.npy", 17.5, 55)
E = ell_ddm.DDEll(S)
blocks, offs = S._block_list(); blk = 3 * S.n_odd + 2 * S.n_even
c0, nf, fun, tgt = blocks[12]; r0 = 12 * blk
mask = np.zeros((S.layout()[2] - 1,) * 2, bool)
for b, (cc, nn, ff, tt) in enumerate(blocks[:12]):
    mask[b * blk:(b + 1) * blk, cc:cc + nn] = True
out = "data/ell_ddm_hybrid_1025.jsonl"
for lam in lams:
    t0 = time.time()
    with np.errstate(all="ignore"):
        Mf = S.mode_matrix(z, lam)
    sf, lf, _, _ = md.dd_logdet(Mf, np.zeros_like(Mf), True)
    Md = E.mode_matrix(z, lam, only=[12])
    H, Hl = Mf.copy(), np.zeros_like(Mf)
    H[r0:r0 + blk, c0:c0 + nf] = Md.h[r0:r0 + blk, c0:c0 + nf]; Hl[r0:r0 + blk, c0:c0 + nf] = Md.l[r0:r0 + blk, c0:c0 + nf]
    sh, lh, umin, _ = md.dd_logdet(H, Hl, True)
    ns = []
    for sd in range(2):
        xi = np.random.default_rng(100 + sd).standard_normal(H.shape) * mask
        ns.append(md.dd_logdet(H + 1e-15 * xi * H, Hl, True)[0])
    rec = dict(D=17.5, kc=55, lam=lam, hybrid=[sh, lh], hybrid_noise_1e15=ns, f64=[sf, lf], sec=round(time.time() - t0))
    print(f"lam {lam}: hybrid {sh:+.0f} ln|det| {lh:.10f} (noise 1e-15 on blocks 0-11: {ns}); float64 {sf:+.0f} {lf:.10f} ({rec['sec']} s)", flush=True)
    open(out, "a").write(json.dumps(rec) + "\n")
