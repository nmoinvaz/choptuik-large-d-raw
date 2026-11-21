#!/bin/bash
# #1060 step 2 on win2 (the coordinator's hc of 2026-11-21 ~01:55 UTC): leg 10's step 17 of dh370's ks_chain3b run (D 260.6706 -> 260.8483, a 0.1777) twice on venv-i1058b (hpkernel from main 8179068d, #1058) with a worktree of main
# D:\choptuik-i1060 at 8179068d, from hp/: leg 10's own anm_run command line (command_line.txt: run966m.sh chainm, F3m + --reseed_qd_bar 1e-13 --steps 400 --ks 293 --keep_plan 0 --D_max 266.1776, taken from the dry log
# I966-dh370/ks_chain3b_m_dry.log) with --threads 20 (leg 10: 10), --steps 1, --D_max 300 and an absolute OUT, once with --series_split 1 (leg 10's own; the first attempt, S = 0, was stopped by the coordinator's order after 1.5 min) and once with --series_split 2, nothing else differing. S = 1 first, then S = 2, one at a time on
# an otherwise idle machine, BelowNormal, caps 10800 s each by the exact root pid (command line checked for anm_run.py). The comparator is dh610's cmp1060.py (raw I1060-dh610, blob 953872c9, copied here); its controls run first.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1060-win2
. $OUT/lib1060.sh
V=/c/Users/nathan/Source/venv-i1058b
PY=C:/Users/nathan/Source/venv-i1058b/Scripts/python.exe
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1058b OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export PATH="$V/Scripts:$PATH"
RAWR=D:/choptuik-large-d-raw-push                 # read only: the state of leg 10 (blob hashes checked below)
REFD=$RAWR/I966-dh370/ks_chain3b/leg10_D256.1776_ks293
WOUT=D:/choptuik-i935-raw/I1060-win2
W=/d/choptuik-i1060
stamp() { date -u '+%F %T'; }
[ "$(git -C $W rev-parse HEAD)" = 8179068da460fe6be81312602e4c9987d17d73a3 ] && [ -z "$(git -C $W status --short)" ] || { log "worktree $W is not clean main 8179068d: stop"; exit 1; }
for f in anm_pin3_D260.6706.npz:04e124334bf7 anm_pin3_D260.8483.npz:1502a41e022c jet_pin3_D260.6706.npz:29d3176c74c4 pred_pin3_D260.8483.npz:3d972c20763c anm_run.jsonl:14f606ca6cb9; do
  n=${f%%:*}; h=${f##*:}; [ "$(git hash-object /d/choptuik-large-d-raw-push/I966-dh370/ks_chain3b/leg10_D256.1776_ks293/$n | cut -c1-12)" = "$h" ] || { log "$n blob hash differs from $h: stop"; exit 1; }
done
echo "# $(stamp) UTC 1060 win2: hpkernel $("$PY" -c 'import hpkernel;print(hpkernel.__file__, hpkernel.isa(), hasattr(hpkernel.Solver,"set_exact_recip"))' 2>&1 | tail -1); worktree $W at $(git -C $W rev-parse --short HEAD)" >> $SUM
log "start"
# the comparator's controls first (the script stops when one is wrong)
c=0; cd $OUT
"$PY" cmp1060.py bits $REFD/anm_pin3_D260.8483.npz $REFD/anm_pin3_D260.8483.npz > ctl_bits.txt 2>&1; [ $? = 0 ] || c=1
"$PY" cmp1060.py bits $REFD/anm_pin3_D260.8483.npz $REFD/anm_pin3_D260.8483.npz --mutate > ctl_bits_mutate.txt 2>&1; [ $? = 1 ] || c=1
"$PY" cmp1060.py files $REFD/jet_pin3_D260.6706.npz $REFD/jet_pin3_D260.6706.npz --mutate > ctl_files_mutate.txt 2>&1; [ $? = 1 ] || c=1
for E in 1e-120 1e-90; do
  "$PY" cmp1060.py plant $E $REFD/anm_pin3_D260.8483.npz $WOUT/planted_$E.npz > ctl_plant_$E.txt 2>&1
  "$PY" cmp1060.py close $REFD/anm_pin3_D260.8483.npz $WOUT/planted_$E.npz > ctl_close_$E.txt 2>&1; r=$?
  if [ $E = 1e-120 ]; then [ $r = 0 ] || c=1; else [ $r = 1 ] || c=1; fi
done
echo "comparator controls: $([ $c = 0 ] && echo 'all as required' || echo WRONG) (ctl_*.txt: bits identical exit 0, bits --mutate exit 1, files --mutate exit 1, plant 1e-120 passes close, 1e-90 fails it)" >> $SUM; log "comparator controls c=$c"
[ $c = 0 ] || exit 1
cd $W/hp || exit 1
for S in 1 2; do
  CMD="-u anm_run.py $RAWR $WOUT/step17_s$S $(sed "s/--series_split S/--series_split $S/" $OUT/command_line.txt)"
  { echo "# $(stamp) UTC cmd: $PY $CMD"; } > $OUT/step17_s$S.log
  s0=$(date +%s)
  crun step17_s$S 0 10800 anm_run.py "$PY" $CMD >> $OUT/step17_s$S.log 2>&1
  echo "exit $RC" >> $OUT/step17_s$S.log
  echo "step17_s$S: expected exit 0, got $RC, $(( $(date +%s) - s0 )) s wall (cap 10800 s) capped $CAPPED" >> $SUM
  if grep -aq '^Traceback' $OUT/step17_s$S.log; then log "step17_s$S Traceback, stop"; echo "step17_s$S: Traceback in the log, stopped" >> $SUM; break; fi
  if [ ! -f $OUT/step17_s$S/anm_pin3_D260.8483.npz ]; then echo "step17_s$S: no state anm_pin3_D260.8483.npz in the output: D differs or the step failed; reading: report both logs' step lines and stop" >> $SUM; log "s$S: no state at D 260.8483"; break; fi
done
cd $OUT
"$PY" report1060w.py > report_1060w.md 2>&1
echo "report_1060w.md written" >> $SUM; log "done"
touch $OUT/all.done
