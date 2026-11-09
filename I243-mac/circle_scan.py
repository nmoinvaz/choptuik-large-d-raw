#!/usr/bin/env python3
"""I243-mac: the alias rule of #242 on the small circles of hp/modecount_circle.py (#178, #190, I68), from their
records and evaluation caches alone (no determinants).

    python3 circle_scan.py RECORDS.jsonl CACHE.jsonl [CACHE ...]     (each record reads only the cache of its own tag,
                                                                    modecount_<tag>_evals.jsonl)

For each circle the cached points with ||lam - c| - R| < 1e-9 are its samples. ln h = ln det M - beta (lam - c) with
the record's beta, as modecount_circle.py follows it. The winding from the wrapped steps must equal the record's,
and the point count too (a check that the samples are the circle's). Then, as on an edge, each arc's length is held
against the largest |Delta ln h| / arc of itself and 3 arcs each side (cyclic), and an arc is flagged when
length * scale > pi/2.
"""
import json
import math
import sys

recs = [json.loads(line) for line in open(sys.argv[1])]
caches = {}
for path in sys.argv[2:]:
    ev = caches.setdefault(path.split("/")[-1][len("modecount_"):-len("_evals.jsonl")], {})
    for line in open(path):
        x = json.loads(line)
        ev[(x["re"], x["im"])] = complex(x["lnabs"], x["arg"])


def wrap(a):
    return math.remainder(a, 2 * math.pi)


tot = 0
for r in recs:
    c, R, beta = complex(*r["center"]), r["R"], complex(*r["beta"])
    ev = caches.get(r["tag"], {})
    pts = sorted([((math.atan2(k[1] - c.imag, k[0] - c.real) / (2 * math.pi)) % 1.0, complex(*k), v)
                  for k, v in ev.items() if abs(abs(complex(*k) - c) - R) < 1e-9], key=lambda p: p[0])
    # touching circles share a point, stored twice with keys about 1e-16 apart: keep one per angle
    pts = [p for i, p in enumerate(pts) if i == 0 or p[0] - pts[i - 1][0] > 1e-9]
    if not pts:
        continue
    t = [p[0] for p in pts] + [pts[0][0] + 1.0]
    lh = [p[2] - beta * (p[1] - c) for p in pts]
    lh.append(lh[0])
    st = [wrap(lh[i + 1].imag - lh[i].imag) for i in range(len(pts))]
    arc = [(t[i + 1] - t[i]) * 2 * math.pi * R for i in range(len(pts))]
    sc = [abs(complex(lh[i + 1].real - lh[i].real, st[i])) / arc[i] for i in range(len(pts))]
    n = len(pts)
    w = sum(st) / (2 * math.pi)
    flags = []
    for i in range(n):
        s = max(sc[(i + j) % n] for j in range(-3, 4))
        if arc[i] * s > math.pi / 2:
            flags.append((i, arc[i], st[i], arc[i] * s))
    tot += len(flags)
    ok = abs(w - r["winding"]) < 1e-6 and n == r["points"]
    print(f"{r['tag']} c {c.real:+.4f}{c.imag:+.4f}i R {R}: {n} points (record {r['points']}), winding {w:+.4f} "
          f"(record {r['winding']:+.4f}){'' if ok else '  SAMPLES DO NOT MATCH THE RECORD'}, largest arc*scale "
          f"{max(a * max(sc[(i + j) % n] for j in range(-3, 4)) for i, a in enumerate(arc)):.2f}, {len(flags)} flagged"
          + "".join(f"\n    arc {i}: length {a:.4f}, step {s:+.3f}, length*scale {q:.2f}" for i, a, s, q in flags))
print(f"{tot} arcs flagged")
