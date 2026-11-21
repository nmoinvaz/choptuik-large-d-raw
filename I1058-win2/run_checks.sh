#!/bin/bash
# I1058 step 2 on the new build (worktree D:\choptuik-i1058b, venv-i1058b), BelowNormal: the issue's four commands (ref against T81/ref_main.json, scaled, jets, jets --mutate=kappa) and, as information, ref against win2's own Windows reference T45-win/.../ref_new.json,
# as three chains of one BLAS thread each. Each check writes NAME.log (header, command, output, last line "exit N") and a line in summary_1058.txt. Caps: three times the #1034 run's seconds, at least 600 s.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
OUT=/d/choptuik-i935-raw/I1058-win2
. $OUT/lib1058.sh
V=/c/Users/nathan/Source/venv-i1058b
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1058b PYO3_PYTHON=C:/Users/nathan/Source/venv-i1058b/Scripts/python.exe
export PATH="$V/Scripts:$PATH"
PY=C:/Users/nathan/Source/venv-i1058b/Scripts/python.exe
R=D:/choptuik-i935-raw
cd /d/choptuik-i1058b/hp || exit 1
stamp() { date -u '+%F %T'; }
echo "# checks1058 (step 5) start $(stamp) UTC, hp $(git rev-parse HEAD)" >> $SUM
# run NAME WANT CAP args...
run() {
  local name=$1 want=$2 cap=$3; shift 3
  { echo "# $(stamp) UTC hp worktree $(git rev-parse --short HEAD), python $PY"
    echo "# hpkernel $($PY -c 'import hpkernel; print(hpkernel.__file__)')"
    echo "# cmd: $*"; } > $OUT/$name.log
  local s=$(date +%s)
  crun "$name" $want $cap highm_check.py "$PY" -u "$@" >> $OUT/$name.log 2>&1
  echo "exit $RC" >> $OUT/$name.log
  echo "$name: expected exit $want, got $RC, $(( $(date +%s) - s )) s capped $CAPPED $([ $RC = $want ] && echo OK || echo MISMATCH)" >> $SUM
}
J=$R/anm-mac/jets_inputs/jets_inputs.json
chain_ref()    { run ref_t45 0 600 highm_check.py ref --compare=$R/T45-win/scratch/t45/diag/ref_new.json --Ms=48,64,80
                 run ref_t81 0 600 highm_check.py ref --compare=$R/T81/ref_main.json --Ms=48,64,80; }
chain_scaled() { run scaled 0 1800 highm_check.py scaled --compare=$R/T81/scaled_main.json; }
chain_jets()   { run jets 0 600 highm_check.py jets --compare=$J
                 run jets_kappa 1 600 highm_check.py jets --compare=$J --mutate=kappa; }
chain_ref & chain_scaled & chain_jets & wait
echo "# step 5 done $(stamp) UTC" >> $SUM
touch $OUT/checks.done
