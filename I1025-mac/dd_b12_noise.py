import sys, os, json, time, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
os.chdir("/Users/nathan/Source/choptuik-1025/solver/matter")
import multidouble as md
import ddnp as dd
import ell_ddm
lams = [float(v) for v in sys.argv[1].split(",")]
epss = [1e-20, 1e-16, 1e-14, 1e-12, 1e-11, 1e-10, 1e-9]
S, z = ell_ddm._setup("data/sol_l1kc55Fs1025_D17.5000.npy", 17.5, 55)
blocks, offs = S._block_list(); blk = 3 * S.n_odd + 2 * S.n_even
c0, nf, fun, tgt = blocks[12]; r0 = 12 * blk
sl = (slice(r0, r0 + blk), slice(c0, c0 + nf))
out = "data/ell_ddm_b12noise_1025.jsonl"
for lam in lams:
    t0 = time.time()
    with np.errstate(all="ignore"):
        Mf = S.mode_matrix(z, lam)
    Md = ell_ddm.DDEll(S).mode_matrix(z, lam, only=[12])
    H, Hl = Mf.copy(), np.zeros_like(Mf)
    H[sl] = Md.h[sl]; Hl[sl] = Md.l[sl]
    s0, l0 = md.dd_logdet(H, Hl, True)[:2]
    rows = []
    for eps in epss:
        for sd in range(4):
            xi = np.random.default_rng(200 + sd).standard_normal((blk, nf))
            B = dd.add(dd.R(H[sl].copy(), Hl[sl].copy()), dd.R(eps * xi * H[sl]))
            Hn, Hnl = H.copy(), Hl.copy(); Hn[sl] = B.h; Hnl[sl] = B.l
            s, l = md.dd_logdet(Hn, Hnl, True)[:2]
            rows.append(dict(eps=eps, seed=sd, sign=s, dln=l - l0))
        r = [x for x in rows if x["eps"] == eps]
        print(f"lam {lam} eps {eps:.0e}: signs {[x['sign'] for x in r]} (unperturbed {s0:+.0f}), ln shifts "
              ", ".join(f"{x['dln']:+.1e}" for x in r), flush=True)
    flips = [x["eps"] for x in rows if x["sign"] != s0]
    rec = dict(D=17.5, kc=55, lam=lam, sign0=s0, ln0=l0, rows=rows, eps_star=min(flips) if flips else None, sec=round(time.time() - t0))
    print(f"lam {lam}: unperturbed {s0:+.0f} {l0:.10f}; smallest eps with a flip: {rec['eps_star']} ({rec['sec']} s)", flush=True)
    open(out, "a").write(json.dumps(rec) + "\n")
