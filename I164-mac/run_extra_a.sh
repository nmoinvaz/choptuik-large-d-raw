#!/bin/bash
# Issue #164: worker a's part of run_extra.sh (32x99 from start a, then 32x95 from the start-b root of 32x97), moved to
# start when worker a's queue is done, since its 48x95 solve took longer than the others (up to 20 Newton steps).
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3f8a38336503b3e7
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
until grep -q "queue done" "$HERE/queue_a.stdout"; do sleep 15; done
"$HERE/run_main.sh" a "32x99" D60.0020
cd "$CODE" || exit 2
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC c97_32x95 D60.0020"
nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$HERE/roots/b121_32x97_D60.0020_32x97.npz" \
    --grids 32x95 --solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4 \
    --newton_tol 1e-36 --out "$HERE/roots" --tag c97_32x95
echo "== exit $? c97_32x95 D60.0020"
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC extra done"
