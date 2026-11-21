# the strong step at t = 0 and the residual along it: lambda scan
import near_null as nn
L = ctx.L
zero = ctx.zero
R0 = ls.resid(ctx, ctx.z8)
xs, r, passes = ls.strong_step(ctx, R0)
print("strong step: |dw|", ls.omax8(xs), "|P R0|", ls.omax8(r), "passes", passes)
# u_k, k = 3..6 from the subspace iteration
def solve(b, transpose=False):
    x = ctx.s.olu_solve([np.ascontiguousarray(b)] + [zero] * 7, transpose)
    return np.asarray(x[0]) + np.asarray(x[1])
V, hist = nn.subspace(solve, L, 8, 32)
sig = hist[-1]
print("sigma_1..8", " ".join(f"{x:.3e}" for x in sig))
uk = []
for i in range(8):
    x = ctx.s.olu_solve([np.ascontiguousarray(V[:, i])] + [zero] * 7, True)
    x = [np.ascontiguousarray(np.asarray(p)) for p in x]
    rv = [ls.parts_to_mp(x, c) for c in range(L)]
    nr = mp.sqrt(mp.fsum(a * a for a in rv))
    uk.append([a / nr for a in rv])
def pk(X8):
    xm = [ls.parts_to_mp(X8, c) for c in range(L)]
    return [mp.fsum(uk[i][c] * xm[c] for c in range(L)) for i in range(8)]
print("u_k . R0, k=1..8:", " ".join(ls.nstr(v, 4) for v in pk(R0)))
# step components along v_k
dwm = [ls.parts_to_mp(xs, c) for c in range(L)]
print("v_k . step, k=1..8:", " ".join(ls.nstr(mp.fsum(mp.mpf(float(V[c, i])) * dwm[c] for c in range(L)), 4) for i in range(8)))
for e in range(-12, 1, 1):
    lam = float(f"1e{e}")
    zc = ctx.ax8(-lam, xs, ctx.z8)
    R = ls.resid(ctx, zc)
    pm = pk(R)
    print(f"lambda 1e{e}: max|R| {ls.omax8(R):.3e}; u_k.R k=1..8: " + " ".join(ls.nstr(v, 3) for v in pm), flush=True)
