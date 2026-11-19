#!/bin/bash
# I1031 win2: the issue's checks on the 4.9.1 build (worktree D:\choptuik-i1031, venv-md491), BelowNormal.
# Order changed at 18:54 UTC, before this script ran, at the coordinator's note that win2b's #1033 run 3 waits for the build's memory:
# Phase A first (ref, scaled, jets and its kappa control as three chains of one BLAS thread each, like #962; small memory), then
# The cols_ cargo tests (issue step 4, bullet 1) were first planned as a phase 0 after phase A; by 18:56 UTC (this edit) the coordinator had moved them to dh610, so this script has no cargo phase.
# Each check writes NAME.log (header, command, output, last line "exit N") and a line in summary_1031.txt.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
V=/c/Users/nathan/Source/venv-md491
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-md491 PYO3_PYTHON=C:/Users/nathan/Source/venv-md491/Scripts/python.exe
export PATH="$V/Scripts:$PATH"
PY=C:/Users/nathan/Source/venv-md491/Scripts/python.exe
R=D:/choptuik-i935-raw
OUT=/d/choptuik-i935-raw/I1031-win2
SUM=$OUT/summary_1031.txt
cd /d/choptuik-i1031/hp || exit 1
stamp() { date -u '+%F %T'; }
echo "# checks1031 start $(stamp) UTC, hp $(git rev-parse HEAD)" >> $SUM
hdr() {
  echo "# $(stamp) UTC hp worktree $(git rev-parse --short HEAD), python $PY"
  echo "# hpkernel $($PY -c 'import hpkernel; print(hpkernel.__file__)')"
}
# run NAME WANT_EXIT args...   (stdout and stderr to the log)
run() {
  local name=$1 want=$2; shift 2
  { hdr; echo "# cmd: $*"; } > $OUT/$name.log
  local s=$(date +%s)
  "$PY" -u "$@" >> $OUT/$name.log 2>&1
  local rc=$?
  echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $SUM
}
J=$R/anm-mac/jets_inputs/jets_inputs.json
chain_ref()    { run ref 0 highm_check.py ref --compare=$R/T45-win/scratch/t45/diag/ref_new.json --Ms=48,64,80; }
chain_scaled() { run scaled 0 highm_check.py scaled --compare=$R/T81/scaled_main.json; }
chain_jets()   { run jets 0 highm_check.py jets --compare=$J
                 run jets_kappa 1 highm_check.py jets --compare=$J --mutate=kappa; }
chain_ref & chain_scaled & chain_jets & wait
echo "# phase A done $(stamp) UTC" >> $SUM
# The cols_ cargo tests do not run on win2: the coordinator moved them to dh610 (its hc before 18:56 UTC, "Do not touch go_cargo"), queued after its K 49 run; #1003's K 49 beside win2 cannot resume and their compile peak is unknown.
echo "# cols_ cargo tests (issue step 4, bullet 1) NOT run on win2: moved to dh610 by the coordinator (recorded 18:56 UTC)" >> $SUM
echo "# checks1031 done $(stamp) UTC" >> $SUM
touch $OUT/checks.done
