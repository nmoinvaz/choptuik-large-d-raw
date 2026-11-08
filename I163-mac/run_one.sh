#!/bin/bash
# Issue #163: one RT solve with #145's options, from a state resampled to a grid, at the state's D.
#   run_one.sh OUTDIR TAG START GRID K [extra rt_run.py options...]
# K is --horizon (0: the collocation of #145 and #164). Newton's target is 1e-40 below D 54, 1e-38 at 54.996085 and
# 1e-36 at 60.001952, as in #145 and #164.
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-aed8a75ee3273b565
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
cd "$CODE" || exit 2
OUT=$1; TAG=$2; ST=$3; G=$4; K=$5
shift 5
case "$ST" in
    *D60.0020*) NTOL=1e-36 ;;
    *D54.9961*) NTOL=1e-38 ;;
    *) NTOL=1e-40 ;;
esac
OPTS="--solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4"
mkdir -p "$HERE/$OUT"
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC $TAG $G K $K from $ST (code $(git rev-parse --short HEAD))"
nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$ST" --grids "$G" $OPTS --newton_tol $NTOL \
    --horizon "$K" --out "$HERE/$OUT" --tag "$TAG" "$@"
rc=$?
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC exit $rc $TAG"
exit $rc
