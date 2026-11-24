import sys, time
import numpy as np
sys.path.insert(0, "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/mh")
from common import *

key = sys.argv[1]
zh, zl, meta = load_state(key)
M = meta["M"]; nodes = meta["nodes"]; K = len(nodes)
s = solver(meta)
t = time.time()
segs = s.plan(zh, zl, 1e-32, 0.05)
print("plan", round(time.time() - t, 1), "s; steps per segment", [len(g) - 1 for g in segs], "total",
      sum(len(g) - 1 for g in segs), flush=True)
s.set_segs(segs)
fh, fl = s.residual(zh, zl)
print("|F|", float(np.abs(np.asarray(fh) + np.asarray(fl)).max()), "Delta", zh[-1], flush=True)
z = zh + zl
for i, x in enumerate(nodes):
    nd = node(z, M, i)
    p, m, a, c = nd[:M], nd[M:2 * M], nd[2 * M:3 * M], nd[3 * M:]
    print(f"node {i:2d} x {x:.6f}: min(c-x) {np.min(c - x):.4e} at j {np.argmin(c - x)}, max(c-x) {np.max(c - x):.3e}, "
          f"max|p| {np.abs(p).max():.3e} max|m| {np.abs(m).max():.3e} a {a.min():.3f}..{a.max():.3f}", flush=True)
prof_all = []
for b in range(1, K):
    xs = segs[b - 1]
    o = 2 * M + 4 * M * (b - 1)
    cur_h, cur_l = zh[o:o + 4 * M].copy(), zl[o:o + 4 * M].copy()
    prof = []
    for j in range(1, len(xs)):
        out = s.integrate(zh, zl, cur_h, cur_l, [xs[j - 1], xs[j]])
        cur_h, cur_l = np.asarray(out[0]), np.asarray(out[1])
        c = (cur_h + cur_l)[3 * M:]
        d = c - xs[j]
        prof.append((b, xs[j], d.min(), int(np.argmin(d))))
    mn = min(prof, key=lambda t: t[2])
    print(f"seg {b:2d} [{xs[0]:.6f},{xs[-1]:.6f}] {len(xs) - 1:4d} steps: min(c-x) {mn[2]:.4e} at x {mn[1]:.6f} j {mn[3]}",
          flush=True)
    prof_all += prof
np.save(os.path.join(OUT, f"prof_{key}.npy"), np.array(prof_all, float))
