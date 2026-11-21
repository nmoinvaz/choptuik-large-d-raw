#!/bin/bash
# #1064: (2) delta of the two earlier ks 293 controls by hand; (1) pilot of the re-seed alone at ks 294 and ks 315 (stopped by exact pid at the 'base re-seed' line, cap 400 s)
SD=$HOME/Source/choptuik-large-d-raw/I1064-dh610; RAW=$HOME/Source/choptuik-large-d-raw; WT=$HOME/Source/choptuik-large-d-1060; VENV=$HOME/Source/venv-i1058
OUT=$SD/dry_d3; mkdir $OUT || exit 1
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONFAULTHANDLER=1
. $VENV/bin/activate
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 276aa1cd ] && [ -z "$(git -C $WT status --short)" ] || { echo "worktree not at a clean 276aa1cd"; exit 1; }
cd $WT/hp || exit 1
A=$SD/k294_D261.6229/ks293/base_pin3_D261.6229.npz; B=$SD/leg14_D261.6229/ks293/base_pin3_D261.6229.npz
date -u '+%F %T delta of the two earlier controls'
{ echo "# $(date -u '+%F %T') UTC cmd: python3 exact_recip_check.py delta $A $B --out $OUT/delta_earlier_vs_earlier0.json"; } > $OUT/delta_earlier_vs_earlier0.log
nice -n 10 python3 exact_recip_check.py delta $A $B --out $OUT/delta_earlier_vs_earlier0.json >> $OUT/delta_earlier_vs_earlier0.log 2>&1; rc=$?; echo "exit $rc" >> $OUT/delta_earlier_vs_earlier0.log
python3 -I $SD/xcheck1064.py $A $B $OUT/delta_earlier_vs_earlier0.json > $OUT/xcheck_earlier_vs_earlier0.txt 2>&1; rx=$?
echo "delta exit $rc, xcheck exit $rx: $(grep 'Delta(b) - Delta(a)' $OUT/delta_earlier_vs_earlier0.log | sed 's/^ *//')"
S=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D261.6229.npz; THR=10
eval "$(grep '^F=' $SD/run1064d.sh)"
declare -A PID T0 DONE
for K in 294 315; do
  mkdir -p $OUT/ks$K
  { echo "# $(date -u '+%F %T') UTC cmd: python3 -u anm_run.py $RAW $OUT/ks$K --state $S $F --steps 0 --ks $K --keep_plan 0 --save_base 1 --D_max 270.8483"; } > $OUT/ks$K.log
  ( exec nice -n 10 python3 -u anm_run.py $RAW $OUT/ks$K --state $S $F --steps 0 --ks $K --keep_plan 0 --save_base 1 --D_max 270.8483 >> $OUT/ks$K.log 2>&1 ) &
  PID[$K]=$!; T0[$K]=$(date +%s); echo "ks$K started, pid ${PID[$K]} $(date -u '+%F %T')"
done
while :; do
  alive=0
  for K in 294 315; do
    p=${PID[$K]}
    kill -0 $p 2>/dev/null || continue
    alive=1
    if grep -q '^base re-seed' $OUT/ks$K.log; then echo "ks$K: re-seed line after $(( $(date +%s) - ${T0[$K]} )) s: TERM to pid $p"; kill -TERM $p; DONE[$K]=1
    elif [ $(( $(date +%s) - ${T0[$K]} )) -ge 400 ]; then echo "ks$K: no re-seed line at the 400 s cap: TERM to pid $p"; kill -TERM $p; fi
  done
  [ $alive = 0 ] && break
  sleep 10
done
for K in 294 315; do wait ${PID[$K]}; r=$?; echo "ks$K exit $r"; echo "exit $r" >> $OUT/ks$K.log; grep -E '^base re-seed' $OUT/ks$K.log | cut -c1-400; done
date -u '+%F %T done'
