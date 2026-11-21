"""#1021: the unresolved leaves of the recount of record and why. Read-only from a cache, with argcount's Multiplier and
Counter (the code at CODE): a point not in the cache stops the run, so nothing is computed.
    python leftovers.py CODE CACHE LEAVES R1 [--mutate=unguard]
For each leaf with ok false: its boundary walked as argcount's count walks it (dphi 0.5, hmin 1e-5), and every boundary
point without value, with the cause from its cache record (argcount's own note) and its |R|/sigma. A leaf whose
boundary has no point without value is reported as unresolved for another reason. Exit 0 when every unresolved leaf has
at least one named point, 1 otherwise. --mutate=unguard drops the 10 sigma guard (every valued point gets its value), so
the leaves blocked by the guard alone must lose their named points: it must give exit 1 when any leaf is blocked by the
guard alone (or stop at a point not in the cache, which the walk without the guard needs). --mutate=drop drops the
named points of the first unresolved leaf, which must give exit 1."""
import collections, json, math, sys

code, cache, leaves_f, r1 = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
unguard = "--mutate=unguard" in sys.argv
drop = "--mutate=drop" in sys.argv
sys.path.insert(0, code + "/solver/inner_stokes")
import argcount as ac  # noqa: E402

F = ac.Multiplier(3, cache, 1, r1=r1, m3fix=True, retry=False)
if unguard:
    for k, r in F.extra.items():
        if ac.Multiplier.valued3(r) and math.isfinite(r["re"]) and r.get("ymax", 0.0) <= F.ymax:
            F.vals[k] = complex(r["re"], r["im"])


def raw(pts):
    miss = [p for p in pts if ac.Multiplier.key(p) not in F.vals]
    if miss:
        raise SystemExit(f"{len(miss)} points not in the cache, e.g. {miss[:3]}: nothing is computed here")


F.raw = raw
seen = []
call = F.__class__.__call__
F.__class__.__call__ = lambda self, p: (seen.append(p), call(self, p))[1]
L = [json.loads(line) for line in open(leaves_f)]
un = [x for x in L if not x["ok"]]
causes, named, n_guard_only = collections.Counter(), 0, 0
for x in un:
    seen.clear()
    C = ac.Counter(F, 0.5, 1e-5)
    W, wraw, tv, mn, ok = C.cell(x["a0"], x["a1"], x["w0"], x["w1"])
    bad = sorted({ac.Multiplier.key(p) for p in list(seen) if not math.isfinite(abs(call(F, p)))})
    if drop and x is un[0]:
        bad = []
    notes = []
    for k in bad:
        r = F.extra[k]
        v = complex(r["re"], r["im"])
        rs = abs(v) / r["sig"] if math.isfinite(abs(v)) and r.get("sig") else float("nan")
        n = F.note(r)
        if n.startswith("no value: |R|"):
            n = f"guard, |R|/sigma {rs:.3g}"
        else:
            n = n.replace("no value: ", "")
        notes.append((k, n))
        causes[n.split(",")[0] if n.startswith("guard") else n[:60]] += 1
    named += bool(notes)
    n_guard_only += bool(notes) and all(n.startswith("guard") for _, n in notes)
    print(flush=True, *[f"leaf A {x['a0']:.7f}-{x['a1']:.7f} w {x['w0']:.8f}-{x['w1']:.8f} (depth {x['depth']}): "
          f"{'resolved' if ok else 'unresolved'} here; {len(bad)} boundary points without value"
          + "".join(f"\n    ({k[0]:.7f}, {k[1]:.8f}): {n}" for k, n in notes)])
print(f"{len(un)} unresolved leaves, {named} with a named point, {n_guard_only} blocked by the guard alone")
print("causes over the named points: " + "; ".join(f"{c} {n}" for n, c in causes.most_common()))
ok = named == len(un)
print(f"leftovers check{' (--mutate=unguard)' if unguard else ' (--mutate=drop)' if drop else ''}: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
