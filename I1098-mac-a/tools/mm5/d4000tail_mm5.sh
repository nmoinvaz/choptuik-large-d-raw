#!/bin/bash
# #1098 on mm5: D 4000's M 48 tail (coordinator, 2026-11-27 02:35 UTC), in D 4000's 6 threads once its M 32 stages
# have ended ("job rc 0" in D4000/run.log, rls13's h13 state present; at most WAIT_H hours, 8 by default).
#   1. The ks: dh610's downward gate put D 4000 at ks 4717 (raw I1098-dh610/ksdown: 4717 -> 4817 changes the
#      octo-double residual by 5.01e-75 at the M 32 jump state, 4617 -> 4717 by 2.92e-52, the control fires at 4717).
#      That gate was measured on the jump state, so it is checked here on the tail's own start: rls13's h13 state
#      resampled to M 48 (resample_m.py) and set to ks 4717 (variant_state.py, a 9.995), then the upward gate
#      (ks_gate.py, steps of 100, bar 1e-70, the bar D 4000 was run to) from 4717. The tail takes the ks it gates at.
#   2. ladder_tail.sh mob (tools3, blob 322f0995): MT 48 at that ks, h13 re-converged and h15..h23 released (kmax 23,
#      qq, od, tol 1e-48, tol_h 1e-44, ddelta 1e-25), chord-free, then the k* stage (kstar_stage.sh, tools3).
#   3. kmax_rule.py (tools3, blob 196f12a5) on the tail's release_ls.jsonl: exit 0, kmax 23 suffices; exit 2, the h25
#      extension (release_ls from the h23 state into the same folder, --harm 25 --kmax 25, qq, od, tol 1e-48, tol_h
#      1e-44, ddelta 1e-25, chord-free) and the k* stage again into tail/kstar25. A second "extend" is logged, not run.
# fastmul7 (~/Source/choptuik-fastmul7 at d40a9c62, ~/Source/fastmul7-site). Output into <ladder>/D4000/tail; the last
# act writes "job rc N" to tail/job.log.
#
#     [WAIT_H=8] d4000tail_mm5.sh      (detached, from the ladder folder)
{
L=$HOME/Source/choptuik-large-d-raw/I1098-mm5/ladder
T=$L/tools3
S=$L/D4000/rls13/release_ls_h13_D4000.0000.npz
O=$L/D4000/tail
export HP=$HOME/Source/choptuik-fastmul7/hp SITE=$HOME/Source/fastmul7-site PY=$HOME/venv-314/bin/python
R=$HOME/Source/choptuik-large-d-raw
for f in ladder_tail.sh:322f0995ace89827d8265882f2c03defafaa7f1a kmax_rule.py:196f12a553edce9651fef58ef90353f3c7fb49b4 \
         kstar_stage.sh:6d29dfc0225a2eff0be932cb849e656c190a0b6e; do
  [ "$(git -C $R hash-object --no-filters $T/${f%%:*})" = "${f#*:}" ] || { echo "tools3/${f%%:*}: blob differs"; exit 1; }
done
n=0
until grep -q "^job rc 0" $L/D4000/run.log 2>/dev/null && [ -s $S ]; do
  grep -q "^job rc [1-9]" $L/D4000/run.log 2>/dev/null && exit 2
  n=$((n + 1)); [ $n -gt $(( ${WAIT_H:-8} * 12 )) ] && exit 2; sleep 300
done
mkdir -p $O/gate
J=$O/job.log
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $J
COMMIT=$(git -C $HP rev-parse --short=8 HEAD)
cd $HP || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1
PYTHONPATH=$SITE:$HP $PY $T/resample_m.py $S $O/gate/h13_M48.npz 48 > $O/gate/prep.log 2>&1 || exit 3
PYTHONPATH=$SITE:$HP $PY $T/variant_state.py $HP $O/gate/h13_M48.npz $O/gate/h13_M48_ks4717.npz mob9.995,ks=4717 \
  >> $O/gate/prep.log 2>&1 || exit 3
PYTHONPATH=$SITE nice -n 10 $PY -u ks_gate.py $O/gate/h13_M48_ks4717.npz --bar 1e-70 --step 100 --tries 6 --threads 6 \
  > $O/gate/ks_gate.log 2>&1
KSG=$(grep -oE "^gate ks [0-9]+" $O/gate/ks_gate.log | awk '{print $3}')
echo "ks gate at M 48 from 4717 (bar 1e-70): ${KSG:-none} ($(tail -2 $O/gate/ks_gate.log | head -1)) $(date -u +%H:%M:%S)" >> $J
[ -n "$KSG" ] || exit 4
MT=48 KS=$KSG KMAX=23 INNER_CHORD=0 EXTRA= COMMIT=$COMMIT bash $T/ladder_tail.sh mob 4000 $S $O 6
echo "tail rc $? $(date -u +%H:%M:%S)" >> $J
$PY $T/kmax_rule.py $O/release_ls.jsonl > $O/kmax_rule.log 2>&1
r=$?
echo "kmax_rule rc $r ($(tail -1 $O/kmax_rule.log))" >> $J
if [ $r = 2 ]; then
  H23=$O/release_ls_h23_D4000.0000.npz
  [ -s $H23 ] || exit 5
  PYTHONPATH=$SITE nice -n 10 timeout 8h $PY -u form_s.py release_ls $H23 $O --harm 25 --kmax 25 --jac_by 25:qq --res od \
    --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 6 --outer 8 --inner_chord 0 --commit $COMMIT > $O/rls25.log 2>&1
  echo "h25 extension rc $? $(date -u +%H:%M:%S)" >> $J
  HP=$HP SITE=$SITE PY=$PY EXTRA= INNER_CHORD=0 COMMIT=$COMMIT bash $T/kstar_stage.sh $O $O/kstar25 6
  echo "kstar25 rc $? $(date -u +%H:%M:%S)" >> $J
  $PY $T/kmax_rule.py $O/release_ls.jsonl > $O/kmax_rule25.log 2>&1
  echo "kmax_rule after h25 rc $? ($(tail -1 $O/kmax_rule25.log)): a second extension is not run here" >> $J
fi
echo "job rc 0 $(date -u +%H:%M:%S)" >> $J
exit 0
}
