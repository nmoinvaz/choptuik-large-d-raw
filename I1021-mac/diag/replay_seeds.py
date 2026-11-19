"""#1021: the F3 seed argcount 068913b4 passed to each point of the Mac's recount at xi1 0.17, by replaying the two
runs (the full recount from #1013's cache until its stop, then boxes 7-10 from the 627-line cache) with a Multiplier
whose raw() takes each batch's records from the cache in order instead of computing them; each record's key must be
the point the replay asks for, or it stops.
    python replay_seeds.py CODE I1021-mac OUT.jsonl"""
import json, sys
code, R, out = sys.argv[1:4]
sys.path.insert(0, code + "/solver/inner_stokes")
import argcount as ac

lines = open(f"{R}/m3/points_M3_r0.17.jsonl").read().splitlines(True)
rows = []


class Done(Exception):
    pass


class Replay(ac.Multiplier):
    def raw(self, pts):
        todo, seen = [], set()
        for p in pts:
            k = self.key(p)
            if k not in self.vals and k not in seen:
                seen.add(k)
                todo.append(p)
        if not todo:
            return
        seeds = [self.seed(p) for p in todo]          # as 068913b4 builds the batch's args, before any is stored
        for p, s in zip(todo, seeds):
            if not self.src:
                raise Done
            i, line = self.src.pop(0)
            r = json.loads(line)
            assert (r["A"], r["wf"]) == self.key(p), (i, r["A"], r["wf"], self.key(p))
            rows.append(dict(line=i, A=r["A"], wf=r["wf"], seed=list(s)))
            self.store(self.key(p), r)


def run(cache_lines, leaves, src):
    tmp = out + ".cache.tmp"
    open(tmp, "w").writelines(cache_lines)
    F = Replay(3, tmp, 2, None, r1=0.17, m3fix=True, retry=True)
    F.extra[(-1.0, -1.0)] = dict(F3re=float(((2.7264758856 / 2j) * (0.0532 + 0.0041j)).real),
                                 F3im=float(((2.7264758856 / 2j) * (0.0532 + 0.0041j)).imag), info=0.0)
    for r in map(json.loads, open(f"{R}/m3/points_M3_r0.2.jsonl")):
        F.extra.setdefault((r["A"], r["wf"]), dict(F3re=r["F3re"], F3im=r["F3im"], info=r["info"]))
    F.src = src
    try:
        ac.recount(F, list(map(json.loads, open(leaves))))
    except Done:
        pass
    return len(src)


left1 = run(lines[:214], f"{R}/m3/leaves_M3_cand_r0.25.jsonl", list(enumerate(lines))[214:627])
left2 = run(lines[:627], f"{R}/split/leaves_b07-10.jsonl", list(enumerate(lines))[627:])
with open(out, "w") as fh:
    for row in rows:
        fh.write(json.dumps(row) + "\n")
print(f"replayed {len(rows)} records (lines 215-{len(lines)}); unreplayed: run 1 {left1}, run 2 {left2}")
