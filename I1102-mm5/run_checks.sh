#!/bin/bash
# #1102 (mm5): the order's four checks, one after the other, from ~/Source/choptuik-ellrs/solver/matter; exits in checks.txt
{
H=$HOME/Source/choptuik-large-d-raw/I1102-mm5
cd $HOME/Source/choptuik-ellrs/solver/matter || exit 1
export OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
PY=$HOME/venv-314/bin/python
: > $H/checks.txt
run() { name=$1; shift; t0=$(date +%s); echo "start $name $(date -u '+%H:%M:%S UTC')" >> $H/checks.txt; $PY -u ell_b12rs.py "$@" > $H/$name.log 2>&1; rc=$?; echo "$name exit $rc $(( $(date +%s) - t0 )) s" >> $H/checks.txt; }
run selftest selftest
run selftest_nolam selftest --mutate=nolam
run selftest_harm selftest --mutate=harm
run check check $H/in/l1kc31r1025.jsonl $H/in/sol_l1kc31r1025_D10.5000.npy 10.5 2.87 --threads=2 --controls=1
echo "done $(date -u '+%H:%M:%S UTC')" >> $H/checks.txt
exit
}
