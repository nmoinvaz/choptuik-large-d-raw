"""#1021: why each unresolved leaf of a count is unresolved: along each of its four edges, the cache's points in order
with their value or the reason for none (no record, no value, |R| within 10 sigma, max|Y| over ymax), and each phase
step (a step >= dphi on a piece no longer than hmin also leaves the edge unresolved).
    python edge_cause.py CACHE LEAVES [--dphi 0.5] [--hmin 1e-5] [--ymax 100]"""
import json, math, sys
cache, leaves = sys.argv[1], sys.argv[2]
opt = dict(zip(sys.argv[3::2], sys.argv[4::2]))
dphi, hmin, ymax = float(opt.get("--dphi", 0.5)), float(opt.get("--hmin", 1e-5)), float(opt.get("--ymax", 100))
rk = lambda x: round(x, 9)
last = {}
for l in open(cache):
    r = json.loads(l)
    last[(rk(r["A"]), rk(r["wf"]))] = r
byA, byW = {}, {}
for k in last:
    byA.setdefault(k[0], []).append(k)
    byW.setdefault(k[1], []).append(k)


def val(k):
    r = last.get(k)
    if r is None:
        return None, "no record"
    v = complex(r["re"], r["im"])
    if not (math.isfinite(v.real) and math.isfinite(v.imag)):
        return None, "no value"
    if not r.get("ymax", 0) <= ymax:
        return None, f"max|Y| {r['ymax']:.3g}"
    if abs(v) < 10 * r.get("sig", 0):
        return None, f"|R| {abs(v):.3g} < 10 sigma {10 * r['sig']:.3g}"
    return v, f"|R|/sigma {abs(v) / r['sig']:.0f}" if r.get("sig") else "ok"


for line in open(leaves):
    L = json.loads(line)
    if L["ok"]:
        continue
    a0, a1, w0, w1 = (rk(L[x]) for x in ("a0", "a1", "w0", "w1"))
    print(f"leaf A {a0}-{a1}, wf {w0}-{w1} (depth {L['depth']})")
    for name, ks in (("bottom", sorted((k for k in byW.get(w0, []) if a0 - 1e-9 <= k[0] <= a1 + 1e-9))),
                     ("top", sorted((k for k in byW.get(w1, []) if a0 - 1e-9 <= k[0] <= a1 + 1e-9))),
                     ("left", sorted((k for k in byA.get(a0, []) if w0 - 1e-9 <= k[1] <= w1 + 1e-9), key=lambda k: k[1])),
                     ("right", sorted((k for k in byA.get(a1, []) if w0 - 1e-9 <= k[1] <= w1 + 1e-9), key=lambda k: k[1]))):
        vs = [val(k) for k in ks]
        bad = [(k, why) for k, (v, why) in zip(ks, vs) if v is None]
        steps = []
        for (p, (u, _)), (q, (v, _)) in zip(zip(ks[:-1], vs[:-1]), zip(ks[1:], vs[1:])):
            if u is not None and v is not None:
                s = abs((math.atan2(v.imag, v.real) - math.atan2(u.imag, u.real) + math.pi) % (2 * math.pi) - math.pi)
                Lp = math.hypot(q[0] - p[0], q[1] - p[1])
                if s >= dphi:
                    steps.append(f"step {s:.2f} rad over {Lp:.2g}{' (at hmin)' if Lp <= hmin else ''}")
        print(f"  {name}: {len(ks)} points" + (f"; without value: " + "; ".join(f"{k} {w}" for k, w in bad) if bad else "")
              + (f"; " + ", ".join(steps) if steps else "") + ("" if bad or steps else "; resolved"))
