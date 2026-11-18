#!/bin/bash
# #962 on win2: the checks of the issue on the 40f4b4a5 build (worktree D:\choptuik-i962, venv-i962), 4 threads at
# BelowNormal. Phase A runs ref, scaled and jets (then its kappa control) as three chains of one BLAS thread each;
# phase B runs octo_hashes --threads 4, phase C jet_by_order_check --threads 4, so at most 4 threads are busy.
# Each check writes NAME.log (header, command, output, last line "exit N") and a line in summary_962.txt.
# R is the raw worktree beside this folder; its four inputs are sha256-identical to the live clone's (input_sha256.txt).
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=C:/Users/nathan/Source/venv-i962/Scripts/python.exe
R=D:/choptuik-i935-raw
OUT=/d/choptuik-i935-raw/I962-win2
ST=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz
SUM=$OUT/summary_962.txt
cd /d/choptuik-i962/hp || exit 1
stamp() { date -u '+%F %T'; }
hdr() {
  echo "# $(stamp) UTC hp worktree $(git rev-parse --short HEAD), python $PY"
  echo "# hpkernel $($PY -c 'import hpkernel; print(hpkernel.__file__)')"
}
# run NAME WANT_EXIT [OUTFILE|-] args...   (OUTFILE: stdout of the script goes there, stderr to the log)
run() {
  local name=$1 want=$2 f=$3; shift 3
  { hdr; echo "# cmd: $*${f:+ > $f}"; } > $OUT/$name.log
  local s=$(date +%s)
  if [ "$f" = "-" ]; then "$PY" -u "$@" >> $OUT/$name.log 2>&1
  else "$PY" -u "$@" > $OUT/$f 2>> $OUT/$name.log; fi
  local rc=$?
  echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $SUM
}
J=$R/anm-mac/jets_inputs/jets_inputs.json
chain_ref()    { run ref 0 - highm_check.py ref --compare=$R/T45-win/scratch/t45/diag/ref_new.json --Ms=48,64,80; }
chain_scaled() { run scaled 0 - highm_check.py scaled --compare=$R/T81/scaled_main.json; }
chain_jets()   { run jets 0 - highm_check.py jets --compare=$J
                 run jets_kappa 1 - highm_check.py jets --compare=$J --mutate=kappa; }
echo "# checks962 start $(stamp) UTC, hp $(git rev-parse HEAD)" > $SUM
chain_ref & chain_scaled & chain_jets & wait
echo "# phase A done $(stamp) UTC" >> $SUM
run octo_ST 0 octo_win2_ST.txt octo_hashes.py $R $ST --threads 4 --N 6
echo "# phase B done $(stamp) UTC" >> $SUM
run jet_by_order 0 - jet_by_order_check.py $R $ST --threads 4 --N 6 --Np 6
echo "# checks962 done $(stamp) UTC" >> $SUM
# check 2's diffs: win2's 4.9.0 hashes against dh170's 4.9.0 (build D) and 4.8.2 (build A) hashes of the same state
cd $OUT || exit 1
for b in D A; do
  diff octo_win2_ST.txt ../I958-dh170/octo_${b}_ST.txt > diff_win2_dh170${b}_ST.txt
  echo "diff win2 vs dh170 build $b ST: exit $? ($(grep -c '^<' diff_win2_dh170${b}_ST.txt) lines differ of $(wc -l < octo_win2_ST.txt))" >> $SUM
done
touch checks.done
