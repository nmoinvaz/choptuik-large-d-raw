#!/bin/bash
# Issue #145: is each grid's root at D = 40.020065 determined? Re-solve it from a state of another grid, resampled.
#   101 from the 121 follower state, 121 from the 32x141 state (fol_32x141), then compare with the first roots.
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5b009d60d38d2338
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
cd "$CODE" || exit 2
OPTS="--solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4"
nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$HERE/fol/fol_32x121_D40.0201_32x121.npz" \
    --grids 32x101 $OPTS --out "$HERE/controls" --tag from121_32x101
echo "== exit $? from121_32x101"
nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$HERE/fol/fol_32x141_D40.0201_32x141.npz" \
    --grids 32x121 $OPTS --out "$HERE/controls" --tag from141_32x121
echo "== exit $? from141_32x121"
