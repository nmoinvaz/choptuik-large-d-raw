#!/bin/bash
# #1064, the coordinator's order of 21 Nov (~14:45 UTC): the projection switch. From the stored state at D 262.0099, leg 13's line with --elim_switch 1e-9 (ElimO projects a point only when its pinned quad-double max|F|
# exceeds 1e-9; the default is 1e-15) and nothing else changed (no --reseed_base): (1) the control ks 293, alone (if it does not converge the rungs are not started), then two at a time (2) ks 315 with --od_accept own
# (leg 13's) and (3) ks 315 with --od_accept natural. The gate and the 7200 s caps (TERM to the exact pid, KILL to it after four more 30 s polls) of run1064d.sh. A run's own wall is the first 30 s poll that finds its pid gone.
# Each run's first two 'on' lines of the octo-double corrector go to the summary. A braced block ending in exit.
# Env (defaults are the real run): ST1064E, STBLOB1064E, TAG1064E, EARLIER1064E (the re-seeded control of this state, information). For the dry test only: OUT1064, CAP1064, THR1064E.
{
. "$(dirname "$0")/common1064.sh"
S=${ST1064E:-I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.0099.npz}; S_BLOB=${STBLOB1064E:-eb34f3c845a485d606907b6f7ba2dc9ef429aaf1}; TAG=${TAG1064E:-sw_D262.0099}
EARLIER=${EARLIER1064E:-$SD/rb_D262.0099/ks293/base_pin3_D262.0099.npz}
OUT=${OUT1064:-$SD/$TAG}
mkdir -p $OUT
X=$OUT/exits_1064e.txt; SUM=$OUT/summary_1064e.txt
log() { echo "1064 $* $(stamp) UTC" >> $X; }
M=$(git -C $WT rev-parse HEAD) || exit 1
[ "${M:0:8}" = 276aa1cd ] || { log "worktree $WT is at $M, not 276aa1cd: stop"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { log "worktree $WT not clean: stop"; exit 1; }
[ "$(git hash-object $RAW/$S)" = $S_BLOB ] || { log "the state's blob differs from $S_BLOB: stop"; exit 1; }
[ -f $EARLIER ] || { log "the earlier control base is missing ($EARLIER): stop"; exit 1; }
for u in i1064 i1064b i1064f i1064g i1064j i1064k i1064l; do [ "$(systemctl --user is-active $u)" != active ] || { log "unit $u still active: stop"; exit 1; }; done
log "worktree $WT at $M, venv-i1058, load $(cut -d' ' -f1-3 /proc/loadavg), state $S"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONFAULTHANDLER=1
. $VENV/bin/activate
cd $OUT
python3 $SD/gate1064.py --selftest > gate_selftest_1064e.txt 2>&1; g1=$?; python3 $SD/gate1064.py --selftest --break > gate_selftest_break_1064e.txt 2>&1; g2=$?
cd $WT/hp || exit 1
python3 -I $SD/xcheck1064.py --planted $RAW/$S $OUT/ctl_test > $OUT/xcheck_planted_1064e.txt 2>&1; x1=$?
python3 -I $SD/xcheck1064.py --planted $RAW/$S $OUT/ctl_test --mutate > $OUT/xcheck_planted_mutate_1064e.txt 2>&1; x2=$?
echo "controls: gate selftest exit $g1 (0), --break exit $g2 (1); xcheck planted exit $x1 (0), --mutate exit $x2 (1)" >> $SUM; log "controls gate $g1/$g2 xcheck $x1/$x2"
[ $g1 = 0 ] && [ $g2 = 1 ] && [ $x1 = 0 ] && [ $x2 = 1 ] || { log "a control is wrong: stop"; exit 1; }
THR=${THR1064E:-10}
# leg 13's line, as in run1064d.sh without --reseed_base, plus the switch
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads $THR --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13 --elim_switch 1e-9"
FN=${F/--od_accept own/--od_accept natural}
[ "$FN" != "$F" ] && [ "${F/--reseed_base/}" = "$F" ] || { log "the flag line is wrong (no own to swap, or --reseed_base present): stop"; exit 1; }
CAP=${CAP1064:-7200}
declare -A KS FLG PID T0 T1 TERMS GATE WALL RC CAPPED
KS[ks293]=293; FLG[ks293]=$F
KS[ks315own]=315; FLG[ks315own]=$F
KS[ks315nat]=315; FLG[ks315nat]=$FN
start_k() { local L=$1; local K=${KS[$L]}; mkdir -p $OUT/$L
  { echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $OUT/$L --state $S ${FLG[$L]} --steps 0 --ks $K --keep_plan 0 --save_base 1 --D_max 270.8483"; } > $OUT/$L.log
  ( cd $WT/hp && exec nice -n 10 python3 -u anm_run.py $RAW $OUT/$L --state $S ${FLG[$L]} --steps 0 --ks $K --keep_plan 0 --save_base 1 --D_max 270.8483 >> $OUT/$L.log 2>&1 ) &
  PID[$L]=$!; T0[$L]=$(date +%s); TERMS[$L]=0; log "$L started, pid ${PID[$L]}"
}
run_rung() {  # LABEL...: start them together, cap each, record exit, own wall and the gate
  local L p alive
  [ $# = 0 ] && return
  for L in "$@"; do start_k $L; done
  while :; do
    alive=0
    for L in "$@"; do
      p=${PID[$L]}
      if kill -0 $p 2>/dev/null; then
        alive=1
        if [ $(( $(date +%s) - ${T0[$L]} )) -ge $CAP ]; then
          CAPPED[$L]=1; TERMS[$L]=$(( ${TERMS[$L]} + 1 ))
          if [ ${TERMS[$L]} -le 4 ]; then log "$L cap $CAP s: TERM to pid $p"; kill -TERM $p; else log "$L still alive: KILL to pid $p"; kill -KILL $p; fi
        fi
      elif [ -z "${T1[$L]}" ]; then T1[$L]=$(date +%s)
      fi
    done
    [ $alive = 0 ] && break
    sleep 30
  done
  for L in "$@"; do
    wait ${PID[$L]}; RC[$L]=$?; WALL[$L]=$(( ${T1[$L]} - ${T0[$L]} ))
    echo "exit ${RC[$L]}" >> $OUT/$L.log
    python3 $SD/gate1064.py $OUT/$L.log $OUT/$L > $OUT/gate_$L.txt 2>&1; GATE[$L]=$?
    echo "$L: exit ${RC[$L]}, own wall ${WALL[$L]} s (30 s polls)${CAPPED[$L]:+, capped at $CAP s}: $(cat $OUT/gate_$L.txt)" >> $SUM
    log "$L exit ${RC[$L]} wall ${WALL[$L]} s gate ${GATE[$L]}"
    echo "$L first two on-lines: $(grep -E '^ +on [0-9]' $OUT/$L.log | head -2 | sed 's/^ *//' | cut -c1-300 | tr '\n' '|')" >> $SUM
  done
}
run_rung ks293
A=""; R=""
if [ "${GATE[ks293]}" != 0 ]; then
  echo "the control ks 293 from this state did not converge: the rungs are not started (the issue: stop and report)" >> $SUM; log "control failed: rungs not started"
else
  A=$(ls $OUT/ks293/base_pin3_D*.npz | head -1); R="ks315own ks315nat"
  run_rung $R
fi
cd $WT/hp
dl() {  # dl A.npz B.npz TAG
  { echo "# $(stamp) UTC cmd: python3 exact_recip_check.py delta $1 $2 --out $OUT/delta1064_$3.json"; } > $OUT/delta1064_$3.log
  nice -n 10 timeout -s TERM 1800 python3 exact_recip_check.py delta $1 $2 --out $OUT/delta1064_$3.json >> $OUT/delta1064_$3.log 2>&1; local rc=$?
  echo "exit $rc" >> $OUT/delta1064_$3.log
  python3 -I $SD/xcheck1064.py $1 $2 $OUT/delta1064_$3.json > $OUT/xcheck1064_$3.txt 2>&1; local rx=$?
  echo "delta1064_$3: exit $rc, xcheck exit $rx: $(grep 'Delta(b) - Delta(a)' $OUT/delta1064_$3.log | sed 's/^ *//')" >> $SUM; log "delta1064_$3 exit $rc xcheck $rx"
}
if [ -n "$A" ]; then
  for L in $R; do
    [ "${GATE[$L]}" = 0 ] || continue
    B=$(ls $OUT/$L/base_pin3_D*.npz | head -1)
    dl $A $B $L
  done
  dl $RAW/$S $A ctl_vs_state        # information: the control's base against the stored state (--keep_plan 0 plans the base again)
  dl $EARLIER $A ctl_vs_reseeded    # information: against the re-seeded control of this state (rb_D262.0099/ks293)
fi
cd $OUT && python3 $SD/table1064e.py $OUT > table_1064e.md 2>&1
log "done"
echo "1064e done" >> $SUM
exit 0
}
