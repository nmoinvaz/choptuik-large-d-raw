#!/bin/bash
# #1098 on mm5: D 8000's M 48 tail (coordinator, 2026-11-27), once its M 32 stages end ("job rc 0" in D8000/run.log, written
# by d8000_mm5.sh after rls13, and rls13's h13 state present; at most WAIT_H hours, 10 by default; h13 started 15:10:37
# UTC). The recipe of d4000tail_mm5.sh (raw I1098-mac-a/tools/mm5/), with D 8000's values, on 12 threads (the 6 that
# D 4000 freed and D 3214's, which end about when D 8000's h13 does; the tail is the ladder's last stage):
#   1. The ks: the downward gate put D 8000 at ks 8600 on the M 32 jump state. It is checked on the tail's own start:
#      rls13's h13 state resampled to M 48, set to ks 8600 (variant_state.py, a 19.995), then the upward gate (ks_gate.py,
#      steps of 100, bar 1e-64, the bar D 8000 was run to) from 8600. The tail takes the ks it gates at.
#   2. ladder_tail.sh mob (tools3, blob 322f0995): MT 48 at that ks, h13 re-converged and h15..h23 released (kmax 23,
#      qq, od, tol 1e-48, tol_h 1e-44, ddelta 1e-25), chord-free, then the k* stage (kstar_stage.sh, tools3).
#   3. kmax_rule.py (tools3, blob 196f12a5): exit 0, kmax 23 suffices; exit 2, the h25 extension and the k* stage again.
#   hold_timeouts.sh (tools3, blob b9a711ca) runs beside it on D8000/tail, cap 16 h per stage.
# fastmul7 (~/Source/choptuik-fastmul7 at d40a9c62, ~/Source/fastmul7-site). tools3 is read, not written. Output into
# <ladder>/D8000/tail; the last act writes "job rc N" to tail/job.log and tail/run.log.
#
#     [WAIT_H=10] d8000tail_mm5.sh      (detached, from the ladder folder)
{
L=$HOME/Source/choptuik-large-d-raw/I1098-mm5/ladder
T=$L/tools3
S=$L/D8000/rls13/release_ls_h13_D8000.0000.npz
O=$L/D8000/tail
export HP=$HOME/Source/choptuik-fastmul7/hp SITE=$HOME/Source/fastmul7-site PY=$HOME/venv-314/bin/python
R=$HOME/Source/choptuik-large-d-raw
for f in ladder_tail.sh:322f0995ace89827d8265882f2c03defafaa7f1a kmax_rule.py:196f12a553edce9651fef58ef90353f3c7fb49b4 \
         kstar_stage.sh:6d29dfc0225a2eff0be932cb849e656c190a0b6e hold_timeouts.sh:b9a711cad555836b1887162281073b955c42ce21; do
  [ "$(git -C $R hash-object --no-filters $T/${f%%:*})" = "${f#*:}" ] || { echo "tools3/${f%%:*}: blob differs"; exit 1; }
done
n=0
until grep -q "^job rc 0" $L/D8000/run.log 2>/dev/null && [ -s $S ]; do
  grep -q "^job rc [1-9]" $L/D8000/run.log 2>/dev/null && exit 2
  n=$((n + 1)); [ $n -gt $(( ${WAIT_H:-10} * 12 )) ] && exit 2; sleep 300
done
mkdir -p $O/gate
J=$O/job.log
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $J
bash $T/hold_timeouts.sh $O 57600 $O/hold_timeouts.log &
fin() { echo "job rc $1 $(date -u +%H:%M:%S)" >> $J; echo "job rc $1 $(date -u +%H:%M:%S)" >> $O/run.log; exit $1; }
COMMIT=$(git -C $HP rev-parse --short=8 HEAD)
cd $HP || fin 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1
PYTHONPATH=$SITE:$HP $PY $T/resample_m.py $S $O/gate/h13_M48.npz 48 > $O/gate/prep.log 2>&1 || fin 3
PYTHONPATH=$SITE:$HP $PY $T/variant_state.py $HP $O/gate/h13_M48.npz $O/gate/h13_M48_ks8600.npz mob19.995,ks=8600 \
  >> $O/gate/prep.log 2>&1 || fin 3
PYTHONPATH=$SITE nice -n 10 $PY -u ks_gate.py $O/gate/h13_M48_ks8600.npz --bar 1e-64 --step 100 --tries 6 --threads 12 \
  > $O/gate/ks_gate.log 2>&1
KSG=$(grep -oE "^gate ks [0-9]+" $O/gate/ks_gate.log | awk '{print $3}')
echo "ks gate at M 48 from 8600 (bar 1e-64): ${KSG:-none} ($(tail -2 $O/gate/ks_gate.log | head -1)) $(date -u +%H:%M:%S)" >> $J
[ -n "$KSG" ] || fin 4
MT=48 KS=$KSG KMAX=23 INNER_CHORD=0 EXTRA= COMMIT=$COMMIT bash $T/ladder_tail.sh mob 8000 $S $O 12
echo "tail rc $? $(date -u +%H:%M:%S)" >> $J
$PY $T/kmax_rule.py $O/release_ls.jsonl > $O/kmax_rule.log 2>&1
r=$?
echo "kmax_rule rc $r ($(tail -1 $O/kmax_rule.log))" >> $J
if [ $r = 2 ]; then
  H23=$O/release_ls_h23_D8000.0000.npz
  [ -s $H23 ] || fin 5
  PYTHONPATH=$SITE nice -n 10 timeout 8h $PY -u form_s.py release_ls $H23 $O --harm 25 --kmax 25 --jac_by 25:qq --res od \
    --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 12 --outer 8 --inner_chord 0 --commit $COMMIT > $O/rls25.log 2>&1
  echo "h25 extension rc $? $(date -u +%H:%M:%S)" >> $J
  HP=$HP SITE=$SITE PY=$PY EXTRA= INNER_CHORD=0 COMMIT=$COMMIT bash $T/kstar_stage.sh $O $O/kstar25 12
  echo "kstar25 rc $? $(date -u +%H:%M:%S)" >> $J
  $PY $T/kmax_rule.py $O/release_ls.jsonl > $O/kmax_rule25.log 2>&1
  echo "kmax_rule after h25 rc $? ($(tail -1 $O/kmax_rule25.log)): a second extension is not run here" >> $J
fi
fin 0
}
