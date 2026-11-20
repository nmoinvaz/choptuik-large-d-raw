#!/usr/bin/env python3
"""fu_value.py CODE CACHE ROWS.jsonl (--points "A,w;A,w" | --auto LEAVES) [--procs 3] [--append]
   fu_value.py CODE CACHE ROWS.jsonl --retest PREV_ROWS.jsonl [--mutate f3|lowguard]

#1021 follow-up (dh610): values M = 3 points that argcount left without value, again, from other starts, and takes a value
into the cache only if it passes the same tests as a point of the recount.

Each point is run through f_M3 of the argcount at CODE (xi1 0.17, --m3fix) in these variants, in this order:
  default     the run's own settings (right-hand-side bound 2.4e6, starts 0.25 then 0.2, nearest valued neighbour's F_3 as seed);
              it must reproduce the cache's record (the control that this script runs the same function)
  rhs1e7      right-hand-side bound 1e7
  s0.2        starts 0.2 then 0.25, bound 1e7
  seed2       the second nearest valued neighbour's F_3 as seed, bound 1e7
  seed3       the third nearest
  s0.2seed2   starts 0.2 then 0.25, second nearest seed, bound 1e7
A row is accepted when all of these hold: the point is valued by the continuation or tuned (|r_3| < 1e-8 or fix.ok), the
path stays under max|Y| 100, |R| >= 10 sigma (the guard, not lowered), and F_3 is within 0.1 of that of the nearest valued
neighbour in the cache (one sheet of S_3 = 0; 0.1 is the step sheet_connect.py of I1021-mac allows). --append writes, for
each point, the first accepted row as a cache line (with "fu": the variant), so that the recount reads it with --retry.

--retest re-applies the tests to the rows of an earlier run with a mutation, without computing: f3 adds 0.3i to every F_3
(the sheet test must then reject everything it accepted), lowguard uses 1 sigma for the guard (it accepts what the guard
blocked). Exit 1 when the mutated decisions differ from the plain ones (the check fired), 0 when they do not.
Plain run: exit 0 when every point has an accepted row, 2 when some has none (reported with its cause per variant).
"""
import argparse
import json
import math
import multiprocessing as mp
import os
import sys
import time

CODE = sys.argv[1]
sys.path.insert(0, CODE + "/solver/inner_stokes")
import argcount as ac  # noqa: E402

R1 = 0.17
VARIANTS = [                                   # name, bounds beyond wall 3600 and noise cap 1e7, starts, seed rank
    ("default", dict(rhs=2.4e6), None, 0),
    ("rhs1e7", dict(rhs=1e7), None, 0),
    ("s0.2", dict(rhs=1e7), [0.2, 0.25], 0),
    ("seed2", dict(rhs=1e7), None, 1),
    ("seed3", dict(rhs=1e7), None, 2),
    ("s0.2seed2", dict(rhs=1e7), [0.2, 0.25], 1),
]
SHEET_STEP = 0.1


def job(a):
    i, args = a
    c, w = time.process_time(), time.time()
    return i, ac.f_M3(args), time.process_time() - c, time.time() - w


def finite(x):
    return isinstance(x, float) and math.isfinite(x)


def has_value(r):
    """a record as the recount reads it: valued by the inner solve or the continuation, path and guard passed"""
    if not (ac.Multiplier.valued3(r) and finite(r.get("re")) and finite(r.get("im"))):
        return False
    return r.get("ymax", 0.0) <= 1e2 and math.hypot(r["re"], r["im"]) >= 10 * r.get("sig", 0.0)


def load(cache):
    """the latest record of each point, as the cache loader keeps them (a later line replaces an earlier one)"""
    recs = {}
    for line in open(cache):
        r = json.loads(line)
        recs[ac.Multiplier.key((r["A"], r["wf"]))] = r
    return recs


def ranked(recs, p, ok, n):
    """the n nearest records passing ok, by the distance seed() uses"""
    k0 = ac.Multiplier.key(p)
    c = [(((k[0] - p[0]) ** 2 + (k[1] - p[1]) ** 2), k, r) for k, r in recs.items() if k != k0 and ok(r)]
    c.sort(key=lambda t: t[0])
    return c[:n]


GUARD = 10.0           # --break (selftest only) sets 1.0: the selftest must then fail


