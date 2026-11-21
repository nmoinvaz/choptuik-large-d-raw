#!/bin/bash
# #1064 on win2 (the coordinator's hc of 2026-11-21 ~08:37 UTC): base polishes from the chain's front, leg 14's accepted state at D 261.6229 (ks_chain3b, I966-dh370, ks 293), at ks 293 (the control, must converge), then 315 and 316 side by side
# at 10 threads each, each capped at 7200 s by the exact root pid (taskkill /T /F after the command line is checked). Leg 13's own anm_run line (dh610's run1064.sh, ks_chain3b_q_dry.log) with only --state, an absolute OUT, and
# --steps 0 --keep_plan 0 --save_base 1 --ks K changed (#973's form), venv-i1058b, worktree D:\choptuik-i1060 (main 8179068d), BelowNormal. The gate (gate1064.py, dh610's, copied) and the delta check (exact_recip_check.py delta,
# xcheck1064.py) are as dh610's. If the control fails the rungs are not started.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1064-win2
. $OUT/lib_1064.sh
V=/c/Users/nathan/Source/venv-i1058b
PY=C:/Users/nathan/Source/venv-i1058b/Scripts/python.exe
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1058b OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONFAULTHANDLER=1
export PATH="$V/Scripts:$PATH"
RAWR=D:/choptuik-large-d-raw-push
WOUT=D:/choptuik-i935-raw/I1064-win2
WT=/d/choptuik-i1060
S=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D261.6229.npz
S_BLOB=e0737904cb191e88a688df2e3968222c0920d3e5
CAP=7200
stamp() { date -u '+%F %T'; }
M=$(git -C $WT rev-parse HEAD) || exit 1
[ "${M:0:8}" = 8179068d ] || { log "worktree $WT is at $M, not 8179068d: stop"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { log "worktree $WT not clean: stop"; exit 1; }
[ "$(git hash-object /d/choptuik-large-d-raw-push/$S)" = $S_BLOB ] || { log "the state's blob differs from $S_BLOB: stop"; exit 1; }
log "worktree $WT at $M, venv-i1058b, state blob ${S_BLOB:0:8}"
cd $OUT
"$PY" gate1064.py --selftest > gate_selftest_1064.txt 2>&1; g1=$?; "$PY" gate1064.py --selftest --break > gate_selftest_break_1064.txt 2>&1; g2=$?
cd $WT/hp || exit 1
"$PY" -I $WOUT/xcheck1064.py --planted $RAWR/$S $WOUT/ctl_test > $OUT/xcheck_planted_1064.txt 2>&1; x1=$?
"$PY" -I $WOUT/xcheck1064.py --planted $RAWR/$S $WOUT/ctl_test --mutate > $OUT/xcheck_planted_mutate_1064.txt 2>&1; x2=$?
echo "controls: gate selftest exit $g1 (0), --break exit $g2 (1); xcheck planted exit $x1 (0), --mutate exit $x2 (1)" >> $SUM; log "controls gate $g1/$g2 xcheck $x1/$x2"
[ $g1 = 0 ] && [ $g2 = 1 ] && [ $x1 = 0 ] && [ $x2 = 1 ] || { log "a control is wrong: stop"; exit 1; }
F=$(cat $OUT/flags_leg13.txt)
declare -A GATE
rung1() {  # K: one run, capped, then its gate (runs in the foreground or as a background job)
  local K=$1 s0=$(date +%s) rc w g
  mkdir -p $OUT/ks$K
  { echo "# $(stamp) UTC cmd: $PY -u anm_run.py $RAWR $WOUT/ks$K --state $S $F --steps 0 --ks $K --keep_plan 0 --save_base 1 --D_max 270.8483"; } > $OUT/ks$K.log
  crun ks$K 0 $CAP anm_run.py "$PY" -u anm_run.py $RAWR $WOUT/ks$K --state $S $F --steps 0 --ks $K --keep_plan 0 --save_base 1 --D_max 270.8483 >> $OUT/ks$K.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/ks$K.log
  "$PY" $WOUT/gate1064.py $WOUT/ks$K.log $WOUT/ks$K > $OUT/gate_ks$K.txt 2>&1; g=$?
  echo "$g" > $OUT/gate_rc_ks$K.txt
  echo "ks$K: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"): $(cat $OUT/gate_ks$K.txt)" >> $SUM
  log "ks$K exit $rc wall $w s gate $g"
}
rung1 293
G293=$(cat $OUT/gate_rc_ks293.txt)
if [ "$G293" != 0 ]; then
  echo "the control ks 293 did not converge: the rungs are not started (the issue: stop and report)" >> $SUM; log "control failed: rungs not started"
else
  rung1 315 &
  p1=$!
  rung1 316 &
  p2=$!
  wait $p1; wait $p2
fi
cd $WT/hp
A=$(ls $OUT/ks293/base_pin3_D*.npz 2>/dev/null | head -1)
dl() {  # dl A.npz B.npz TAG
  { echo "# $(stamp) UTC cmd: $PY exact_recip_check.py delta $1 $2 --out $WOUT/delta1064_$3.json"; } > $OUT/delta1064_$3.log
  crun delta_$3 0 1800 exact_recip_check.py "$PY" exact_recip_check.py delta $1 $2 --out $WOUT/delta1064_$3.json >> $OUT/delta1064_$3.log 2>&1; local rc=$RC
  echo "exit $rc" >> $OUT/delta1064_$3.log
  "$PY" -I $WOUT/xcheck1064.py $1 $2 $WOUT/delta1064_$3.json > $OUT/xcheck1064_$3.txt 2>&1; local rx=$?
  echo "delta1064_$3: exit $rc, xcheck exit $rx: $(grep 'Delta(b) - Delta(a)' $OUT/delta1064_$3.log | sed 's/^ *//')" >> $SUM; log "delta1064_$3 exit $rc xcheck $rx"
}
if [ -n "$A" ]; then
  for K in 315 316; do
    [ "$(cat $OUT/gate_rc_ks$K.txt 2>/dev/null)" = 0 ] || continue
    B=$(ls $OUT/ks$K/base_pin3_D*.npz | head -1)
    dl $A $B K$K
  done
  # information: the control's base against the stored state (--keep_plan 0 plans the base again)
  dl $RAWR/$S $A ctl_vs_state
fi
cd $OUT && "$PY" table1064.py $WOUT > table_1064.md 2>&1
log "done"; echo "1064 done" >> $SUM
touch $OUT/all.done
exit 0
