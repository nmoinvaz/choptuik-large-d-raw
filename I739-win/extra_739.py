#!/usr/bin/env python3
"""#739, read-only extras from the saved states: (1) attempt times, octo-double here against the stalled quad-double ones of #726; (2) Delta_full - Delta_held at D 113 (the point #726 did not reach), NOT asked by the issue.
usage: python extra_739.py          (venv-t151 python, from this folder; needs the stage checkout's T138-win2/chain held states and the worktree's hp/data/delta_all.csv, as I726-win/table_726.py does)
Control for (2): the same arithmetic at D 112, from #726's quad-double state, must reproduce #726's +4.2096e-13 (a mismatch exits 1 before D 113 is printed).
Delta of a state = the exact sum of the last entry of every part present, arb at 600 bits."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RAW, "I726-win"))
import table_726 as t26          # noqa: E402  (fits_err, STAGE, DELTA_ALL; sets arb precision 400, raised below)
import cmp_739 as c              # noqa: E402  (delta of eight parts; sets arb precision 600)

LAST = lambda p: float(json.loads(open(p).read().splitlines()[-1])["attempts"][-1]["t_corr"])


def attempts(path, step=None):
    out = []
    for ln in open(path):
        r = json.loads(ln)
        if step is None or r["step"] == step:
            for at in r["attempts"]:
                out.append((r["D0"], at["a"], at["D"], at["steps"], at["t_corr"], at["accepted"], at["F_final"]))
    return out


print("(1) attempt times\n")
print("| run | from D | a | to D | corrector steps | seconds in the corrector | accepted |\n|---|---|---|---|---|---|---|")
for D0, a, D, n, tc, acc, F in attempts(os.path.join(RAW, "I726-win", "L", "anm_run.jsonl"), 9):
    print(f"| #726 quad-double | {D0:g} | {a:g} | {D:g} | {n} | {tc:.0f} | {acc} |")
for name in ("A", "B"):
    p = os.path.join(HERE, name, "anm_run.jsonl")
    if os.path.exists(p):
        for D0, a, D, n, tc, acc, F in attempts(p):
            print(f"| #739 octo-double ({name}) | {D0:g} | {a:g} | {D:g} | {n} | {tc:.0f} | {acc} |")

print("\n(2) Delta_full - Delta_held (extra, not asked)\n")
err = t26.fits_err()
c.flint.ctx.prec = 600
held = lambda D: os.path.join(t26.STAGE, "T138-win2", "chain", f"anm_pin3_D{D}.0000.npz")


def shift(full, D):
    return float((c.delta(full) - c.delta(held(D))).mid())


s112 = shift(os.path.join(RAW, "I726-win", "L", "anm_pin13_D112.0000.npz"), 112)
want = 4.2096e-13
print(f"control, D 112 from #726's quad-double state: {s112:+.4e} (#726 reported +4.2096e-13) {'ok' if abs(s112 - want) < 5e-18 else 'MISMATCH'}")
if abs(s112 - want) >= 5e-18:
    sys.exit(1)
b = os.path.join(HERE, "B", "anm_pin13_D113.0000.npz")
if os.path.exists(b) and os.path.exists(held(113)):
    s113 = shift(b, 113)
    e113 = t26.fits_err().get(113.0)
    e112 = err.get(112.0)
    print(f"D 113 from the octo-double state of B: Delta_full - Delta_held = {s113:+.4e}; delta_all.csv err {e113[1]:.1e} ({e113[0]}), ratio {s113 / e113[1]:.3f}")
    print(f"ratio of the shift D 113 to D 112: {s113 / s112:.3f} (#726's successive ratios fell 1.055 to 1.039); ratio to the err at D 112 was {s112 / e112[1]:.3f}")
else:
    print("no B state or no held state at D 113")
