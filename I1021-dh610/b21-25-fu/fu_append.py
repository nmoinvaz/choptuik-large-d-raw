#!/usr/bin/env python3
"""fu_append.py CODE CACHE SRC.jsonl A,w LABEL: appends one point's valued record from another cache to the working cache.

SRC is a path or - (stdin; for `git show origin/main:<path>`). The record taken is the last one of that point in SRC that
the recount would read as valued (|r_3| < 1e-8 or fix.ok, finite R, max|Y| <= 100, |R| >= 10 sigma, noise_3 under the cap 1e7);
none: exit 1, nothing appended. The cache line is the record plus "fu": LABEL (where it came from). Prints its |R|/sigma and
|F_3 step| to the four nearest valued neighbours already in the cache, for the report; the sheet and noise-cap judgement of
a merge is not made here. Already appended (a line with the same A, wf and fu): exit 0, nothing appended."""
import json
import math
import sys

code, cache, src, pt, label = sys.argv[1:6]
sys.path.insert(0, code + "/solver/inner_stokes")
import argcount as ac  # noqa: E402

A, W = (float(x) for x in pt.split(","))
key = ac.Multiplier.key((A, W))
fin = lambda x: isinstance(x, float) and math.isfinite(x)


def valued(r):
    if not (ac.Multiplier.valued3(r) and fin(r.get("re")) and fin(r.get("im"))):
        return False
    noise = (r.get("fix") or {}).get("noise3", 0.0)
    return r.get("ymax", 0.0) <= 1e2 and math.hypot(r["re"], r["im"]) >= 10 * r.get("sig", 0.0) and noise < ac.NOISE3_CAP


cur, last, nrec = {}, None, 0
for line in open(cache):
    r = json.loads(line)
    cur[ac.Multiplier.key((r["A"], r["wf"]))] = r
if (cur.get(key) or {}).get("fu") == label:
    print(f"point {pt} already appended with fu {label!r}")
    sys.exit(0)
for n, line in enumerate(open(src) if src != "-" else sys.stdin, 1):
    r = json.loads(line)
    if ac.Multiplier.key((r["A"], r["wf"])) == key:
        nrec += 1
        if valued(r):
            last = (n, r)
if last is None:
    print(f"no valued record of {pt} in {src} ({nrec} records of the point)")
    sys.exit(1)
n, r = last
nb = sorted(((k[0] - A) ** 2 + (k[1] - W) ** 2, k, v) for k, v in cur.items()
            if k != key and ac.Multiplier.valued3(v) and fin(v.get("re")) and fin(v.get("F3re")))[:4]
f3 = complex(r["F3re"], r["F3im"])
steps = [(k, round(abs(f3 - complex(v["F3re"], v["F3im"])), 4)) for _, k, v in nb]
R = math.hypot(r["re"], r["im"])
print(f"{src} line {n} ({nrec} records of the point): |R| {R:.4g}, sigma {r['sig']:.4g}, |R|/sigma {R / r['sig']:.1f}, "
      f"info {r['info']:.3g}, trail {(r.get('fix') or {}).get('trail')}, noise3 {(r.get('fix') or {}).get('noise3')}, "
      f"F3 {f3:.4g}; |dF3| to the four nearest valued neighbours {steps}")
with open(cache, "a") as fh:
    fh.write(json.dumps(dict(r, fu=label)) + "\n")
print("appended")