def decide(row, guard=None, f3shift=0j):
    """the tests on a row's stored data; returns the row's verdicts"""
    guard = GUARD if guard is None else guard
    ok_val = bool(row["valued3"]) and finite(row["re"]) and finite(row["im"])
    ratio = math.hypot(row["re"], row["im"]) / row["sig"] if ok_val and row["sig"] else float("nan")
    ok_guard = ok_val and row["ymax"] <= 1e2 and math.hypot(row["re"], row["im"]) >= guard * row["sig"]
    f3 = complex(row["F3re"], row["F3im"]) + f3shift
    d = [abs(f3 - complex(n[2], n[3])) for n in row["nbrs"]]
    ok_sheet = bool(d) and d[0] <= SHEET_STEP
    return dict(ratio=ratio, ok_guard=bool(ok_guard), dF3_nearest=(d[0] if d else None), ok_sheet=ok_sheet,
                accepted=bool(ok_val and ok_guard and ok_sheet))


def why(r):
    """a record without value in words (the cause)"""
    if not finite(r.get("info")):
        return f"inner solve: {r.get('info')}"
    fx = r.get("fix") or {}
    if fx.get("bound"):
        return f"{fx['bound'][-1][1]} at xi1 {fx['bound'][-1][0]}"
    if not finite(r["re"]):
        return f"continuation lost S3's zero after {fx.get('trail')}" if fx else f"|r3| {r['info']:.3g}"
    return "ok"


