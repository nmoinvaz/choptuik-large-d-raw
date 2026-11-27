#!/bin/bash
# #1102 step 1: build ellrs (wip/ell1-rust-b12 d4b6b6ce) into SITE for the scanner's venv, the venv itself untouched; then steps 2 (the gates) if the build prints the ellrs line.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1102-dh370
WT=/home/nathan/Source/choptuik-large-d-1102/solver/matter
SITE=/home/nathan/Source/ellrs-site-1102
export VIRTUAL_ENV=/home/nathan/Source/choptuik-large-d-1058b/.venv
export PATH=$VIRTUAL_ENV/bin:$PATH
PY=$VIRTUAL_ENV/bin/python
export OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP.txt; exit 1; }
cd $WT || exit 9
[ "$(git rev-parse --short=8 HEAD)" = d4b6b6ce ] && [ -z "$(git status --short)" ] || stop "the worktree is not a clean d4b6b6ce"
step "build starts: ellrs/build.sh $SITE (cargo $(cargo --version | cut -d' ' -f2), maturin $(maturin --version | cut -d' ' -f2), python $($PY -V 2>&1 | cut -d' ' -f2))"
t0=$(date +%s)
ellrs/build.sh $SITE > $OUT/build.log 2>&1; rc=$?
step "build exit $rc, $(( $(date +%s) - t0 )) s; $(tail -1 $OUT/build.log | cut -c1-200)"
[ $rc = 0 ] && grep -q '^ellrs ' $OUT/build.log || stop "the build did not exit 0 with the ellrs line (see build.log)"
export PYTHONPATH=$SITE
$PY -c "import ellrs; print('ellrs', ellrs.isa(), ellrs.gemm(), ellrs.__file__)" > $OUT/ellrs_import.txt 2>&1
step "import: $(cat $OUT/ellrs_import.txt)"
nice -n 10 $PY -u ell_b12rs.py selftest > $OUT/selftest.log 2>&1; e0=$?
nice -n 10 $PY -u ell_b12rs.py selftest --mutate=nolam > $OUT/selftest_nolam.log 2>&1; e1=$?
nice -n 10 $PY -u ell_b12rs.py selftest --mutate=harm > $OUT/selftest_harm.log 2>&1; e2=$?
step "selftest exit $e0 (0 wanted); --mutate=nolam exit $e1, --mutate=harm exit $e2 (1 wanted each)"
[ $e0 = 0 ] && [ $e1 = 1 ] && [ $e2 = 1 ] || stop "a selftest or a mutation did not read as written"
t1=$(date +%s)
nice -n 10 $PY -u ell_b12rs.py check $OUT/in/l1kc31r1025.jsonl $OUT/in/sol_l1kc31r1025_D10.5000.npy 10.5 2.87 --threads=4 --controls=1 --out=$OUT/check_kc31.jsonl > $OUT/check_kc31.log 2>&1; ec=$?
step "k_c 31 check exit $ec (0 wanted), $(( $(date +%s) - t1 )) s; $(grep -E 'bit for bit' $OUT/check_kc31.log | head -3 | tr '\n' '|' | cut -c1-300)"
[ $ec = 0 ] || stop "the k_c 31 gate exit $ec"
echo "GATES DONE $(stamp) UTC" > $OUT/GATES_DONE.txt
exit 0
}
