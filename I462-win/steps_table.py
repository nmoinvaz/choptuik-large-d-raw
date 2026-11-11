"""#462: the table of accepted steps, from the chains' logs and the saved states' file times.

    python3 steps_table.py [--since-d10 D] [--since-d6 D]      run from the I462-win folder
    python3 steps_table.py --selftest

One row per accepted step: the base pivot (smallest, from the step's series line), the series and Newton times, the
re-seed, the number of od solves, max|F| after the first and after the second Newton solve, the converged max|F| and
the save time (UTC, the state file's write time; a state restored by git carries the restore time). --selftest parses a
block with known numbers (the d10 step to D 221.13125 as logged: 1.08e-30, then 1.27e-29, converged 2.66e-54) and
exits 1 when any value differs, and shows a changed value is caught."""
import datetime as dt
import glob
import os
import re
import sys


def parse(lines, chain):
    out, cur = [], None
    for l in lines:
        m = re.match(r"^step (\d+): D ([0-9.]+), pivots ([0-9.e+-]+)\.\.\S+, \|z_1\| \S+, \|z_N\| (\S+), ratios .*a_max ([0-9.]+), (\d+) s", l)
        if m:
            cur = dict(chain=chain, base=m.group(2), piv=m.group(3), zN=m.group(4), amax=m.group(5), series=m.group(6), f=[])
            out.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r"^    a ([0-9.]+): re-seeded \((\w+)\), ([0-9.]+) s", l)
        if m:
            cur.update(a=m.group(1), rs=m.group(2), rss=m.group(3))
        m = re.match(r"^  on (\d+): \|F\| (\S+) -> (\S+),", l)
        if m:
            cur["f"].append(m.group(3))                    # max|F| after the Newton solve number int(m.group(1)) + 1
        m = re.match(r"^  on \d+: \|F\| (\S+) converged", l)
        if m:
            cur["conv"] = m.group(1)
        m = re.match(r"^    a [0-9.]+ -> D ([0-9.]+):.*od (\d+) steps.*, (\d+) s$", l)
        if m:
            cur.update(D=m.group(1), n=m.group(2), nt=m.group(3))
    return [b for b in out if "D" in b]


def saved(chain, D):
    for dd in (float(D), float(D) + 1e-9):
        f = glob.glob(f"chain_{chain}/anm_pin3_D{dd:.4f}.npz")
        if f:
            return dt.datetime.fromtimestamp(os.path.getmtime(f[0]), dt.timezone.utc).strftime("%H:%M:%S")
    return "?"


def row(b):
    f1 = b["f"][0] if b["f"] else "?"
    f2 = b["f"][1] if len(b["f"]) > 1 else "?"
    return (f"| {b['chain']} | {b['base']} to {b['D']} | {b['series']} s | {b['piv']} | {b['rs']}, {float(b['rss']):.0f} s | {b['n']} | "
            f"{f1} | {f2} | {b['conv']} | {b['nt']} s | {saved(b['chain'], b['D'])} |")


HEAD = ("| chain | D | series | smallest pivot at the base | re-seed | od solves | max\\|F\\| after solve 1 | after solve 2 | converged max\\|F\\| "
        "| Newton time | saved (UTC) |\n|---|---|---|---|---|---|---|---|---|---|---|")


def selftest():
    block = ["step 5: D 220.13125, pivots 3.4e-17..1.4e+31, |z_1| 4.21e-04, |z_N| 3.40e-29, ratios 2-5 281.5 253.7 242.2 217.9, a_max 3.036, 3701 s",
             "    a 1.0000: re-seeded (ok), 278.96 s",
             "  on 0: |F| 2.48e-20 -> 1.08e-30, |dz| 1.5e-18 -> 6.4e-31, lam 1, dDelta +1.45e-19, piv 1.5e-17..2.0e+31, 552.97 s",
             "  on 1: |F| 1.08e-30 -> 1.27e-29, |dz| 6.4e-31 -> 3.0e-43, lam 1, dDelta -1.73e-31, piv 1.5e-17..2.0e+31, 190.56 s",
             "  on 2: |F| 1.27e-29 -> 2.66e-54, |dz| 3.0e-43 -> 1.3e-44, lam 1, dDelta +6.98e-44, piv 1.5e-17..2.0e+31, 235.62 s",
             "  on 3: |F| 2.66e-54 converged, Delta 1.69025329286197801 -5.7938e-17",
             "    a 1.000 -> D 221.13125: predicted |F| 4.46e+02, od 4 steps -> 4.15e+02 (tol 9.3e-20, stall accepted, Delta correction +0.0e+00), Delta 1.690253292862 (formula diff -1.4e-06), moved 1.5e-18, 1185 s"]
    b = parse(block, "d10")[0]
    want = dict(base="220.13125", D="221.13125", piv="3.4e-17", series="3701", n="4", nt="1185", conv="2.66e-54", rs="ok")
    ok = all(b[k] == v for k, v in want.items()) and b["f"][:2] == ["1.08e-30", "1.27e-29"]
    bad = parse([l.replace("1.27e-29", "9.99e-29") for l in block], "d10")[0]
    caught = bad["f"][:2] != ["1.08e-30", "1.27e-29"]
    print(f"selftest: known values parsed {ok}, a changed value is caught {caught}")
    return 0 if ok and caught else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    since = {"d10": 0.0, "d6": 0.0}
    for i, a in enumerate(sys.argv):
        if a == "--since-d10":
            since["d10"] = float(sys.argv[i + 1])
        if a == "--since-d6":
            since["d6"] = float(sys.argv[i + 1])
    print(HEAD)
    for c in ("d10", "d6"):
        for b in parse(open(f"chain_{c}.log", encoding="utf-8", errors="replace").read().splitlines(), c):
            if float(b["D"]) > since[c]:
                print(row(b))
