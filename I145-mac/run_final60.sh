#!/bin/bash
# Issue #145, the end at D = 60.001952: once the 32x101 continuation has saved that state, stop it, then run in
# parallel the coefficient mutation (run_coef.sh) and the 32x121 re-solve, then the second 32x101 root from the
# 32x121 root. Two processes at most.
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5b009d60d38d2338
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
ST="$HERE/cont/cont_32x101_D60.0020_32x101.npz"
until [ -e "$ST" ] && [ $(( $(date +%s) - $(stat -f %m "$ST") )) -ge 10 ]; do sleep 15; done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC the D 60.0020 state exists; stopping the continuation"
pkill -f "solver/rt/rt_run.py --start $HERE/cont/cont_32x101_D56.0000_32x101.npz"
sleep 5
OPTS="--solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4 --newton_tol 1e-36"
cd "$CODE" || exit 2
"$HERE/run_coef.sh" D60.0020 > "$HERE/controls/coef_D60.0020.stdout" 2>&1 &
nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$ST" --grids 32x121 $OPTS --out "$HERE/fol" \
    --tag fol_32x121
echo "== exit $? fol_32x121 D60.0020"
touch "$HERE/fol/done_fol_32x121_D60.0020"
nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$HERE/fol/fol_32x121_D60.0020_32x121.npz" \
    --grids 32x101 $OPTS --out "$HERE/fol" --tag from121_32x101
echo "== exit $? from121_32x101 D60.0020"
touch "$HERE/fol/done_from121_32x101_D60.0020"
wait
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC done"
