t0 = time.time()
w0, i0 = ls.solve_point(ctx, [], None, "", verbose=True)
print("t=0:", i0["ok"], i0["why"], i0["its"], "g", ls.nstr(i0["g"][0], 6), ls.nstr(i0["g"][1], 6), "a", ls.nstr(ctx.a[0], 6), ls.nstr(ctx.a[1], 6), "delta", ls.nstr(i0["delta"], 20), f"{time.time() - t0:.0f} s")
w = w0
for e in (-30, -28, -26):
    t = float(f"1e{e}")
    t1 = time.time()
    w, info = ls.solve_point(ctx, [(t, ctx.vs[0])], w, "", verbose=True)
    print("t", t, info["ok"], info["why"], info["its"], "g", ls.nstr(info["g"][0], 6), ls.nstr(info["g"][1], 6), f"{time.time() - t1:.0f} s")
