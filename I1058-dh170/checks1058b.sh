#!/bin/bash
# #1058 on dh170: the stored-reference checks of the issue on the second build (hp worktree 8179068d, its venv). One after another, 6 threads where a check takes them, nice 10.
# Each writes NAME.log (first lines: hpkernel.__file__, the .so's crate strings, the command; last: exit N) and a line in summary_1058.txt. usage: bash checks1058.sh
OUT=/home/nathan/Source/choptuik-large-d-raw/I1058-dh170
WT=/home/nathan/Source/choptuik-large-d-1058b
R=/home/nathan/scratch1058/raw
PD=$WT/.venv/bin/python
SUM=$OUT/summary_1058.txt
cd "$WT/hp" || exit 1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
stamp() { date -u '+%F %T'; }
run() {   # name, expected exit, command...
  local name=$1 want=$2; shift 2
  local so=$($PD -c 'import hpkernel,os; print(os.path.dirname(hpkernel.__file__))')/*.so
  { echo "# $(stamp) UTC hp worktree $(git -C $WT rev-parse --short HEAD), python $PD"
    echo "# hpkernel $($PD -c 'import hpkernel; print(hpkernel.__file__)')"
    echo "# crate strings in the .so: $(strings -n 8 $so 2>/dev/null | grep -oE '(multidouble|multishoot|multisolver)[-/][0-9][^/ ]*' | sort -u | head -12 | tr '\n' ' ')"
    echo "# cmd: $*"; } > $OUT/$name.log
  local s=$(date +%s)
  nice -n 10 "$PD" "$@" >> $OUT/$name.log 2>&1; local rc=$?
  echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH); $(grep -E '^(PASS|FAIL)' $OUT/$name.log | tail -n 1)" >> $SUM
}
: > $SUM
echo "# checks1058b start $(stamp) UTC, raw commit $(cat /home/nathan/scratch1058/raw_commit.txt)" >> $SUM
run ref 0 highm_check.py ref --compare=$R/T81/ref_main.json --Ms=48,64,80
run scaled 0 highm_check.py scaled --compare=$R/T81/scaled_main.json
run jets 0 highm_check.py jets --compare=$R/anm-mac/jets_inputs/jets_inputs.json
run jets_kappa 1 highm_check.py jets --compare=$R/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa
echo "# checks1058b end $(stamp) UTC" >> $SUM
