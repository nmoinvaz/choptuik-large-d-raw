#!/bin/bash
# #1098 on dh610: D 6666's M 48 tail (coordinator, 2026-11-27), in the 10 threads of its M 32 stages, once those end
# ("job rc 0" in D6666/run.log, written after rls13, and rls13's h13 state present; at most WAIT_H hours, 12 by default;
# h13 started 14:20:38 UTC). The recipe of d4628tail_610.sh (raw I1098-mac-a/tools/), with D 6666's values:
#   1. The ks: the downward gate put D 6666 at ks 7300 on the M 32 jump state. It is checked on the tail's own start:
#      rls13's h13 state resampled to M 48, set to ks 7300 (variant_state.py, a 16.66), then the upward gate (ks_gate.py,
#      steps of 100, bar 1e-64) from 7300. The tail takes the ks it gates at.
#   2. ladder_tail.sh mob (tools3, blob 322f0995): MT 48 at that ks, h13 re-converged and h15..h23 released (kmax 23,
#      qq, od, tol 1e-48, tol_h 1e-44, ddelta 1e-25), chord-free, then the k* stage (kstar_stage.sh, tools3).
#   3. kmax_rule.py (tools3): exit 0, kmax 23 suffices; exit 2, the h25 extension and the k* stage again into
#      tail/kstar25. A second "extend" is logged, not run.
#   hold_timeouts.sh (blob b9a711ca) runs beside it on tail/, cap 16 h per stage.
# fastmul7 (hp_z, site_z, Python c21ba40d, as D 6666's M 32 stages). tools3 is read, not written (D 4628's tail reads it
# too). Output into <ladder>/D6666/tail; the last act writes "job rc N" to tail/job.log and tail/run.log.
#
#     [WAIT_H=12] d6666tail_610.sh      (detached: systemd-run --user)
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
L=$LV/I1098-dh610/ladder
T=$L/tools3
S=$L/D6666/rls13/release_ls_h13_D6666.0000.npz
O=$L/D6666/tail
export HP=$W/hp_z SITE=$W/site_z PY=$(cat $W/python_path) COMMIT=c21ba40d
for f in ladder_tail.sh:322f0995ace89827d8265882f2c03defafaa7f1a kmax_rule.py:196f12a553edce9651fef58ef90353f3c7fb49b4 \
         kstar_stage.sh:6d29dfc0225a2eff0be932cb849e656c190a0b6e; do
  [ "$(git -C $LV hash-object --no-filters $T/${f%%:*})" = "${f#*:}" ] || { echo "tools3/${f%%:*}: blob differs"; exit 1; }
done
[ "$(git -C $LV hash-object --no-filters $W/hold_timeouts.sh)" = b9a711cad555836b1887162281073b955c42ce21 ] || exit 1
n=0
until grep -q "^job rc 0" $L/D6666/run.log 2>/dev/null && [ -s $S ]; do
  grep -q "^job rc [1-9]" $L/D6666/run.log 2>/dev/null && exit 2
  n=$((n + 1)); [ $n -gt $(( ${WAIT_H:-12} * 12 )) ] && exit 2; sleep 300
done
mkdir -p $O/gate
J=$O/job.log
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $J
bash $W/hold_timeouts.sh $O 57600 $O/hold_timeouts.log &
cd $HP || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1
fin() { echo "job rc $1 $(date -u +%H:%M:%S)" >> $J; echo "job rc $1 $(date -u +%H:%M:%S)" >> $O/run.log; exit $1; }
PYTHONPATH=$SITE:$HP $PY $T/resample_m.py $S $O/gate/h13_M48.npz 48 > $O/gate/prep.log 2>&1 || fin 3
PYTHONPATH=$SITE:$HP $PY $T/variant_state.py $HP $O/gate/h13_M48.npz $O/gate/h13_M48_ks7300.npz mob16.66,ks=7300 \
  >> $O/gate/prep.log 2>&1 || fin 3
PYTHONPATH=$SITE nice -n 10 $PY -u ks_gate.py $O/gate/h13_M48_ks7300.npz --bar 1e-64 --step 100 --tries 6 --threads 10 \
  > $O/gate/ks_gate.log 2>&1
KSG=$(grep -oE "^gate ks [0-9]+" $O/gate/ks_gate.log | awk '{print $3}')
echo "ks gate at M 48 from 7300 (bar 1e-64): ${KSG:-none} ($(tail -2 $O/gate/ks_gate.log | head -1)) $(date -u +%H:%M:%S)" >> $J
[ -n "$KSG" ] || fin 4
MT=48 KS=$KSG KMAX=23 INNER_CHORD=0 EXTRA= COMMIT=$COMMIT bash $T/ladder_tail.sh mob 6666 $S $O 10
echo "tail rc $? $(date -u +%H:%M:%S)" >> $J
$PY $T/kmax_rule.py $O/release_ls.jsonl > $O/kmax_rule.log 2>&1
r=$?
echo "kmax_rule rc $r ($(tail -1 $O/kmax_rule.log))" >> $J
if [ $r = 2 ]; then
  H23=$O/release_ls_h23_D6666.0000.npz
  [ -s $H23 ] || fin 5
  PYTHONPATH=$SITE nice -n 10 timeout 8h $PY -u form_s.py release_ls $H23 $O --harm 25 --kmax 25 --jac_by 25:qq --res od \
    --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 10 --outer 8 --inner_chord 0 --commit $COMMIT > $O/rls25.log 2>&1
  echo "h25 extension rc $? $(date -u +%H:%M:%S)" >> $J
  HP=$HP SITE=$SITE PY=$PY EXTRA= INNER_CHORD=0 COMMIT=$COMMIT bash $T/kstar_stage.sh $O $O/kstar25 10
  echo "kstar25 rc $? $(date -u +%H:%M:%S)" >> $J
  $PY $T/kmax_rule.py $O/release_ls.jsonl > $O/kmax_rule25.log 2>&1
  echo "kmax_rule after h25 rc $? ($(tail -1 $O/kmax_rule25.log)): a second extension is not run here" >> $J
fi
fin 0
}
