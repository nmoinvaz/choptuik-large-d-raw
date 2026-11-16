"""the predictor through the given states at D_target: min_i (c_i - x) along segment b (node b -> b+1) integrated
from the predictor's node b with D_target's equations on the last state's stored plan; with --truth T, the
predictor's error per node block against the state T"""
import sys, time
import numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a96e091f62ba437de/hp")
from hpkernel.driver import load, make_solver, predict

args = [a for a in sys.argv[1:] if not a.startswith("--")]
opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--"))
Dt = float(args[0])
b = int(args[1])
paths = args[2:]
hist = []
for p in paths:
    h, l, m = load(p)
    hist.append((m["D"], np.asarray(h) + np.asarray(l)))
M, nodes = m["M"], m["nodes"]
K = len(nodes)
zp = predict(hist, Dt)
if "truth" in opts:
    ht, lt, mt = load(opts["truth"])
    zt = ht + lt
    e = zp - zt
    print("predictor error: p1 %.2e c0 %.2e" % (abs(e[:M]).max(), abs(e[M:2 * M]).max()))
    for k in range(K):
        blk = e[2 * M + 4 * M * k:2 * M + 4 * M * (k + 1)].reshape(4, M)
        print("  node %g: p %.2e m %.2e a %.2e c %.2e" % ((nodes[k],) + tuple(abs(blk).max(axis=1))))
    print("  m_h %.2e a_h %.2e Delta %.2e" % (abs(e[2 * M + 4 * M * K:2 * M + 4 * M * K + M]).max(),
                                              abs(e[2 * M + 4 * M * K + M:-1]).max(), abs(e[-1])))
s = make_solver(Dt, M, nodes=nodes, kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=4)
import json
segs = json.load(open(opts["plan"])) if "plan" in opts else m["segs"]
s.set_segs(segs)
g = list(segs[b])
print(f"plan: {sum(len(q) - 1 for q in segs)} steps, segment {b}: {len(g) - 1}")
r = int(opts.get("refine", 1))
if r > 1:
    g = [float(v) for a_, b_ in zip(g[:-1], g[1:]) for v in np.linspace(a_, b_, r + 1)[:-1]] + [g[-1]]
off = 2 * M + 4 * M * b
sh, sl = zp[off:off + 4 * M].copy(), np.zeros(4 * M)
t = time.time()
worst = (1e9, None, None)
every = int(opts.get("every", 200)) * r
for j in range(len(g) - 1):
    out = s.integrate(zp, 0 * zp, sh, sl, g[j:j + 2])
    sh, sl = np.asarray(out[0]), np.asarray(out[1])
    st = (sh + sl).reshape(4, M)
    if not np.all(np.isfinite(st)):
        print(f"segment {b}: non-finite at x {g[j + 1]:.8f} (step {j + 1} of {len(g) - 1}); last min(c - x) {worst}")
        break
    d = st[3] - g[j + 1]
    i = int(np.argmin(d))
    if j % every == 0 or d[i] < 0 and worst[0] >= 0:
        print(f"   x {g[j + 1]:.8f} min(c - x) {d[i]:+.4e} at i {i}, max |state| {np.abs(st).max():.3e}")
    if d[i] < worst[0]:
        worst = (float(d[i]), g[j + 1], i)
else:
    e = zp[off + 4 * M:off + 8 * M]
    print(f"segment {b}: finite; min(c - x) {worst[0]:.4e} at x {worst[1]:.8f} i {worst[2]}; end mismatch "
          f"{np.abs(sh + sl - e).max():.3e}")
print(f"  {time.time() - t:.0f}s")
