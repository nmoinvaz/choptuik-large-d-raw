#!/usr/bin/env python3
"""#1076 fu022mp_jump_map (dh610) map_jump.py selftest [--mutate] | run SRC_CACHE SEED02 OUT: float64 solves of the M = 3 multiplier at xi1 0.249 on a 5 x 5 grid of the lower half of the #1076 box
(A 3.6623456 to 3.9123456, wf 0.20654321 to 0.25654321) plus the two points of the gap on A = 3.7873456 (wf 0.239868405312 and 0.239874508828), in three passes with argcount.py's own Multiplier (imported from the pinned
worktree, not changed): STD = the recount's rule (F_3 seed from the nearest valued point, from a copy of the recount's cache), L = the seed forced to the F_3 of the gap's lower point, R = forced to the F_3 of its upper point.
The options are the recount's (--m3fix, bounds rhs 2.4e6, wall 3600, noise3 1e7, no extended precision, 4 processes). selftest: the forced seed must be what seed() returns (two different forced seeds, two different answers);
--mutate ignores the forced seed and the selftest exits 1."""
import json, os, shutil, sys

SI = "/home/nathan/Source/choptuik-large-d-1076b/solver/inner_stokes"
sys.path.insert(0, SI)
import argcount as AC                                            # noqa: E402

AS = [3.6623456, 3.7248456, 3.7873456, 3.8498456, 3.9123456]
WS = [0.20654321, 0.21904321, 0.23154321, 0.24404321, 0.25654321]
GAP_L, GAP_R = 0.239868405312, 0.239874508828
R1 = 0.249


class Forced(AC.Multiplier):
    def __init__(self, *a, forced=None, mutate_force=False, **k):
        super().__init__(*a, **k)
        self.forced, self.mutate_force = forced, mutate_force

    def seed(self, p):
        return super().seed(p) if (self.forced is None or self.mutate_force) else self.forced


def selftest(mutate):
    a = Forced(3, None, 1, r1=R1, forced=(0.1, -0.5), mutate_force=mutate)
    b = Forced(3, None, 1, r1=R1, forced=(0.2, 0.3), mutate_force=mutate)
    c = Forced(3, None, 1, r1=R1)
    p = (3.7873456, 0.24)
    ok = a.seed(p) == (0.1, -0.5) and b.seed(p) == (0.2, 0.3) and a.seed(p) != b.seed(p) and c.seed(p) == AC.Multiplier(3, None, 1, r1=R1).seed(p)
    print("selftest" + (" --mutate" if mutate else ""), "PASS" if ok else "FAIL" + (" (FIRED)" if mutate else ""))
    return 0 if ok else 1


def gap_rows(src):
    rows = [json.loads(l) for l in open(src) if l.strip()]
    pick = lambda w: [r for r in rows if abs(r["A"] - 3.7873456) < 1e-9 and abs(r["wf"] - w) < 1e-9][-1]
    return pick(GAP_L), pick(GAP_R)


def run(src, seed02, out):
    gl, gr = gap_rows(src)
    for r in (gl, gr):
        assert AC.Multiplier.valued3(r), "a gap seed is not valued"
    lseed, rseed = (gl["F3re"], gl["F3im"]), (gr["F3re"], gr["F3im"])
    grid = [(a, w) for a in AS for w in WS] + [(gl["A"], gl["wf"]), (gr["A"], gr["wf"])]
    bounds = dict(rhs=2.4e6, wall=3600.0, noise3=1e7)
    print(f"grid {len(grid)} locations; L seed {lseed}, R seed {rseed}", flush=True)
    for name, forced in (("std", None), ("L", lseed), ("R", rseed)):
        cache = os.path.join(out, f"points_M3_r{R1}_{name}.jsonl")
        assert not os.path.exists(cache), cache
        if name == "std":
            shutil.copyfile(src, cache)
        F = Forced(3, cache, 4, r1=R1, ymax=1e2, m3fix=True, retry=False, bounds=bounds, m3mp=False, forced=forced)
        F.extra[(-1.0, -1.0)] = dict(F3re=float(((2.7264758856 / 2j) * (0.0532 + 0.0041j)).real),
                                     F3im=float(((2.7264758856 / 2j) * (0.0532 + 0.0041j)).imag), info=0.0)
        for r in map(json.loads, open(seed02)):
            F.extra.setdefault((r["A"], r["wf"]), AC.Multiplier.seed_record(r))
        print(f"== pass {name}: {len(grid)} locations, {sum(1 for p in grid if F.key(p) in F.vals)} already in the cache", flush=True)
        F.raw(grid)
        F.close()
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["selftest"]:
        sys.exit(selftest("--mutate" in a))
    sys.exit(run(a[1], a[2], a[3]))
