#!/bin/bash
# #1064, the coordinator's order of 21 Nov (~11:35 UTC): the re-seeded base. Main 276aa1cd's --reseed_base 1 re-seeds the base's horizon data at the run's --ks, from the base's own last node,
# before the polish. From leg 14's D 261.6229 state: the control ks 293 with --reseed_base 1 alone, then ks 315 and ks 294 side by side; leg 13's line plus --reseed_base 1, the gate and 7200 s caps of run1064c.sh.
# If the control does not converge the rungs are not started. Delta(K) - Delta(293) is against that control's base; the control's base is also compared with the earlier controls (information).
# Each log's 'base re-seed' line is copied to the summary (a missing line or a FAILED one is reported as such). A run's own wall is the first 30 s poll that finds its pid gone.
# Env (defaults are the real run): ST1064D, STBLOB1064D, TAG1064D, EARLIER1064D, EARLIER0_1064D. For the dry test only: OUT1064, CAP1064, R_1064D (the K of the rungs), THR1064D.
{
. "$(dirname "$0")/common1064.sh"
S=${ST1064D:-I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D261.6229.npz}; S_BLOB=${STBLOB1064D:-e0737904cb191e88a688df2e3968222c0920d3e5}; TAG=${TAG1064D:-rb_D261.6229}
EARLIER=${EARLIER1064D:-$SD/k294_D261.6229/ks293/base_pin3_D261.6229.npz}; EARLIER0=${EARLIER0_1064D:-$SD/leg14_D261.6229/ks293/base_pin3_D261.6229.npz}
OUT=${OUT1064:-$SD/$TAG}
mkdir -p $OUT
X=$OUT/exits_1064d.txt; SUM=$OUT/summary_1064d.txt
log() { echo "1064 $* $(stamp) UTC" >> $X; }
M=$(git -C $WT rev-parse HEAD) || exit 1
[ "${M:0:8}" = 276aa1cd ] || { log "worktree $WT is at $M, not 276aa1cd: stop"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { log "worktree $WT not clean: stop"; exit 1; }
[ "$(git hash-object $RAW/$S)" = $S_BLOB ] || { log "the state's blob differs from $S_BLOB: stop"; exit 1; }
[ -f $EARLIER ] && [ -f $EARLIER0 ] || { log "an earlier control base is missing ($EARLIER, $EARLIER0): stop"; exit 1; }
for u in i1064 i1064b i1064f i1064g; do [ "$(systemctl --user is-active $u)" != active ] || { log "unit $u still active: stop"; exit 1; }; done
log "worktree $WT at $M, venv-i1058, load $(cut -d' ' -f1-3 /proc/loadavg), state $S"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONFAULTHANDLER=1
. $VENV/bin/activate
cd $OUT
python3 $SD/gate1064.py --selftest > gate_selftest_1064d.txt 2>&1; g1=$?; python3 $SD/gate1064.py --selftest --break > gate_selftest_break_1064d.txt 2>&1; g2=$?
cd $WT/hp || exit 1
python3 -I $SD/xcheck1064.py --planted $RAW/$S $OUT/ctl_test > $OUT/xcheck_planted_1064d.txt 2>&1; x1=$?
python3 -I $SD/xcheck1064.py --planted $RAW/$S $OUT/ctl_test --mutate > $OUT/xcheck_planted_mutate_1064d.txt 2>&1; x2=$?
echo "controls: gate selftest exit $g1 (0), --break exit $g2 (1); xcheck planted exit $x1 (0), --mutate exit $x2 (1)" >> $SUM; log "controls gate $g1/$g2 xcheck $x1/$x2"
[ $g1 = 0 ] && [ $g2 = 1 ] && [ $x1 = 0 ] && [ $x2 = 1 ] || { log "a control is wrong: stop"; exit 1; }
THR=${THR1064D:-10}
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads $THR --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13 --reseed_base 1"
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
    echo "ks$K re-seed: $(grep -E '^base re-seed' $OUT/ks$K.log | cut -c1-300 | head -1 | grep . || echo 'NO base re-seed line in the log')" >> $SUM
  done
}
R=${R_1064D-315 294}
run_rung 293
A=""
if [ "${GATE[293]}" != 0 ]; then
  echo "the control ks 293 from this state did not converge: the rungs are not started (the issue: stop and report)" >> $SUM; log "control failed: rungs not started"; R=""
else
  A=$(ls $OUT/ks293/base_pin3_D*.npz | head -1)
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
  for K in $R; do
    [ "${GATE[$K]}" = 0 ] || continue
    B=$(ls $OUT/ks$K/base_pin3_D*.npz | head -1)
    dl $A $B K$K
  done
  dl $EARLIER $A ctl_vs_earlier     # the coordinator's ask: the re-seeded control's Delta against the earlier ks 293 control (run1064c's, k294_D261.6229/ks293)
  dl $EARLIER0 $A ctl_vs_earlier0   # and against the first ks 293 control of this state (leg14_D261.6229/ks293)
  dl $RAW/$S $A ctl_vs_state        # information: the control's base against the stored state (--keep_plan 0 plans the base again)
fi
cd $OUT && python3 $SD/table1064.py $OUT > table_1064d.md 2>&1
log "done"
echo "1064d done" >> $SUM
exit 0
}
