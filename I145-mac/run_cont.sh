#!/bin/bash
# The continuations of issue #145: rt_run.py --solver mp on 32 x N from D = 30, steps of 1, quadratic predictor.
#   run_cont.sh N START PREV1,PREV2[,...] TAG [D_TO] [PRED_ORDER]
# START and PREV are rt_run.py states (any grid; resampled to 32 x N). Output in cont/ beside this script.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5b009d60d38d2338
N="$1"; START="$2"; PREV="$3"; TAG="$4"; DTO="${5:-100}"; ORDER="${6:-2}"
EXTRA=34.993266,40.020065,44.963411,50.007491,54.996085,60.001952,64.994829
CHECK="$EXTRA",70,75,80,85,90,95,100
mkdir -p "$HERE/cont"
cd "$CODE" || exit 2
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
exec nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$START" --start_prev "$PREV" \
    --grids "32x$N" --solver mp --D_to "$DTO" --dD 1 --pred_order "$ORDER" --D_extra "$EXTRA" --extras_off_path \
    --check_D "$CHECK" --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --out "$HERE/cont" --tag "$TAG"
