#!/bin/bash
# #1064 (coordinator's task of 21 Nov): base polishes from the chain's front, leg 13's accepted state at D 261.0721 (ks_chain3b, I966-dh370, ks 293), at ks 293 (the control), 315 and 316
# side by side, then 317 and 318 side by side. Leg 13's own anm_run line (ks_chain3b_q_dry.log) with only --state, an absolute OUT, and --steps 0 --keep_plan 0 --save_base 1 --ks K changed
# (#973's form), 10 threads per run, nice 10, each run capped at 7200 s by TERM to its exact pid (KILL after four more 30 s polls). Main 8179068d in the #1060 worktree, venv-i1058.
# The gate is the issue's: the last octo-double Newton line says converged and the base is saved (gate1064.py). If the control fails, the rungs are not started. A braced block ending in exit.
{
. "$(dirname "$0")/common1064.sh"
X=$OUT/exits_1064.txt; SUM=$OUT/summary_1064.txt
log() { echo "1064 $* $(stamp) UTC" >> $X; }
M=$(git -C $WT rev-parse HEAD) || exit 1
[ "${M:0:8}" = 8179068d ] || { log "worktree $WT is at $M, not 8179068d: stop"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { log "worktree $WT not clean: stop"; exit 1; }
[ "$(git hash-object $RAW/$S)" = $S_BLOB ] || { log "the state's blob differs from $S_BLOB: stop"; exit 1; }
log "worktree $WT at $M, venv-i1058, load $(cut -d' ' -f1-3 /proc/loadavg)"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONFAULTHANDLER=1
. $VENV/bin/activate
mkdir -p $OUT; cd $OUT
python3 $SD/gate1064.py --selftest > gate_selftest_1064.txt 2>&1; g1=$?; python3 $SD/gate1064.py --selftest --break > gate_selftest_break_1064.txt 2>&1; g2=$?
cd $WT/hp || exit 1
python3 -I $SD/xcheck1064.py --planted $RAW/$S $OUT/ctl_test > $OUT/xcheck_planted_1064.txt 2>&1; x1=$?
python3 -I $SD/xcheck1064.py --planted $RAW/$S $OUT/ctl_test --mutate > $OUT/xcheck_planted_mutate_1064.txt 2>&1; x2=$?
echo "controls: gate selftest exit $g1 (0), --break exit $g2 (1); xcheck planted exit $x1 (0), --mutate exit $x2 (1)" >> $SUM; log "controls gate $g1/$g2 xcheck $x1/$x2"
[ $g1 = 0 ] && [ $g2 = 1 ] && [ $x1 = 0 ] && [ $x2 = 1 ] || { log "a control is wrong: stop"; exit 1; }
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads 10 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13"
CAP=${CAP1064:-7200}
declare -A PID T0 TERMS GATE WALL RC CAPPED
start_k() { local K=$1; mkdir -p $OUT/ks$K
  { echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $OUT/ks$K --state $S $F --steps 0 --ks $K --keep_plan 0 --save_base 1 --D_max 270.8483"; } > $OUT/ks$K.log
  ( cd $WT/hp && exec nice -n 10 python3 -u anm_run.py $RAW $OUT/ks$K --state $S $F --steps 0 --ks $K --keep_plan 0 --save_base 1 --D_max 270.8483 >> $OUT/ks$K.log 2>&1 ) &
  PID[$K]=$!; T0[$K]=$(date +%s); TERMS[$K]=0; log "ks$K started, pid ${PID[$K]}"
}
run_rung() {  # K...: start them together, cap each, record exit, wall and the gate
  local K p alive
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
      fi
    done
    [ $alive = 0 ] && break
    sleep 30
  done
  for K in "$@"; do
    wait ${PID[$K]}; RC[$K]=$?; WALL[$K]=$(( $(date +%s) - ${T0[$K]} ))
    echo "exit ${RC[$K]}" >> $OUT/ks$K.log
    python3 $SD/gate1064.py $OUT/ks$K.log $OUT/ks$K > $OUT/gate_ks$K.txt 2>&1; GATE[$K]=$?
    echo "ks$K: exit ${RC[$K]}, ${WALL[$K]} s${CAPPED[$K]:+, capped at $CAP s}: $(cat $OUT/gate_ks$K.txt)" >> $SUM
    log "ks$K exit ${RC[$K]} wall ${WALL[$K]} s gate ${GATE[$K]}"
  done
}
run_rung 293
if [ "${GATE[293]}" != 0 ]; then
  echo "the control ks 293 did not converge: the rungs are not started (the issue: stop and report)" >> $SUM; log "control failed: rungs not started"
else
  run_rung 315 316
  run_rung 317 318
fi
cd $WT/hp
A=$(ls $OUT/ks293/base_pin3_D*.npz 2>/dev/null | head -1)
dl() {  # dl A.npz B.npz TAG
  { echo "# $(stamp) UTC cmd: python3 exact_recip_check.py delta $1 $2 --out $OUT/delta1064_$3.json"; } > $OUT/delta1064_$3.log
  nice -n 10 timeout -s TERM 1800 python3 exact_recip_check.py delta $1 $2 --out $OUT/delta1064_$3.json >> $OUT/delta1064_$3.log 2>&1; local rc=$?
  echo "exit $rc" >> $OUT/delta1064_$3.log
  python3 -I $SD/xcheck1064.py $1 $2 $OUT/delta1064_$3.json > $OUT/xcheck1064_$3.txt 2>&1; local rx=$?
  echo "delta1064_$3: exit $rc, xcheck exit $rx: $(grep 'Delta(b) - Delta(a)' $OUT/delta1064_$3.log | sed 's/^ *//')" >> $SUM; log "delta1064_$3 exit $rc xcheck $rx"
}
if [ -n "$A" ]; then
  for K in 315 316 317 318; do
    [ "${GATE[$K]}" = 0 ] || continue
    B=$(ls $OUT/ks$K/base_pin3_D*.npz | head -1)
    dl $A $B K$K
  done
  # information: the control's base against the stored leg 13 state (--keep_plan 0 plans the base again)
  dl $RAW/$S $A ctl_vs_leg13
fi
cd $OUT && python3 $SD/table1064.py $OUT > table_1064.md 2>&1
log "done"
echo "1064 done" >> $SUM
exit 0
}
