"""the first batch of uncached points argcount 068913b4 sends to its pool for a --recount, from the leaves file and
the input cache, by running argcount's own recount with a Multiplier whose raw() stops at the first uncached point"""
import json, math, sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-1021run/solver/inner_stokes")
import argcount as ac

leaves, cache, seedf, procs = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])


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


F = Stop(3, cache, procs, None, r1=0.17, m3fix=True, retry=True)
F.extra[(-1.0, -1.0)] = dict(F3re=float(((2.7264758856 / 2j) * (0.0532 + 0.0041j)).real),
                             F3im=float(((2.7264758856 / 2j) * (0.0532 + 0.0041j)).imag), info=0.0)
for r in map(json.loads, open(seedf)):
    F.extra.setdefault((r["A"], r["wf"]), dict(F3re=r["F3re"], F3im=r["F3im"], info=r["info"]))
B = list(map(json.loads, open(leaves)))
try:
    ac.recount(F, B)
    print("no uncached point")
except Batch as e:
    todo = e.args[0]
    print(f"first batch: {len(todo)} points")
    for (p, s) in todo:
        box = [i for i, b in enumerate(B) if b["a0"] - 1e-9 <= p[0] <= b["a1"] + 1e-9 and b["w0"] - 1e-9 <= p[1] <= b["w1"] + 1e-9]
        # cached records at this point (the input's, skipped by --retry) and the nearest valued neighbours' |R|/sigma
        old = [r for k, r in F_all.items() if False] if False else None
        print(f"  A {p[0]:.7f} wf {p[1]:.8f}  seed F3 ({s[0]:.5g}, {s[1]:.5g})  box (in this file) {box}")
