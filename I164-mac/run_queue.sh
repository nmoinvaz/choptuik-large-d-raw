#!/bin/bash
# Issue #164: what one worker runs after its main runs (run_main.sh), by the criteria of README.md. The D 60 results
# of the main runs gave min E = 6.4e-13 (32x95) and E not monotone (E(95) < E(101) = 2.33e-12), so 87, 89, 93 and 97
# run at both D from both starts (93 and 97 first, beside the best grid). Then worker a re-solves start a on 48x95 at
# D 60 (time resolution of the best grid), and worker b runs the coefficient mutation on 32x91 at D 60.
#   run_queue.sh a|b
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3f8a38336503b3e7
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
until grep -q "UTC done" "$HERE/main_$1.stdout"; do sleep 15; done
"$HERE/run_main.sh" "$1" "32x93 32x97 32x89 32x87"
if [ "$1" = a ]; then
    "$HERE/run_main.sh" a "48x95" D60.0020
else
    mkdir -p "$HERE/controls"
    cd "$CODE" || exit 2
    echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC coef_32x91 D60.0020"
    nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$HERE/roots/a101_32x91_D60.0020_32x91.npz" \
        --grids 32x91 --solver mp --tol 1e-12 --mutate=coef --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 \
        --full_below 1e-4 --newton_tol 1e-36 --out "$HERE/controls" --tag coef_32x91
    echo "== exit $? coef_32x91 D60.0020"
fi
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC queue done"