def selftest(brk):
    """the decisions on synthetic rows: a row at 12 sigma on one sheet is accepted, one at 9 sigma is blocked by the guard,
    one 0.3 from its neighbour's F_3 by the sheet test; f3 and lowguard change exactly those decisions"""
    global GUARD
    GUARD = 1.0 if brk else 10.0
    row = lambda ratio, d: dict(valued3=True, re=12.0 * ratio, im=0.0, sig=12.0, ymax=1.0, F3re=0.0, F3im=-0.1 + d,
                                nbrs=[[0, 0, 0.0, -0.1]])
    ok = [decide(row(12, 0.0))["accepted"] is True, decide(row(9, 0.0))["ok_guard"] is False,
          decide(row(12, 0.3))["ok_sheet"] is False, decide(row(12, 0.0), f3shift=0.3j)["accepted"] is False,
          decide(row(9, 0.0), guard=1.0)["accepted"] is True]
    print(f"selftest{' --break' if brk else ''}: accepted at 12 sigma {ok[0]}, 9 sigma blocked {ok[1]}, sheet step 0.3 blocked "
          f"{ok[2]}, f3 mutation rejects {ok[3]}, lowguard accepts 9 sigma {ok[4]}: {'PASS' if all(ok) else 'FAIL'}")
    return 0 if all(ok) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("code")
    ap.add_argument("cache", nargs="?")
    ap.add_argument("rows", nargs="?")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--break", dest="brk", action="store_true")
    ap.add_argument("--points")
    ap.add_argument("--auto")
    ap.add_argument("--procs", type=int, default=3)
    ap.add_argument("--append", action="store_true")
    ap.add_argument("--retest")
    ap.add_argument("--mutate", choices=["f3", "lowguard"])
    ap.add_argument("--exclude", help='points "A,w;A,w" that are not valued here (default: the lines of exclude_points.txt '
                                      'beside ROWS, if it exists); the coordinator\'s word on 20 Nov, 03:17 UTC')
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.brk)
    if a.retest:
        prev = [json.loads(line) for line in open(a.retest)]
        shift, guard = (0.3j if a.mutate == "f3" else 0j), (1.0 if a.mutate == "lowguard" else GUARD)
        plain = [decide(r)["accepted"] for r in prev]
        mut = [decide(r, guard, shift)["accepted"] for r in prev]
        with open(a.rows, "w") as fh:
            for r, p, m in zip(prev, plain, mut):
                fh.write(json.dumps(dict(A=r["A"], wf=r["wf"], variant=r["variant"], plain_accepted=p,
                                         mutated_accepted=m, mutate=a.mutate)) + "\n")
        print(f"retest of {len(prev)} rows with --mutate={a.mutate}: plain accepts {sum(plain)}, mutated accepts {sum(mut)}")
        print("control fired" if plain != mut else "control did not fire (the mutation changes no decision on these rows)")
        return 1 if plain != mut else 0
    recs = load(a.cache)
    if a.points:
        pts = [tuple(float(x) for x in s.split(",")) for s in a.points.split(";")]
    else:
        cells = [json.loads(line) for line in open(a.auto)]
        cells = [(c["a0"], c["a1"], c["w0"], c["w1"]) for c in cells if not c["ok"]]
        pts = []
        for k, r in sorted(recs.items()):
            if not has_value(r) and any(a0 - 1e-9 <= k[0] <= a1 + 1e-9 and w0 - 1e-9 <= k[1] <= w1 + 1e-9
                                        for a0, a1, w0, w1 in cells):
                pts.append(k)
    ex = a.exclude
    if ex is None and os.path.exists(os.path.join(os.path.dirname(os.path.abspath(a.rows)), "exclude_points.txt")):
        ex = open(os.path.join(os.path.dirname(os.path.abspath(a.rows)), "exclude_points.txt")).read().strip()
    if ex:
        gone = {ac.Multiplier.key(tuple(float(x) for x in s_.split(","))) for s_ in ex.replace("\n", ";").split(";") if s_.strip()}
        print(f"excluded from valuing: {sorted(gone)}", flush=True)
        pts = [p for p in pts if ac.Multiplier.key(p) not in gone]
    jobs, meta = [], []
    for p in pts:
        nb = ranked(recs, p, lambda r: ac.Multiplier.valued3(r) and finite(r.get("F3re")), 3)
        nv = ranked(recs, p, has_value, 4)
        for name, bd, starts, rank in VARIANTS:
            if rank >= len(nb):
                continue
            seed = (nb[rank][2]["F3re"], nb[rank][2]["F3im"])
            bounds = dict(wall=3600.0, noise3=ac.NOISE3_CAP, **bd)
            if starts:
                bounds["starts"] = starts
            jobs.append((len(jobs), (p, seed, R1, True, bounds)))
            meta.append(dict(A=p[0], wf=p[1], variant=name, rhs=bd["rhs"], starts=starts or [0.25, 0.2], seed_from=list(nb[rank][1]),
                             seed=list(seed), nbrs=[[k[0], k[1], r["F3re"], r["F3im"]] for _, k, r in nv]))
    print(f"{len(pts)} points, {len(jobs)} runs of f_M3 at xi1 {R1} with --procs {a.procs} (code {CODE})", flush=True)
    rows = [None] * len(jobs)
    ctx = mp.get_context("spawn")
    with ctx.Pool(a.procs) as pool, open(a.rows, "w") as fh:
        for i, r, cpu, wall in pool.imap_unordered(job, jobs):
            m = meta[i]
            fx = r[7] if len(r) > 7 else None
            rec = dict(A=m["A"], wf=m["wf"], re=r[0], im=r[1], info=r[2], r1=R1, F3re=r[3], F3im=r[4], ymax=r[5], sig=r[6])
            if fx:
                rec["fix"] = fx
            row = dict(m, cpu_s=round(cpu, 1), wall_s=round(wall, 1), re=r[0], im=r[1], info=r[2], F3re=r[3], F3im=r[4],
                       ymax=r[5], sig=r[6], fix=fx, valued3=ac.Multiplier.valued3(rec), why=why(rec))
            row.update(decide(row))
            k0 = ac.Multiplier.key((m["A"], m["wf"]))
            c = recs.get(k0)
            if m["variant"] == "default" and c and finite(c.get("re")) and finite(r[0]):
                row["repro_rel"] = abs(complex(r[0], r[1]) - complex(c["re"], c["im"])) / abs(complex(c["re"], c["im"]))
            rows[i] = (rec, row)
            fh.write(json.dumps(row) + "\n")
            fh.flush()
            absr = math.hypot(r[0], r[1]) if finite(r[0]) else float("nan")
            print(f"  point {m['A']:.7f} {m['wf']:.8f} {m['variant']:>9}: {row['why']}, |R| {absr:.3g}, sigma {r[6]:.3g}, "
                  f"|R|/sigma {row['ratio']:.3g}, dF3 {row['dF3_nearest']}, accepted {row['accepted']}"
                  + (f", repro {row['repro_rel']:.2g}" if "repro_rel" in row else "") + f", {cpu:.0f} CPU s", flush=True)
    got, miss = 0, []
    with open(a.cache, "a") as cf:
        for p in pts:
            mine = [x for x in rows if x and (x[1]["A"], x[1]["wf"]) == p]
            first = next((x for x in mine if x[1]["accepted"]), None)
            if first:
                got += 1
                if a.append:
                    cf.write(json.dumps(dict(first[0], fu=first[1]["variant"])) + "\n")
            else:
                miss.append((p, [(x[1]["variant"], x[1]["why"], round(x[1]["ratio"], 2) if finite(x[1]["ratio"]) else None)
                                 for x in mine]))
    print(f"accepted {got} of {len(pts)} points" + (", appended to the cache" if a.append else ", not appended"))
    for p, v in miss:
        print(f"  no accepted row for {p}: {v}")
    return 0 if not miss else 2


if __name__ == "__main__":
    sys.exit(main())
