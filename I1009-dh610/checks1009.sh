#!/bin/bash
# #1009 step 4 on dh610: the bit checks on the new build (worktree -ccc, venv-ccc), each with its control; each line's exit is logged to summary_checks.txt.
# 1. cargo test --profile release-dev --lib cols_ (the control COLS_MUT_ULP must fire inside it)
# 2. highm_check ref --compare=T81/ref_main.json --Ms=48,64,80
# 3. highm_check scaled --compare=T81/scaled_main.json
# 4. highm_check jets --compare=anm-mac/jets_inputs/jets_inputs.json, and its control --mutate=kappa (must exit 1)
# Expected exits: 0 0 0 0 1. Threads: highm_check's own default; nice 10, beside the K 49 run.
. "$(dirname "$0")/common1009.sh"
export CARGO_BUILD_JOBS=6 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
SUM=$OUT/summary_checks.txt
. $VENV/bin/activate
cd "$WT/hp" || exit 1
echo "# $(stamp) UTC checks start, hp $(git rev-parse --short=8 HEAD), hpkernel $(python -c 'import hpkernel; print(hpkernel.__file__)'), load $(cut -d' ' -f1-3 /proc/loadavg)" > $SUM
run() { local name=$1 want=$2; shift 2; { echo "# $(stamp) UTC cmd: $*"; } > $OUT/$name.log; local s=$(date +%s); nice -n 10 "$@" >> $OUT/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $SUM; }
run cols_test 0 cargo test --profile release-dev --lib cols_ -- --nocapture
run highm_ref 0 python3 highm_check.py ref --compare=$R/T81/ref_main.json --Ms=48,64,80
run highm_scaled 0 python3 highm_check.py scaled --compare=$R/T81/scaled_main.json
run highm_jets 0 python3 highm_check.py jets --compare=$R/anm-mac/jets_inputs/jets_inputs.json
run highm_jets_kappa 1 python3 highm_check.py jets --compare=$R/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa
echo "# $(stamp) UTC checks done" >> $SUM
