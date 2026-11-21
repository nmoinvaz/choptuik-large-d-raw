#!/bin/bash
# #1060, the two controls ordered after parts 1-3 (coordinator's hc, 2026-11-21 ~04:46 UTC), one at a time on win2 (worktree D:\choptuik-i1060 at 8179068d, venv-i1058b, BelowNormal), caps 10800 s each by exact pid:
#  (1) series_split_check.py at anm_pin3_D260.6706.npz with --N 31 (the chain's order) instead of 24
#  (2) the step 17 A/B (S = 1, then S = 2) with --keep_plan 1 (the stored plan, no re-plan at the base): OUT step17_k1_s<S>
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
STATE=I966-dh370/ks_chain3b/leg10_D256.1776_ks293/anm_pin3_D260.6706.npz
stamp() { date -u '+%F %T'; }
[ "$(git -C $W rev-parse HEAD)" = 8179068da460fe6be81312602e4c9987d17d73a3 ] && [ -z "$(git -C $W status --short)" ] || { log "worktree $W is not clean main 8179068d: stop"; exit 1; }
[ "$(git hash-object /d/choptuik-large-d-raw-push/$STATE | cut -c1-12)" = 04e124334bf7 ] || { log "state blob hash differs: stop"; exit 1; }
echo "# $(stamp) UTC controls (1) N 31 and (2) keep_plan 1 start" >> $SUM; log "q controls start"
cd $W/hp || exit 1
# ---- (1)
name=split2_D260_N31
CMD2="-u series_split_check.py $RAWR $STATE --N 31 --threads 9 --Np 6 --split 2 --out $WOUT/$name"
{ echo "# $(stamp) UTC cmd: $PY $CMD2"; } > $OUT/$name.log
s0=$(date +%s)
crun $name 0 10800 series_split_check.py "$PY" $CMD2 >> $OUT/$name.log 2>&1
echo "exit $RC" >> $OUT/$name.log
echo "$name: series_split_check.py --N 31 exit $RC (want 0), $(( $(date +%s) - s0 )) s wall (cap 10800 s) capped $CAPPED (control 1)" >> $SUM
# ---- (2)
runone() {
  local nm=$1 S=$2
  local CMD="-u anm_run.py $RAWR $WOUT/$nm $(sed -e "s/--series_split S/--series_split $S/" -e "s/--keep_plan 0/--keep_plan 1/" $OUT/command_line.txt)"
  { echo "# $(stamp) UTC cmd: $PY $CMD"; } > $OUT/$nm.log
  local s1=$(date +%s)
  crun $nm 0 10800 anm_run.py "$PY" $CMD >> $OUT/$nm.log 2>&1
  echo "exit $RC" >> $OUT/$nm.log
  echo "$nm: expected exit 0, got $RC, $(( $(date +%s) - s1 )) s wall (cap 10800 s) capped $CAPPED (control 2, --keep_plan 1)" >> $SUM
}
runone step17_k1_s1 1
runone step17_k1_s2 2
cd $OUT
if [ -f step17_k1_s1/jet_pin3_D260.6706.npz ] && [ -f step17_k1_s2/jet_pin3_D260.6706.npz ]; then
  "$PY" series_agree1060.py step17_k1_s1/jet_pin3_D260.6706.npz step17_k1_s2/jet_pin3_D260.6706.npz > series_agree_k1_s1_s2.txt 2>&1
  "$PY" series_agree1060.py step17_s1/jet_pin3_D260.6706.npz step17_k1_s1/jet_pin3_D260.6706.npz > series_agree_s1_kp0_vs_kp1.txt 2>&1
fi
"$PY" report1060q.py > report_1060_q.md 2>&1; echo "controls (1) and (2) done, report_1060_q.md written" >> $SUM
log "q controls done"
touch $OUT/q.done; touch $OUT/all.done
