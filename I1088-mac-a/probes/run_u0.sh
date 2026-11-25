#!/bin/bash
# u0_tolerance.py and slave_test.py after run_o (the octo-double block LU), into their logs here.
# Args: STATE (anm_pin3_D245.5586.npz), GUESS (g250/guess_D250.npz), CODE (the choptuik-large-d worktree), SITE.
{
set -u
STATE=$1; GUESS=$2; CODE=$3; SITE=$4; HERE=$(cd "$(dirname "$0")" && pwd)
cd "$CODE/hp" || exit 1
export PYTHONPATH=$SITE OPENBLAS_NUM_THREADS=2
PY=/Users/nathan/venv-314/bin/python
date -u '+start %Y-%m-%d %H:%M:%S UTC'
nice -n 10 $PY -u "$HERE/slave_test.py" "$STATE" "$GUESS" > "$HERE/slave_test.log" 2>&1
nice -n 10 $PY -u "$HERE/slave_test.py" "$STATE" --mutate=sign > "$HERE/slave_test_mutate_sign.log" 2>&1
nice -n 10 $PY -u "$HERE/u0_tolerance.py" "$STATE" 1e-24,1e-20,1e-16,1e-12 > "$HERE/u0_tolerance.log" 2>&1
date -u '+end %Y-%m-%d %H:%M:%S UTC'
exit
}
