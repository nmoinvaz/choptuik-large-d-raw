#!/bin/bash
# Issue #164: additions after the D 60 results of 93 and 97, outside the criteria's verdict (README.md, What ran).
# 32x95 is the only grid within 1e-12 at D 60, and its neighbours 93 and 97 lie on the other side of hp (+2.4e-12 to
# +2.8e-12 and +8e-14 to +1.1e-12). So: 32x99 at D 60 from both starts (the window between 97 and 101), and 32x95 at
# D 60 from two further starts, the start-b roots of 32x97 and 32x93 resampled (is 95's root the same from there?).
#   run_extra.sh a|b
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3f8a38336503b3e7
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
until grep -q "queue done" "$HERE/queue_$1.stdout"; do sleep 15; done
"$HERE/run_main.sh" "$1" "32x99" D60.0020
if [ "$1" = a ]; then SRC=32x97; TAG=c97; else SRC=32x93; TAG=d93; fi
cd "$CODE" || exit 2
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC ${TAG}_32x95 D60.0020"
nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$HERE/roots/b121_${SRC}_D60.0020_$SRC.npz" \
    --grids 32x95 --solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4 \
    --newton_tol 1e-36 --out "$HERE/roots" --tag "${TAG}_32x95"
echo "== exit $? ${TAG}_32x95 D60.0020"
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC extra done"
