#!/bin/bash
# #1064 precross arm on win2 (the coordinator's hc of 2026-11-21 ~11:31 UTC, moved from dh610's queue): ks 315 from two states before the crossing, leg 10's accepted states of ks_chain3b (I966-dh370, ks 293)
# at D 260.0073 (Delta share 0.991) and D 259.4568, side by side at 10 threads each. Each state's ks 293 control first (the two controls side by side); a state's 315 rung starts only if its own control converged.
# The command is leg 13's line, the first arm's (../flags_leg13.txt, --od_accept own), with only --state, an absolute OUT and --steps 0 --keep_plan 0 --save_base 1 --ks K --D_max 270.8483 as in ../run1064w.sh.
# Each run is capped at 7200 s by the exact root pid (taskkill /T /F after the command line is checked). Gate, delta check and xcheck are the parent folder's.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1064-win2/precross
. $OUT/lib_1064.sh
V=/c/Users/nathan/Source/venv-i1058b
PY=C:/Users/nathan/Source/venv-i1058b/Scripts/python.exe
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1058b OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONFAULTHANDLER=1
export PATH="$V/Scripts:$PATH"
RAWR=D:/choptuik-large-d-raw-push
WOUT=D:/choptuik-i935-raw/I1064-win2/precross
WP=D:/choptuik-i935-raw/I1064-win2
WT=/d/choptuik-i1060
SD=I966-dh370/ks_chain3b/leg10_D256.1776_ks293
declare -A BLOB=( [260.0073]=7d45e68357a3a622ac433857e1cf2ddc79e2410c [259.4568]=7e2452f7d7f46275c84cd9d341d39e82d60ee0b0 )
DS="260.0073 259.4568"
CAP=7200
stamp() { date -u '+%F %T'; }
M=$(git -C $WT rev-parse HEAD) || exit 1
[ "${M:0:8}" = 8179068d ] || { log "worktree $WT is at $M, not 8179068d: stop"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { log "worktree $WT not clean: stop"; exit 1; }
for D in $DS; do
  [ "$(git hash-object /d/choptuik-large-d-raw-push/$SD/anm_pin3_D$D.npz)" = ${BLOB[$D]} ] || { log "the blob of the D $D state differs from ${BLOB[$D]}: stop"; exit 1; }
done
log "worktree $WT at $M, venv-i1058b, state blobs ${BLOB[260.0073]:0:8} (D 260.0073) ${BLOB[259.4568]:0:8} (D 259.4568)"
cd $OUT
"$PY" $WP/gate1064.py --selftest > gate_selftest_1064.txt 2>&1; g1=$?; "$PY" $WP/gate1064.py --selftest --break > gate_selftest_break_1064.txt 2>&1; g2=$?
cd $WT/hp || exit 1
"$PY" -I $WP/xcheck1064.py --planted $RAWR/$SD/anm_pin3_D260.0073.npz $WOUT/ctl_test > $OUT/xcheck_planted_1064.txt 2>&1; x1=$?
"$PY" -I $WP/xcheck1064.py --planted $RAWR/$SD/anm_pin3_D260.0073.npz $WOUT/ctl_test --mutate > $OUT/xcheck_planted_mutate_1064.txt 2>&1; x2=$?
echo "controls: gate selftest exit $g1 (0), --break exit $g2 (1); xcheck planted exit $x1 (0), --mutate exit $x2 (1)" >> $SUM; log "controls gate $g1/$g2 xcheck $x1/$x2"
[ $g1 = 0 ] && [ $g2 = 1 ] && [ $x1 = 0 ] && [ $x2 = 1 ] || { log "a control is wrong: stop"; exit 1; }
F=$(cat $WP/flags_leg13.txt)
echo " $F " | grep -q -e ' --od_accept own ' && ! echo " $F " | grep -q -e ' --od_accept natural ' || { log "flags_leg13.txt does not hold --od_accept own: stop"; exit 1; }
log "flags: the first arm's (../flags_leg13.txt, blob $(git hash-object $WP/flags_leg13.txt | cut -c1-8), --od_accept own)"
rung1() {  # D K
  local D=$1 K=$2 s0=$(date +%s) rc w g N=D$1_ks$2
  local S=$SD/anm_pin3_D$D.npz
  mkdir -p $OUT/$N
  { echo "# $(stamp) UTC cmd: $PY -u anm_run.py $RAWR $WOUT/$N --state $S $F --steps 0 --ks $K --keep_plan 0 --save_base 1 --D_max 270.8483"; } > $OUT/$N.log
  crun $N 0 $CAP anm_run.py "$PY" -u anm_run.py $RAWR $WOUT/$N --state $S $F --steps 0 --ks $K --keep_plan 0 --save_base 1 --D_max 270.8483 >> $OUT/$N.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/$N.log
  "$PY" $WP/gate1064.py $WOUT/$N.log $WOUT/$N > $OUT/gate_$N.txt 2>&1; g=$?
  echo "$g" > $OUT/gate_rc_$N.txt
  echo "$N: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"): $(cat $OUT/gate_$N.txt)" >> $SUM
  log "$N exit $rc wall $w s gate $g"
}
pids=""
for D in $DS; do rung1 $D 293 & pids="$pids $!"; done
for p in $pids; do wait $p; done
pids=""
for D in $DS; do
  if [ "$(cat $OUT/gate_rc_D${D}_ks293.txt 2>/dev/null)" = 0 ]; then rung1 $D 315 & pids="$pids $!"
  else echo "the control D${D}_ks293 did not converge: its ks 315 is not started (the issue: stop and report)" >> $SUM; log "control D$D failed: its 315 not started"; fi
done
for p in $pids; do wait $p; done
cd $WT/hp
dl() {  # dl A.npz B.npz TAG
  { echo "# $(stamp) UTC cmd: $PY exact_recip_check.py delta $1 $2 --out $WOUT/delta1064_$3.json"; } > $OUT/delta1064_$3.log
  crun delta_$3 0 1800 exact_recip_check.py "$PY" exact_recip_check.py delta $1 $2 --out $WOUT/delta1064_$3.json >> $OUT/delta1064_$3.log 2>&1; local rc=$RC
  echo "exit $rc" >> $OUT/delta1064_$3.log
  "$PY" -I $WP/xcheck1064.py $1 $2 $WOUT/delta1064_$3.json > $OUT/xcheck1064_$3.txt 2>&1; local rx=$?
  echo "delta1064_$3: exit $rc, xcheck exit $rx: $(grep 'Delta(b) - Delta(a)' $OUT/delta1064_$3.log | sed 's/^ *//')" >> $SUM; log "delta1064_$3 exit $rc xcheck $rx"
}
# information: each converged 315 base against its own control's base, and each control's base against its stored state
for D in $DS; do
  A=$(ls $OUT/D${D}_ks293/base_pin3_D*.npz 2>/dev/null | head -1)
  [ -n "$A" ] || continue
  if [ "$(cat $OUT/gate_rc_D${D}_ks315.txt 2>/dev/null)" = 0 ]; then
    B=$(ls $OUT/D${D}_ks315/base_pin3_D*.npz | head -1)
    dl $A $B D${D}_315_vs_293
  fi
  dl $RAWR/$SD/anm_pin3_D$D.npz $A D${D}_ctl_vs_state
done
cd $OUT && "$PY" $WOUT/report_precross.py $WOUT > table_precross.md 2>&1
log "done"; echo "1064 done" >> $SUM
touch $OUT/all.done
exit 0
