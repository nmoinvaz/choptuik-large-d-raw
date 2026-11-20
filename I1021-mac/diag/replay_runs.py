"""#1021: the F3 seed argcount passed to each point of a recount cache, by replaying its runs with a Multiplier whose
raw() takes each batch's records from the cache in order instead of computing them (replay_seeds.py for any cache);
each batch's records must be the points the replay asks for, in any order (argcount writes them as they return from
db28e274 on), or it stops. Run i starts from the cache's first P_i lines
and the leaves file L_i and replays the lines from P_i on; the seeds' F.extra holds the first R02N lines of R02 (the
0.2 file as the run found it). PROCS sets the batch size (2 x procs), as in the run.
    python replay_runs.py CODE CACHE R02 R02N PROCS OUT P1:L1 [P2:L2 ...] [--keepfix]
--keepfix keeps 'fix' in the copies of R02's records, as --seed does from 6da7da7b on (#1021); without it the copies
hold F3re, F3im and info only, as before 6da7da7b."""
import json, sys
keepfix = "--keepfix" in sys.argv
argv = [a for a in sys.argv if a != "--keepfix"]
code, cache, r02, r02n, procs, out = argv[1:7]
runs = [(int(a.split(":", 1)[0]), a.split(":", 1)[1]) for a in argv[7:]]
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
        win = self.src[:len(todo)]                    # the batch's records, in the order they returned (db28e274 on)
        at = {}
        for i, line in win:
            r = json.loads(line)
            at[(r["A"], r["wf"])] = (i, line, r)
        for p, s in zip(todo, seeds):
            if not self.src:
                raise Done
            hit = at.pop(self.key(p), None)
            if hit is None and len(win) < len(todo):  # the cache ends inside this batch
                raise Done
            assert hit is not None, (win[0][0], self.key(p), [k for k in at])
            i, line, r = hit
            self.src.remove((i, line))
            rows.append(dict(line=i, A=r["A"], wf=r["wf"], seed=list(s)))
            self.store(self.key(p), r)


def run(p0, p1, leaves):
    tmp = out + ".cache.tmp"
    open(tmp, "w").writelines(lines[:p0])
    F = Replay(3, tmp, int(procs), None, r1=0.17, m3fix=True, retry=True)
    z = (2.7264758856 / 2j) * (0.0532 + 0.0041j)
    F.extra[(-1.0, -1.0)] = dict(F3re=float(z.real), F3im=float(z.imag), info=0.0)
    for r in map(json.loads, r02l):
        F.extra.setdefault((r["A"], r["wf"]), dict(F3re=r["F3re"], F3im=r["F3im"], info=r["info"],
                                                  **({"fix": r.get("fix")} if keepfix else {})))
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
