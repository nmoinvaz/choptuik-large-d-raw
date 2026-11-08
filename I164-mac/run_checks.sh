#!/bin/bash
# Issue #164: the checks on the finished roots (criteria in README.md). For each grid: the verdict at D 60.001952
# (rt_grids.py on the roots from starts a and b, --tol 1e-12), the table at both D (--table, outside the verdict),
# and rt_roots.py on each pair of roots. Controls: --mutate=shift on 32x95 at D 60 and rt_roots.py --mutate=same.
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3f8a38336503b3e7
PY=/Users/nathan/venv-qd/bin/python
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
cd "$CODE" || exit 2
R="$HERE/roots"
mkdir -p "$HERE/fit"
for N in ${GRIDS:-85 87 89 91 93 95 97}; do
    A="$R/a101_32x$N.jsonl"; B="$R/b121_32x$N.jsonl"
    $PY solver/rt/rt_grids.py "$A" "$B" --D 60.001952 --tol 1e-12 > "$HERE/fit/verdict_32x$N.log" 2>&1
    echo "== exit $? verdict 32x$N D 60.001952"
    $PY solver/rt/rt_grids.py "$A" "$B" --D 54.996085,60.001952 --tol 1e-12 --table > "$HERE/fit/table_32x$N.log" 2>&1
    echo "== exit $? table 32x$N D 54.996085,60.001952"
    for DTAG in D60.0020 D54.9961; do
        nice -n 10 $PY solver/rt/rt_roots.py "$R/a101_32x${N}_${DTAG}_32x$N.npz" "$R/b121_32x${N}_${DTAG}_32x$N.npz" \
            > "$HERE/fit/roots_32x${N}_$DTAG.log" 2>&1
        echo "== exit $? roots 32x$N $DTAG"
    done
done
$PY solver/rt/rt_grids.py "$R/a101_32x95.jsonl" "$R/b121_32x95.jsonl" --D 60.001952 --tol 1e-12 --mutate=shift \
    > "$HERE/fit/verdict_32x95_mutate_shift.log" 2>&1
echo "== exit $? verdict 32x95 --mutate=shift (must be 1)"
nice -n 10 $PY solver/rt/rt_roots.py "$R/a101_32x95_D60.0020_32x95.npz" "$R/b121_32x95_D60.0020_32x95.npz" \
    --mutate=same > "$HERE/fit/roots_32x95_D60.0020_mutate_same.log" 2>&1
echo "== exit $? roots 32x95 D60.0020 --mutate=same (must be 1)"
