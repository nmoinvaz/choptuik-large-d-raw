"""#1021: the F3 seed argcount passed to each point of a recount cache, by replaying its runs with a Multiplier whose
raw() takes each batch's records from the cache in order instead of computing them (replay_seeds.py for any cache);
each record's key must be the point the replay asks for, or it stops. Run i starts from the cache's first P_i lines
and the leaves file L_i and replays the lines from P_i on; the seeds' F.extra holds the first R02N lines of R02 (the
0.2 file as the run found it). PROCS sets the batch size (2 x procs), as in the run.
    python replay_runs.py CODE CACHE R02 R02N PROCS OUT P1:L1 [P2:L2 ...]"""
import json, sys
code, cache, r02, r02n, procs, out = sys.argv[1:7]
runs = [(int(a.split(":", 1)[0]), a.split(":", 1)[1]) for a in sys.argv[7:]]
sys.path.insert(0, code + "/solver/inner_stokes")
import argcount as ac

lines = open(cache).read().splitlines(True)
r02l = open(r02).read().splitlines(True)[:int(r02n)]
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
        seeds = [self.seed(p) for p in todo]          # as argcount builds the batch's args, before any is stored
        for p, s in zip(todo, seeds):
            if not self.src:
                raise Done
            i, line = self.src.pop(0)
            r = json.loads(line)
            assert (r["A"], r["wf"]) == self.key(p), (i, r["A"], r["wf"], self.key(p))
            rows.append(dict(line=i, A=r["A"], wf=r["wf"], seed=list(s)))
            self.store(self.key(p), r)


def run(p0, p1, leaves):
    tmp = out + ".cache.tmp"
    open(tmp, "w").writelines(lines[:p0])
    F = Replay(3, tmp, int(procs), None, r1=0.17, m3fix=True, retry=True)
    z = (2.7264758856 / 2j) * (0.0532 + 0.0041j)
    F.extra[(-1.0, -1.0)] = dict(F3re=float(z.real), F3im=float(z.imag), info=0.0)
    for r in map(json.loads, r02l):
        F.extra.setdefault((r["A"], r["wf"]), dict(F3re=r["F3re"], F3im=r["F3im"], info=r["info"]))
    F.src = list(enumerate(lines))[p0:p1]
    try:
        ac.recount(F, list(map(json.loads, open(leaves))))
    except Done:
        pass
    return len(F.src)


left = [run(p0, runs[i + 1][0] if i + 1 < len(runs) else len(lines), lv) for i, (p0, lv) in enumerate(runs)]
with open(out, "w") as fh:
    for row in rows:
        fh.write(json.dumps(row) + "\n")
print(f"replayed {len(rows)} records (lines {runs[0][0] + 1}-{len(lines)}); unreplayed per run: {left}")
