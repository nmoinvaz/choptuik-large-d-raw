#!/usr/bin/env python3
"""#1076 fu022mp_jump_width (dh610) width_jump.py selftest [--mutate] | run MAPDIR OUT: the width in A of the region where S_3 has two roots at xi1 0.249. Float64 solves of the M = 3 multiplier (argcount.py's own
Multiplier from the pinned worktree, not changed; the recount's options, no extended precision, 4 processes) at A = 3.7873456 + {-0.03125, -0.016, -0.004, -0.001, 0, +0.001, +0.004, +0.016, +0.03125} on the rows wf 0.23154321
and 0.24404321, each with two forced seeds: the L root and the R root that the map (../fu022mp_jump_map/m3/) found at that row on A = 3.7873456 (offset 0 repeats the map's solves). selftest: the forced seed of a row must be what seed() returns
and two rows must give two different seeds; --mutate ignores the forced seeds and the selftest exits 1."""
import json, os, sys

SI = "/home/nathan/Source/choptuik-large-d-1076b/solver/inner_stokes"
sys.path.insert(0, SI)
import argcount as AC                                            # noqa: E402

A0 = 3.7873456
OFFS = [-0.03125, -0.016, -0.004, -0.001, 0.0, 0.001, 0.004, 0.016, 0.03125]
ROWS = [0.23154321, 0.24404321]
R1 = 0.249


class ForcedRow(AC.Multiplier):
    def __init__(self, *a, rowseed=None, mutate_force=False, **k):
        super().__init__(*a, **k)
        self.rowseed, self.mutate_force = rowseed, mutate_force

    def seed(self, p):
        if self.rowseed is None or self.mutate_force:
            return super().seed(p)
        return self.rowseed[round(p[1], 8)]


def selftest(mutate):
    rs = {0.23154321: (0.1, -0.5), 0.24404321: (0.2, 0.3)}
    a = ForcedRow(3, None, 1, r1=R1, rowseed=rs, mutate_force=mutate)
    c = ForcedRow(3, None, 1, r1=R1)
    ok = (a.seed((3.78, 0.23154321)) == (0.1, -0.5) and a.seed((3.79, 0.24404321)) == (0.2, 0.3)
          and a.seed((3.78, 0.23154321)) != a.seed((3.78, 0.24404321))
          and c.seed((3.78, 0.23154321)) == AC.Multiplier(3, None, 1, r1=R1).seed((3.78, 0.23154321)))
    print("selftest" + (" --mutate" if mutate else ""), "PASS" if ok else "FAIL" + (" (FIRED)" if mutate else ""))
    return 0 if ok else 1


def edge_root(path, w):
    rows = [json.loads(l) for l in open(path) if l.strip()]
    r = [x for x in rows if abs(x["A"] - A0) < 1e-9 and abs(x["wf"] - w) < 1e-9][-1]
    assert AC.Multiplier.valued3(r), (path, w)
    return (r["F3re"], r["F3im"])


def run(mapdir, out):
    Ls = {round(w, 8): edge_root(f"{mapdir}/m3/points_M3_r0.249_L.jsonl", w) for w in ROWS}
    Rs = {round(w, 8): edge_root(f"{mapdir}/m3/points_M3_r0.249_R.jsonl", w) for w in ROWS}
    grid = [(round(A0 + o, 7), w) for w in ROWS for o in OFFS]
    bounds = dict(rhs=2.4e6, wall=3600.0, noise3=1e7)
    print(f"{len(grid)} locations; L seeds {Ls}; R seeds {Rs}", flush=True)
    for name, seeds in (("L", Ls), ("R", Rs)):
        cache = os.path.join(out, f"points_M3_r{R1}_{name}.jsonl")
        assert not os.path.exists(cache), cache
        F = ForcedRow(3, cache, 4, r1=R1, ymax=1e2, m3fix=True, retry=False, bounds=bounds, m3mp=False, rowseed=seeds)
        print(f"== pass {name}: {len(grid)} locations", flush=True)
        F.raw(grid)
        F.close()
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["selftest"]:
        sys.exit(selftest("--mutate" in a))
    sys.exit(run(a[1], a[2]))
