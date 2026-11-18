#!/bin/bash
# #954: A's jets compare and its kappa control, repeated: the first pass (checksA.sh) ran with only jets_inputs.json in R, so that M 32's input was "own" (this machine's resample) and not the stored one
# ("input own" in A_jets.log, 12 of 28 outputs differing at M 32); my setup omitted the other files of anm-mac/jets_inputs, now extracted into R. The A_jets_save and the B and C checks run after the extraction.
. "$(dirname "$0")/common954.sh"
WT=/home/nathan/Source/choptuik-large-d-954a
SUM=$OUT/summary_E.txt
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
so=$(python -c 'import hpkernel,os; print(os.path.dirname(hpkernel.__file__))')/*.so
hdr() { echo "# $(stamp) UTC build A, hp $(git -C $WT rev-parse --short HEAD), hpkernel $(python -c 'import hpkernel; print(hpkernel.__file__)')"; echo "# multidouble in the .so: $(strings -n 8 $so 2>/dev/null | grep -oE 'multidouble[-/][^/ ]+' | sort -u | head -3 | tr '\n' ' ')"; }
run() { local name=$1 want=$2; shift 2; { hdr; echo "# cmd: $*"; } > $OUT/$name.log; local s=$(date +%s); nice -n 10 "$@" >> $OUT/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $SUM; }
: > $SUM
run A_jets_rerun 0 python highm_check.py jets --compare=$R/anm-mac/jets_inputs/jets_inputs.json
run A_jets_kappa_rerun 1 python highm_check.py jets --compare=$R/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa
echo "# checksE done $(stamp) UTC" >> $SUM
