#!/bin/bash
# #1079 macm3b step 2 (checks): certify_M_sys.py selftest (+ --mutate=coupling), certify_M.py startcheck 3 (+ --mutate), crosscheck 3 (+ --mutate), from main's solver/proof (worktree ~/Source/choptuik-large-d-1079 at a4cd5eaa),
# 1 process, nice 10, 1 thread per BLAS. Each expected exit is checked; a mismatch writes STOP and ends. Logs in solver/proof/logs/I1079_*.log, records in $P/steps.txt.
{
P=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3
W=/Users/nathan/Source/choptuik-large-d-1079
MAIN=a4cd5eaa7b297ffc6f171551fa15ba054e970e21
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
H=$P/steps.txt
stamp() { date -u '+%F %T'; }
[ "$(git -C $W rev-parse HEAD)" = "$MAIN" ] && [ -z "$(git -C $W status --porcelain --untracked-files=no)" ] || { echo "$(stamp) STOP: the main worktree is not at $MAIN or has tracked changes" >> $H; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $W/solver/proof || exit 1
mkdir -p logs data
run() {   # run NAME EXPECTED CMD...: the command's output to logs/I1079_NAME.log, its exit checked against EXPECTED (0 or nonzero)
    local name=$1 exp=$2; shift 2
    echo "checks $name command: cd $W/solver/proof && nice -n 10 $PY $* > logs/I1079_$name.log 2>&1" >> $H
    echo "checks $name start $(stamp)" >> $H
    nice -n 10 $PY "$@" > logs/I1079_$name.log 2>&1; local rc=$?
    echo "checks $name end $(stamp) exit $rc (expected $exp): $(tail -1 logs/I1079_$name.log | cut -c1-200)" >> $H
    if { [ "$exp" = 0 ] && [ $rc != 0 ]; } || { [ "$exp" = nonzero ] && [ $rc = 0 ]; }; then echo "$(stamp) STOP: $name exit $rc, expected $exp" >> $H; exit 1; fi
}
echo "checks start $(stamp): python-flint $($PY -c 'import flint; print(flint.__version__, "FLINT", flint.__FLINT_VERSION__)')" >> $H
run selftest 0 certify_M_sys.py selftest
run selftest_mut nonzero certify_M_sys.py selftest --mutate=coupling
run startcheck 0 certify_M.py startcheck 3
run startcheck_mut nonzero certify_M.py startcheck 3 --mutate
run crosscheck 0 certify_M.py crosscheck 3
run crosscheck_mut nonzero certify_M.py crosscheck 3 --mutate
echo "checks done $(stamp)" >> $H
exit 0
}
