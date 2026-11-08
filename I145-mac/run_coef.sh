#!/bin/bash
# Issue #145: the coefficient mutation (rt_run.py --mutate=coef: the coefficient (D - 3)(D - 2)/2 of Omega_3 scaled by
# 1 + 1e-3) from the unmutated 32x101 state at a check D. It must move Delta by more than 1e-6 and exit 1.
#   run_coef.sh DTAG    (D54.9961 or D60.0020)
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5b009d60d38d2338
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
cd "$CODE" || exit 2
while pgrep -f "tag from141_32x121" >/dev/null; do sleep 10; done
nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$HERE/cont/cont_32x101_$1_32x101.npz" \
    --grids 32x101 --solver mp --tol 1e-12 --mutate=coef --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 \
    --full_below 1e-4 --newton_tol 1e-36 --out "$HERE/controls" --tag "coef_$1"
echo "== exit $? coef $1"
