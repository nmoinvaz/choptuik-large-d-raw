#!/bin/bash
# #954 (the coordinator's amendment of 04:07 UTC): octo_corrector.py planted can raise StartNotProjected past the projection onset or stall in its quad-double stage (QUAD_DOUBLE 13.28). Always: the
# full planted at ST on A (B's was in checksB.sh), so that A and B can be compared line by line. If either planted at ST raised StartNotProjected or exited non-zero: A and B alike, planted --qd 0 at ST,
# the full planted at T129-win2/chain/anm_pin3_D180.5246.npz (T129) and its --mutate 10 control. The comparison that counts is A against B, line by line (iteration lines and the Delta lines).
. "$(dirname "$0")/common954.sh"
SUM=$OUT/summary_D.txt
T129=T129-win2/chain/anm_pin3_D180.5246.npz
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p "$R/$(dirname $T129)"; git -C "$RAW" show "origin/main:$T129" > "$R/$T129" || { echo "extract T129 failed" > $SUM; exit 1; }
: > $SUM
pyrun() { # build name want cmd...
  local b=$1 name=$2 want=$3; shift 3; local WT=/home/nathan/Source/choptuik-large-d-954$(echo $b | tr A-Z a-z)
  ( cd "$WT/hp" && . ../.venv/bin/activate
    so=$(python -c 'import hpkernel,os; print(os.path.dirname(hpkernel.__file__))')/*.so
    { echo "# $(stamp) UTC build $b, hp $(git -C $WT rev-parse --short HEAD), hpkernel $(python -c 'import hpkernel; print(hpkernel.__file__)')"; echo "# multidouble in the .so: $(strings -n 8 $so 2>/dev/null | grep -oE 'multidouble[-/][^/ ]+' | sort -u | head -3 | tr '\n' ' ')"; echo "# cmd: $*"; } > $OUT/$name.log
    s=$(date +%s); nice -n 10 "$@" >> $OUT/$name.log 2>&1; rc=$?; echo "exit $rc" >> $OUT/$name.log
    echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $SUM )
}
cmpl() { # nameA nameB: the iteration and Delta lines, without seconds, diffed
  local f='^  on [0-9]+:|^  od|^  qn|^  qd|^  \(a\)|StartNotProjected'
  d=$(diff <(grep -E "$f" $OUT/$1.log | sed -E 's/, [0-9.]+ s$//; s/, projections.*//') <(grep -E "$f" $OUT/$2.log | sed -E 's/, [0-9.]+ s$//; s/, projections.*//') | wc -l)
  echo "A against B, $1 and $2: the compared lines differ in $d lines $([ $d = 0 ] && echo IDENTICAL || echo DIFFER)" >> $SUM
}
pyrun A D_A_planted_ST 0 python octo_corrector.py planted $R $ST --threads $T
cmpl D_A_planted_ST B_planted
need=0
for n in D_A_planted_ST B_planted; do grep -q 'StartNotProjected' $OUT/$n.log && need=1; tail -1 $OUT/$n.log | grep -q '^exit 0' || need=1; done
echo "extras needed (StartNotProjected or a failing planted at ST): $need" >> $SUM
if [ $need = 1 ]; then
  for b in A B; do pyrun $b D_${b}_planted_ST_qd0 0 python octo_corrector.py planted $R $ST --threads $T --qd 0; done
  cmpl D_A_planted_ST_qd0 D_B_planted_ST_qd0
  for b in A B; do pyrun $b D_${b}_planted_T129 0 python octo_corrector.py planted $R $T129 --threads $T; done
  cmpl D_A_planted_T129 D_B_planted_T129
  for b in A B; do pyrun $b D_${b}_planted_T129_control 1 python octo_corrector.py planted $R $T129 --threads $T --mutate 10; done
  cmpl D_A_planted_T129_control D_B_planted_T129_control
fi
echo "# checksD done $(stamp) UTC" >> $SUM
