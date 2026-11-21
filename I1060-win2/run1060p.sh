#!/bin/bash
# #1060, the three parts ordered after the controls (coordinator's hc, 2026-11-21 ~03:00 UTC), one run at a time on win2 (worktree D:\choptuik-i1060 at 8179068d, venv-i1058b, BelowNormal, 20 threads), caps 10800 s per run by exact pid:
#  (1) leg 10's own line from steps 15 and 16 (anm_pin3_D260.2515.npz, anm_pin3_D260.4708.npz), S = 1 and S = 2: OUT step15_s<S>, step16_s<S>
#  (2) step 17 (anm_pin3_D260.6706.npz) with --jet_tangent_from 0 in place of 1, S = 1 and S = 2: OUT step17_t0_s<S>
#  (3) series_split_check.py at leg13_D260.8483_ks293/anm_pin3_D261.0721.npz with #1034's arguments, then --mutate 31
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1060-win2
. $OUT/lib1060.sh
V=/c/Users/nathan/Source/venv-i1058b
PY=C:/Users/nathan/Source/venv-i1058b/Scripts/python.exe
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1058b OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export PATH="$V/Scripts:$PATH"
RAWR=D:/choptuik-large-d-raw-push
WOUT=D:/choptuik-i935-raw/I1060-win2
W=/d/choptuik-i1060
L10=I966-dh370/ks_chain3b/leg10_D256.1776_ks293
stamp() { date -u '+%F %T'; }
[ "$(git -C $W rev-parse HEAD)" = 8179068da460fe6be81312602e4c9987d17d73a3 ] && [ -z "$(git -C $W status --short)" ] || { log "worktree $W is not clean main 8179068d: stop"; exit 1; }
for f in $L10/anm_pin3_D260.2515.npz:2928c4a40900 $L10/anm_pin3_D260.4708.npz:a2eccb6c15fa $L10/anm_pin3_D260.6706.npz:04e124334bf7 I966-dh370/ks_chain3b/leg13_D260.8483_ks293/anm_pin3_D261.0721.npz:bd2c69a4d3fd; do
  n=${f%%:*}; h=${f##*:}; [ "$(git hash-object /d/choptuik-large-d-raw-push/$n | cut -c1-12)" = "$h" ] || { log "$n blob hash differs from $h: stop"; exit 1; }
done
echo "# $(stamp) UTC parts 1-3 start" >> $SUM; log "parts start"
cd $W/hp || exit 1
# runone NAME STATE_REL SPLIT TANGENT_FROM
runone() {
  local name=$1 state=$2 S=$3 tf=$4
  local CMD="-u anm_run.py $RAWR $WOUT/$name $(sed -e "s/--series_split S/--series_split $S/" -e "s/--jet_tangent_from 1/--jet_tangent_from $tf/" -e "s#--state [^ ]*#--state $state#" $OUT/command_line.txt)"
  { echo "# $(stamp) UTC cmd: $PY $CMD"; } > $OUT/$name.log
  local s0=$(date +%s)
  crun $name 0 10800 anm_run.py "$PY" $CMD >> $OUT/$name.log 2>&1
  echo "exit $RC" >> $OUT/$name.log
  echo "$name: expected exit 0, got $RC, $(( $(date +%s) - s0 )) s wall (cap 10800 s) capped $CAPPED" >> $SUM
  if grep -aq '^Traceback' $OUT/$name.log; then log "$name Traceback"; echo "$name: Traceback in the log" >> $SUM; fi
}
# ---- part 1
runone step15_s1 $L10/anm_pin3_D260.2515.npz 1 1
runone step15_s2 $L10/anm_pin3_D260.2515.npz 2 1
runone step16_s1 $L10/anm_pin3_D260.4708.npz 1 1
runone step16_s2 $L10/anm_pin3_D260.4708.npz 2 1
cd $OUT; "$PY" report1060p.py 1 > report_1060_p1.md 2>&1; echo "part 1 done, report_1060_p1.md written" >> $SUM; touch $OUT/p1.done
cd $W/hp
# ---- part 2
runone step17_t0_s1 $L10/anm_pin3_D260.6706.npz 1 0
runone step17_t0_s2 $L10/anm_pin3_D260.6706.npz 2 0
cd $OUT
if [ -f step17_t0_s1/jet_pin3_D260.6706.npz ] && [ -f step17_t0_s2/jet_pin3_D260.6706.npz ]; then
  "$PY" series_agree1060.py step17_t0_s1/jet_pin3_D260.6706.npz step17_t0_s2/jet_pin3_D260.6706.npz > series_agree_t0_s1_s2.txt 2>&1
  "$PY" series_agree1060.py step17_s1/jet_pin3_D260.6706.npz step17_t0_s1/jet_pin3_D260.6706.npz > series_agree_s1_t1_vs_t0.txt 2>&1
fi
"$PY" report1060p.py 2 > report_1060_p2.md 2>&1; echo "part 2 done, report_1060_p2.md written" >> $SUM; touch $OUT/p2.done
# ---- part 3
cd $W/hp
STATE3=I966-dh370/ks_chain3b/leg13_D260.8483_ks293/anm_pin3_D261.0721.npz
for M in 0 31; do
  if [ $M = 0 ]; then name=split2_D261; want=0; extra=""; else name=split2_D261_mut31; want=1; extra="--mutate 31"; fi
  CMD2="-u series_split_check.py $RAWR $STATE3 --N 24 --threads 9 --Np 6 --split 2 $extra --out $WOUT/$name"
  { echo "# $(stamp) UTC cmd: $PY $CMD2"; } > $OUT/$name.log
  s0=$(date +%s)
  crun $name $want 10800 series_split_check.py "$PY" $CMD2 >> $OUT/$name.log 2>&1
  echo "exit $RC" >> $OUT/$name.log
  echo "$name: series_split_check.py $extra exit $RC (want $want), $(( $(date +%s) - s0 )) s wall (cap 10800 s) capped $CAPPED" >> $SUM
done
echo "part 3 done" >> $SUM; log "parts done"
touch $OUT/p3.done; touch $OUT/all.done
