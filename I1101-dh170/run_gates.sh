#!/bin/bash
# #1101 dh170 step 1 (t5's order, comment 7212323177): build ellrs (wip/ell1-rust-b12 d4b6b6ce) into SITE for the scanner's venv, the venv untouched;
# then the gates: ell_b12rs.py selftest 0, --mutate=nolam 1, --mutate=harm 1, and the k_c 31 check (15010 of 15010, both controls FAIL). Stops at the first failure (STOP.txt).
{
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1101-dh170
WT=/home/nathan/Source/choptuik-large-d-1102/solver/matter
SITE=/home/nathan/Source/ellrs-site-1102
export VIRTUAL_ENV=/home/nathan/Source/choptuik-large-d-1058b/.venv
export PATH=$VIRTUAL_ENV/bin:$PATH
PY=$VIRTUAL_ENV/bin/python
export OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP.txt; exit 1; }
mkdir -p $OUT/gates
cd $WT || exit 9
[ "$(git rev-parse --short=8 HEAD)" = d4b6b6ce ] && [ -z "$(git status --short)" ] || stop "the worktree is not a clean d4b6b6ce"
[ "$(blob d18_secant.py)" = 9706e506 ] && [ "$(blob ell_b12rs.py)" = a1fff74f ] || stop "d18_secant.py or ell_b12rs.py is not the pinned blob"
[ "$(blob $OUT/in/sol_l1kc31r1025_D10.5000.npy)" = f07a8984 ] && [ "$(blob $OUT/in/l1kc31r1025.jsonl)" = e5a87ec5 ] || stop "the k_c 31 inputs are not the pinned blobs"
step "gates pins ok: worktree d4b6b6ce clean, d18_secant.py 9706e506, ell_b12rs.py a1fff74f, k_c 31 state f07a8984 record e5a87ec5"
step "build starts: ellrs/build.sh $SITE (cargo $(cargo --version | cut -d' ' -f2), maturin $(maturin --version | cut -d' ' -f2), python $($PY -V 2>&1 | cut -d' ' -f2))"
t0=$(date +%s)
ellrs/build.sh $SITE > $OUT/gates/build.log 2>&1; rc=$?
step "build exit $rc, $(( $(date +%s) - t0 )) s; $(tail -1 $OUT/gates/build.log | cut -c1-200)"
[ $rc = 0 ] && grep -q '^ellrs ' $OUT/gates/build.log || stop "the build did not exit 0 with the ellrs line (gates/build.log)"
export PYTHONPATH=$SITE
$PY -c "import ellrs; print('ellrs', ellrs.isa(), ellrs.gemm(), ellrs.__file__)" > $OUT/gates/ellrs_import.txt 2>&1
step "import: $(cat $OUT/gates/ellrs_import.txt)"
nice -n 10 $PY -u ell_b12rs.py selftest > $OUT/gates/selftest.log 2>&1; e0=$?
nice -n 10 $PY -u ell_b12rs.py selftest --mutate=nolam > $OUT/gates/selftest_nolam.log 2>&1; e1=$?
nice -n 10 $PY -u ell_b12rs.py selftest --mutate=harm > $OUT/gates/selftest_harm.log 2>&1; e2=$?
step "ell_b12rs selftest exit $e0 (0 wanted); --mutate=nolam exit $e1, --mutate=harm exit $e2 (1 wanted each)"
[ $e0 = 0 ] && [ $e1 = 1 ] && [ $e2 = 1 ] || stop "a selftest or a mutation did not read as written"
t1=$(date +%s)
nice -n 10 $PY -u ell_b12rs.py check $OUT/in/l1kc31r1025.jsonl $OUT/in/sol_l1kc31r1025_D10.5000.npy 10.5 2.87 --threads=2 --controls=1 --out=$OUT/gates/check_kc31.jsonl > $OUT/gates/check_kc31.log 2>&1; ec=$?
step "k_c 31 check exit $ec (0 wanted), $(( $(date +%s) - t1 )) s; $(grep -E 'bit for bit' $OUT/gates/check_kc31.log | head -3 | tr '\n' '|' | cut -c1-400)"
[ $ec = 0 ] || stop "the k_c 31 gate exit $ec"
grep -q '15010 of 15010 entries bit for bit' $OUT/gates/check_kc31.log || stop "the k_c 31 check did not print 15010 of 15010"
[ "$(grep -E 'control (nolam|harm)' $OUT/gates/check_kc31.log | grep -c FAIL)" = 2 ] || stop "a control did not FAIL"
echo "GATES DONE $(stamp) UTC" > $OUT/GATES_DONE.txt
step "gates done"
exit 0
}
