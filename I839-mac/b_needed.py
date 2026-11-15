#!/usr/bin/env python3
"""#839: does arm B (--full_drop 1e-2) need its own run, given arm A's log of the same seed? newton_od's full_drop
accepts a lam-1 trial that the own test refused only when its max|F| <= 1e-2 of the step's |F|. When no lam-1 trial
of the A run comes within that, B takes every step as A did, bit for bit, and is not run (the coordinator, 2026-11-15
16:07 UTC).
usage: python3 b_needed.py A_LOG                 (exit 0: B needed; 1: not needed; 2: no steps in the log)
       python3 b_needed.py --selftest            (planted logs; exit 0 on pass)
       python3 b_needed.py --selftest --mutate=bar   (the drop at 1e-5 instead of 1e-2; must fail)"""
import re
import sys

DROP = 1e-2
TRIAL = re.compile(r"^    on (\d+) trial lam 1: max\|F\| (\S+);")
STEP = re.compile(r"^  on (\d+): \|F\| ([0-9.eE+-]+)")


def scan(lines, drop=DROP):
    """(needed, the lam-1 trials as (step, trial max|F|, the step's |F|), steps seen)"""
    trials, nf = [], {}
    for ln in lines:
        m = TRIAL.match(ln)
        if m:
            trials.append((int(m.group(1)), float(m.group(2))))
            continue
        m = STEP.match(ln)
        if m:
            nf[int(m.group(1))] = float(m.group(2))
    rows = [(k, f, nf[k]) for k, f in trials if k in nf]
    return any(f <= drop * n for _, f, n in rows), rows, len(nf)


def report(name, lines, drop=DROP):
    need, rows, n = scan(lines, drop)
    if not n:
        print(f"b_needed {name}: no steps in the log")
        return 2
    worst = min(rows, key=lambda r: r[1] / r[2]) if rows else None
    print(f"b_needed {name}: {n} steps, {len(rows)} refused lam-1 trials"
          + (f", the closest at step {worst[0]}: max|F| {worst[1]:.3e} = {worst[1] / worst[2]:.2e} of |F| {worst[2]:.3e}"
             if worst else "")
          + f" (drop {drop:g}): B {'needed' if need else 'not needed, it would repeat A'}")
    return 0 if need else 1


def selftest(mutate):
    drop = 1e-5 if mutate == "bar" else DROP
    far = ["    on 0 trial lam 1: max|F| 1.26e+18; raw |dz_t| 6.325e+12 vs |dz| 2.203e-12 (not <); refused, 842.5 s",
           "  on 0: |F| 3.40e-12 -> 2.97e-12, |dz| 2.20e-12 -> 1.93e-12, lam 0.125, dDelta -2.20e-12"]
    near = ["  on 2: |F| 2.09e-25 -> 2.58e-22, |dz| 2.83e-11 -> 8.77e-13, lam 1, dDelta -5.90e-12",
            "    on 3 trial lam 1: max|F| 1.11e-25; raw |dz_t| 7.180e-09 vs |dz| 8.765e-13 (not <); refused, 597.77 s",
            "  on 3: |F| 2.58e-22 -> 2.54e-22, |dz| 8.77e-13 -> 8.75e-13, lam 0.015625, dDelta -8.77e-13"]
    ok = True
    for name, lines, want in (("far", far, False), ("near (I777-mac step 3)", near, True)):
        got = scan(lines, drop)[0]
        ok &= got == want
        print(f"  {name}: B {'needed' if got else 'not needed'} (want {'needed' if want else 'not needed'})"
              f"{'' if got == want else '  <- wrong'}")
    print(f"b_needed selftest{' --mutate=' + mutate if mutate else ''}: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv):
    if argv and argv[0] == "--selftest":
        return selftest(next((a.split("=", 1)[1] for a in argv[1:] if a.startswith("--mutate=")), ""))
    with open(argv[0]) as f:
        return report(argv[0], f.read().splitlines())


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
