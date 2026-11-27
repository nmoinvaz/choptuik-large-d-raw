#!/bin/bash
# #1102 step 3: ell_b12rs.py check on winb's accepted k_c 127 D 23.0 state at lambda 0.046, DDEll against Rust in one process, nice 19, Rust with --threads 4, OPENBLAS_NUM_THREADS=1.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1102-dh370
WT=/home/nathan/Source/choptuik-large-d-1102/solver/matter
SITE=/home/nathan/Source/ellrs-site-1102
export VIRTUAL_ENV=/home/nathan/Source/choptuik-large-d-1058b/.venv
PY=$VIRTUAL_ENV/bin/python
export PYTHONPATH=$SITE OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WT || exit 9
[ "$(blob $OUT/in/sol_l1kc127wind23_D23.0000.npy)" = 7a1b150c ] && [ "$(blob $OUT/in/l1kc127wind23.jsonl)" = eea03461 ] && [ -e $OUT/GATES_DONE.txt ] || { step "STOP: the k_c 127 state or record is not the pinned blob, or the gates are not done"; exit 1; }
step "k_c 127 check starts: lambda 0.046, D 23.0, Rust --threads=4, DDEll 1 thread, nice 19, one process; state 7a1b150c, record eea03461"
t0=$(date +%s)
nice -n 19 /usr/bin/time -v $PY -u ell_b12rs.py check $OUT/in/l1kc127wind23.jsonl $OUT/in/sol_l1kc127wind23_D23.0000.npy 23.0 0.046 --threads=4 --out=$OUT/check_kc127.jsonl > $OUT/check_kc127.log 2>&1; rc=$?
step "k_c 127 check exit $rc, $(( $(date +%s) - t0 )) s; $(grep -E 'bit for bit' $OUT/check_kc127.log | head -2 | tr '\n' '|' | cut -c1-400)"
grep -hE 'Elapsed|Maximum resident' $OUT/check_kc127.log >> $OUT/steps.txt
echo "KC127 DONE exit $rc $(stamp) UTC" > $OUT/KC127_DONE.txt
exit 0
}
