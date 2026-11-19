"""#1021: one point of a recount's first batch through f_M3 of the argcount at CODE, with bounds (JSON or none);
prints the returned list with repr. python onepoint2.py CODE LEAVES CACHE SEEDFILE PROCS INDEX BOUNDS"""
import json, sys, time
code, leaves, cache, seedf, procs, idx, bounds = sys.argv[1:8]
sys.path.insert(0, code + "/solver/inner_stokes")
import argcount as ac


class Batch(Exception):
    pass


class Stop(ac.Multiplier):
    def raw(self, pts):
        todo, seen = [], set()
        for p in pts:
            k = self.key(p)
            if k not in self.vals and k not in seen:
                seen.add(k)
                todo.append(p)
        if todo:
            raise Batch([(p, self.seed(p)) for p in todo])


F = Stop(3, cache, int(procs), None, r1=0.17, m3fix=True, retry=True)
F.extra[(-1.0, -1.0)] = dict(F3re=float(((2.7264758856 / 2j) * (0.0532 + 0.0041j)).real),
                             F3im=float(((2.7264758856 / 2j) * (0.0532 + 0.0041j)).imag), info=0.0)
for r in map(json.loads, open(seedf)):
    F.extra.setdefault((r["A"], r["wf"]), dict(F3re=r["F3re"], F3im=r["F3im"], info=r["info"]))
try:
    ac.recount(F, list(map(json.loads, open(leaves))))
    raise SystemExit("no uncached point")
except Batch as e:
    p, seed = e.args[0][int(idx)]
b = json.loads(bounds) if bounds != "none" else None
args = (p, seed, 0.17, True) + ((b,) if b else ())
t = time.time()
r = ac.f_M3(args)
print(f"code {code} point {idx} {p!r} bounds {b}: {time.time() - t:.1f} s")
print("f_M3 returned:", repr(r))
