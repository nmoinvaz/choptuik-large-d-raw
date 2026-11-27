#!/bin/bash
# #1098 on dh610: D 4628's M 48 tail (coordinator, 2026-11-27), in the 8 threads its M 32 stages used, which ended at
# 10:42:30 UTC (rls13 released at outer 3, target |F| 2.37e-64; "job rc 0"). The recipe of d4000tail_mm5.sh (raw
# I1098-mac-a/tools/mm5/), with dh610's paths:
#   1. The ks: the downward gate put D 4628 at ks 5259 on the M 32 jump state. It is checked on the tail's own start:
#      rls13's h13 state resampled to M 48 (resample_m.py), set to ks 5259 (variant_state.py, a 11.565), then the upward
#      gate (ks_gate.py, steps of 100, bar 1e-64, the bar D 4628 was run to) from 5259. The tail takes the ks it gates at.
#   2. ladder_tail.sh mob (tools3, blob 322f0995): MT 48 at that ks, h13 re-converged and h15..h23 released (kmax 23,
#      qq, od, tol 1e-48, tol_h 1e-44, ddelta 1e-25), chord-free, then the k* stage (kstar_stage.sh, tools3).
#   3. kmax_rule.py (tools3, blob 196f12a5): exit 0, kmax 23 suffices; exit 2, the h25 extension and the k* stage again
#      into tail/kstar25, as in d4000tail_mm5.sh. A second "extend" is logged, not run.
#   hold_timeouts.sh (raw 6267c60b4, blob b9a711ca) runs beside it on tail/, so no stage's own time limit (10 h for the
#   tail, 3 h for the k* stage, 8 h for h25) can end it; its cap is 16 h per stage.
# fastmul7 (hp_z, site_z, Python c21ba40d, as D 4628's M 32 stages). Output into <ladder>/D4628_x706/tail; the last act
# writes "job rc N" to tail/job.log and tail/run.log.
#
#     d4628tail_610.sh      (detached: systemd-run --user)
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
L=$LV/I1098-dh610/ladder
T=$L/tools3
S=$L/D4628_x706/rls13/release_ls_h13_D4628.0000.npz
O=$L/D4628_x706/tail
export HP=$W/hp_z SITE=$W/site_z PY=$(cat $W/python_path) COMMIT=c21ba40d
for f in ladder_tail.sh:322f0995ace89827d8265882f2c03defafaa7f1a kmax_rule.py:196f12a553edce9651fef58ef90353f3c7fb49b4 \
         kstar_stage.sh:6d29dfc0225a2eff0be932cb849e656c190a0b6e; do
  [ "$(git -C $LV hash-object --no-filters $T/${f%%:*})" = "${f#*:}" ] || { echo "tools3/${f%%:*}: blob differs"; exit 1; }
done
[ "$(git -C $LV hash-object --no-filters $W/hold_timeouts.sh)" = b9a711cad555836b1887162281073b955c42ce21 ] || exit 1
grep -q "^job rc 0" $L/D4628_x706/run.log && [ -s $S ] || exit 2
mkdir -p $O/gate
J=$O/job.log
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $J
bash $W/hold_timeouts.sh $O 57600 $O/hold_timeouts.log &
cd $HP || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1
fin() { echo "job rc $1 $(date -u +%H:%M:%S)" >> $J; echo "job rc $1 $(date -u +%H:%M:%S)" >> $O/run.log; exit $1; }
PYTHONPATH=$SITE:$HP $PY $T/resample_m.py $S $O/gate/h13_M48.npz 48 > $O/gate/prep.log 2>&1 || fin 3
PYTHONPATH=$SITE:$HP $PY $T/variant_state.py $HP $O/gate/h13_M48.npz $O/gate/h13_M48_ks5259.npz mob11.565,ks=5259 \
  >> $O/gate/prep.log 2>&1 || fin 3
PYTHONPATH=$SITE nice -n 10 $PY -u ks_gate.py $O/gate/h13_M48_ks5259.npz --bar 1e-64 --step 100 --tries 6 --threads 8 \
  > $O/gate/ks_gate.log 2>&1
KSG=$(grep -oE "^gate ks [0-9]+" $O/gate/ks_gate.log | awk '{print $3}')
echo "ks gate at M 48 from 5259 (bar 1e-64): ${KSG:-none} ($(tail -2 $O/gate/ks_gate.log | head -1)) $(date -u +%H:%M:%S)" >> $J
[ -n "$KSG" ] || fin 4
MT=48 KS=$KSG KMAX=23 INNER_CHORD=0 EXTRA= COMMIT=$COMMIT bash $T/ladder_tail.sh mob 4628 $S $O 8
echo "tail rc $? $(date -u +%H:%M:%S)" >> $J
$PY $T/kmax_rule.py $O/release_ls.jsonl > $O/kmax_rule.log 2>&1
r=$?
echo "kmax_rule rc $r ($(tail -1 $O/kmax_rule.log))" >> $J
if [ $r = 2 ]; then
  H23=$O/release_ls_h23_D4628.0000.npz
  [ -s $H23 ] || fin 5
  PYTHONPATH=$SITE nice -n 10 timeout 8h $PY -u form_s.py release_ls $H23 $O --harm 25 --kmax 25 --jac_by 25:qq --res od \
    --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 8 --outer 8 --inner_chord 0 --commit $COMMIT > $O/rls25.log 2>&1
  echo "h25 extension rc $? $(date -u +%H:%M:%S)" >> $J
  HP=$HP SITE=$SITE PY=$PY EXTRA= INNER_CHORD=0 COMMIT=$COMMIT bash $T/kstar_stage.sh $O $O/kstar25 8
  echo "kstar25 rc $? $(date -u +%H:%M:%S)" >> $J
  $PY $T/kmax_rule.py $O/release_ls.jsonl > $O/kmax_rule25.log 2>&1
  echo "kmax_rule after h25 rc $? ($(tail -1 $O/kmax_rule25.log)): a second extension is not run here" >> $J
fi
fin 0
}
