#!/bin/bash
# #1064, the coordinator's extension of 21 Nov (05:24 UTC): ks 295 with 297, then 301 with 305 side by side, the same flags, caps and gate as run1064.sh. The control (ks 293) is the one
# run1064.sh made ($SD/ks293, gate converged), so Delta(K) - Delta(293) is taken against its base. Each run is capped at CAP s by TERM to its exact pid (KILL after four more 30 s polls).
# A run's own wall is the first 30 s poll that finds its pid gone (run1064.sh took the wall after the whole rung ended). A braced block ending in exit.
# Env for the dry test only: OUT1064 (output folder), CAP1064, R1_1064B, R2_1064B (the K of each rung; R2 may be empty), THR1064B.
{
. "$(dirname "$0")/common1064.sh"
mkdir -p $OUT
X=$OUT/exits_1064b.txt; SUM=$OUT/summary_1064b.txt
log() { echo "1064 $* $(stamp) UTC" >> $X; }
M=$(git -C $WT rev-parse HEAD) || exit 1
[ "${M:0:8}" = 8179068d ] || { log "worktree $WT is at $M, not 8179068d: stop"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { log "worktree $WT not clean: stop"; exit 1; }
[ "$(git hash-object $RAW/$S)" = $S_BLOB ] || { log "the state's blob differs from $S_BLOB: stop"; exit 1; }
[ "$(systemctl --user is-active i1064)" != active ] || { log "unit i1064 still active: stop"; exit 1; }
grep -q '^converged' $SD/gate_ks293.txt || { log "the control ks 293 of run1064.sh did not converge: stop"; exit 1; }
A=$(ls $SD/ks293/base_pin3_D*.npz 2>/dev/null | head -1)
[ -n "$A" ] || { log "no control base in $SD/ks293: stop"; exit 1; }
log "worktree $WT at $M, venv-i1058, load $(cut -d' ' -f1-3 /proc/loadavg), control base $A"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONFAULTHANDLER=1
. $VENV/bin/activate
cd $OUT
python3 $SD/gate1064.py --selftest > gate_selftest_1064b.txt 2>&1; g1=$?; python3 $SD/gate1064.py --selftest --break > gate_selftest_break_1064b.txt 2>&1; g2=$?
cd $WT/hp || exit 1
python3 -I $SD/xcheck1064.py --planted $RAW/$S $OUT/ctl_test > $OUT/xcheck_planted_1064b.txt 2>&1; x1=$?
python3 -I $SD/xcheck1064.py --planted $RAW/$S $OUT/ctl_test --mutate > $OUT/xcheck_planted_mutate_1064b.txt 2>&1; x2=$?
echo "controls: gate selftest exit $g1 (0), --break exit $g2 (1); xcheck planted exit $x1 (0), --mutate exit $x2 (1)" >> $SUM; log "controls gate $g1/$g2 xcheck $x1/$x2"
[ $g1 = 0 ] && [ $g2 = 1 ] && [ $x1 = 0 ] && [ $x2 = 1 ] || { log "a control is wrong: stop"; exit 1; }
THR=${THR1064B:-10}
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads $THR --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13"
CAP=${CAP1064:-7200}
declare -A PID T0 T1 TERMS GATE WALL RC CAPPED
start_k() { local K=$1; mkdir -p $OUT/ks$K
  { echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $OUT/ks$K --state $S $F --steps 0 --ks $K --keep_plan 0 --save_base 1 --D_max 270.8483"; } > $OUT/ks$K.log
  ( cd $WT/hp && exec nice -n 10 python3 -u anm_run.py $RAW $OUT/ks$K --state $S $F --steps 0 --ks $K --keep_plan 0 --save_base 1 --D_max 270.8483 >> $OUT/ks$K.log 2>&1 ) &
  PID[$K]=$!; T0[$K]=$(date +%s); TERMS[$K]=0; log "ks$K started, pid ${PID[$K]}"
}
run_rung() {  # K...: start them together, cap each, record exit, own wall and the gate
  local K p alive
  [ $# = 0 ] && return
  for K in "$@"; do start_k $K; done
  while :; do
    alive=0
    for K in "$@"; do
      p=${PID[$K]}
      if kill -0 $p 2>/dev/null; then
        alive=1
        if [ $(( $(date +%s) - ${T0[$K]} )) -ge $CAP ]; then
          CAPPED[$K]=1; TERMS[$K]=$(( ${TERMS[$K]} + 1 ))
          if [ ${TERMS[$K]} -le 4 ]; then log "ks$K cap $CAP s: TERM to pid $p"; kill -TERM $p; else log "ks$K still alive: KILL to pid $p"; kill -KILL $p; fi
        fi
      elif [ -z "${T1[$K]}" ]; then T1[$K]=$(date +%s)
      fi
    done
    [ $alive = 0 ] && break
    sleep 30
  done
  for K in "$@"; do
    wait ${PID[$K]}; RC[$K]=$?; WALL[$K]=$(( ${T1[$K]} - ${T0[$K]} ))
    echo "exit ${RC[$K]}" >> $OUT/ks$K.log
    python3 $SD/gate1064.py $OUT/ks$K.log $OUT/ks$K > $OUT/gate_ks$K.txt 2>&1; GATE[$K]=$?
    echo "ks$K: exit ${RC[$K]}, own wall ${WALL[$K]} s (30 s polls)${CAPPED[$K]:+, capped at $CAP s}: $(cat $OUT/gate_ks$K.txt)" >> $SUM
    log "ks$K exit ${RC[$K]} wall ${WALL[$K]} s gate ${GATE[$K]}"
  done
}
R1=${R1_1064B-295 297}; R2=${R2_1064B-301 305}
run_rung $R1
run_rung $R2
cd $WT/hp
dl() {  # dl A.npz B.npz TAG
  { echo "# $(stamp) UTC cmd: python3 exact_recip_check.py delta $1 $2 --out $OUT/delta1064_$3.json"; } > $OUT/delta1064_$3.log
  nice -n 10 timeout -s TERM 1800 python3 exact_recip_check.py delta $1 $2 --out $OUT/delta1064_$3.json >> $OUT/delta1064_$3.log 2>&1; local rc=$?
  echo "exit $rc" >> $OUT/delta1064_$3.log
  python3 -I $SD/xcheck1064.py $1 $2 $OUT/delta1064_$3.json > $OUT/xcheck1064_$3.txt 2>&1; local rx=$?
  echo "delta1064_$3: exit $rc, xcheck exit $rx: $(grep 'Delta(b) - Delta(a)' $OUT/delta1064_$3.log | sed 's/^ *//')" >> $SUM; log "delta1064_$3 exit $rc xcheck $rx"
}
for K in $R1 $R2; do
  [ "${GATE[$K]}" = 0 ] || continue
  B=$(ls $OUT/ks$K/base_pin3_D*.npz | head -1)
  dl $A $B K$K
done
cd $OUT && python3 $SD/table1064.py $OUT > table_1064b.md 2>&1
log "done"
echo "1064b done" >> $SUM
exit 0
}
