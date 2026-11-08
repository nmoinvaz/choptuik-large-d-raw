#!/bin/bash
# Issue #164: the c97 part of run_checks.sh again, after roots/c97_32x95 finished (run_checks.sh reached it first).
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3f8a38336503b3e7
PY=/Users/nathan/venv-qd/bin/python
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
cd "$CODE" || exit 2
R="$HERE/roots"
$PY solver/rt/rt_grids.py "$R/a101_32x95.jsonl" "$R/c97_32x95.jsonl" --D 60.001952 --tol 1e-12 \
    > "$HERE/fit/verdict_32x95_a_c97.log" 2>&1
echo "== exit $? verdict 32x95 a and c97 D 60.001952"
nice -n 10 $PY solver/rt/rt_roots.py "$R/a101_32x95_D60.0020_32x95.npz" "$R/c97_32x95_D60.0020_32x95.npz" \
    > "$HERE/fit/roots_32x95_D60.0020_a_c97.log" 2>&1
echo "== exit $? roots 32x95 a and c97 D60.0020"
