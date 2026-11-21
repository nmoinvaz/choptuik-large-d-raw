"""#1013 recount4 (rpi5): dh610's fu_value.py at xi1 0.18 with recount3's settings. fu_value.py beside this file is
I1021-dh610/b21-25-fu/fu_value.py at raw 18338ce4, byte for byte (sha256 in SHA256SUMS). Only R1 and VARIANTS change.
The tests (decide, has_value), the point selection (--auto), --append, --retest and --selftest are fu_value.py's.
    python fu_value018.py CODE CACHE ROWS.jsonl --auto LEAVES [--procs 4] [--append]
    python fu_value018.py CODE CACHE ROWS.jsonl --retest PREV_ROWS.jsonl --mutate f3|lowguard
    python fu_value018.py CODE --selftest [--break]"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fu_value as fv  # noqa: E402

fv.R1 = 0.18
fv.VARIANTS = [                                     # name, bounds beyond wall 3600 and noise cap 1e7, starts, seed rank
    ("default", dict(rhs=1e7), [0.2, 0.25], 0),     # recount3's own: --m3starts=0.2,0.25 --m3maxrhs=1e7, nearest seed
    ("s0.25", dict(rhs=1e7), [0.25, 0.2], 0),       # dh610's s0.2 with recount3's order reversed
    ("seed2", dict(rhs=1e7), [0.2, 0.25], 1),
    ("seed3", dict(rhs=1e7), [0.2, 0.25], 2),
    ("s0.25seed2", dict(rhs=1e7), [0.25, 0.2], 1),
]

if __name__ == "__main__":
    sys.exit(fv.main())
