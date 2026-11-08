#!/bin/bash
# Issue #106: the 40x79 continuation's step 21.912601 -> 23.043278 did not converge (20 Newton steps, max|F| stuck
# near 5e-8, then 1e-6, Delta 1.8e-2 off; cont/cont_40x79.log). Diagnosis: 40x79 at 23.043278 re-solved directly from
# other starts, the 32x101 and 32x81 states of I105-mac at D = 23 (rt_run.py --D_start 23.043278).
#   run_diag.sh TAG START [NEWTON_TOL]
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-abc971b3baa37717c
TAG="$1"; START="$2"; NT="${3:-1e-40}"; DS="${DS:-23.043278}"; GRID="${GRID:-40x79}"
mkdir -p "$HERE/diag"
cd "$CODE" || exit 2
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
exec nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$START" --D_start "$DS" --grids "$GRID" \
    --solver mp --tol 1e-4 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4 \
    --newton_tol "$NT" --out "$HERE/diag" --tag "$TAG"
