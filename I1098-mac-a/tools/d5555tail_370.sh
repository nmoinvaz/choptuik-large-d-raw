#!/bin/bash
# #1098 on dh370: D 5555's M 48 tail (coordinator, 2026-11-27), in the 6 threads of its M 32 stages, once those end
# ("job rc 0" in D5555/run.log, written by d5555_resume_370.sh after rls13, and rls13's h13 state present; at most WAIT_H
# hours, 10 by default). The recipe of d4628tail_610.sh and d4000tail_mm5.sh (raw I1098-mac-a/tools/), with dh370's paths:
#   1. The ks: the downward gate put D 5555 at ks 6160 on the M 32 jump state. It is checked on the tail's own start:
#      rls13's h13 state resampled to M 48 (resample_m.py), set to ks 6160 (variant_state.py, a 13.8825), then the upward
#      gate (ks_gate.py, steps of 100, bar 1e-64, the bar D 5555 was run to) from 6160. The tail takes the ks it gates at.
#   2. ladder_tail.sh mob (blob 322f0995): MT 48 at that ks, h13 re-converged and h15..h23 released (kmax 23, qq, od,
#      tol 1e-48, tol_h 1e-44, ddelta 1e-25), chord-free, then the k* stage (kstar_stage.sh).
#   3. kmax_rule.py (blob 196f12a5): exit 0, kmax 23 suffices; exit 2, the h25 extension and the k* stage again into
#      tail/kstar25. A second "extend" is logged, not run.
#   hold_timeouts.sh (blob b9a711ca) runs beside it on tail/, so no stage's own time limit can end it; cap 16 h per stage.
# fastmul6's Skylake wheel (site_sky, d368a0c0) and the Python copy hp_y5555 (f398e829), as D 5555's M 32 stages, accepted
# for this point as written in d5555_370.sh. Tools: tools4 (from raw c281b00d3) plus ladder_tail.sh and hold_timeouts.sh,
# fetched by blob from raw commit TC into tools4 (new files: nothing running reads them). Output into
# <ladder>/D5555/tail; the last act writes "job rc N" to tail/job.log and tail/run.log.
#
#     TC=<raw commit> [WAIT_H=10] d5555tail_370.sh      (detached: systemd-run --user)
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
L=$LV/I1098-dh370/ladder
T=$L/tools4
S=$L/D5555/rls13/release_ls_h13_D5555.0000.npz
O=$L/D5555/tail
export HP=$W/hp_y5555 SITE=$W/site_sky PY=/home/nathan/Source/choptuik-large-d-1082/.venv/bin/python COMMIT=f398e829
[ -n "$TC" ] || { echo "TC (the raw commit of the tools) is not set"; exit 1; }
git -C $LV fetch -q origin || exit 3
for f in ladder_tail.sh hold_timeouts.sh; do
  [ -s $T/$f ] || git -C $LV show $TC:I1098-mac-a/tools/$f > $T/$f || exit 3
done
for f in ladder_tail.sh:322f0995ace89827d8265882f2c03defafaa7f1a kmax_rule.py:196f12a553edce9651fef58ef90353f3c7fb49b4 \
         kstar_stage.sh:6d29dfc0225a2eff0be932cb849e656c190a0b6e hold_timeouts.sh:b9a711cad555836b1887162281073b955c42ce21; do
  [ "$(git -C $LV hash-object --no-filters $T/${f%%:*})" = "${f#*:}" ] || { echo "tools4/${f%%:*}: blob differs"; exit 1; }
done
n=0
until grep -q "^job rc 0" $L/D5555/run.log 2>/dev/null && [ -s $S ]; do
  tail -1 $L/D5555/run.log | grep -q "^job rc [1-9]" && grep -q "^resume" $L/D5555/run.log && \
    [ "$(grep -c '^job rc' $L/D5555/run.log)" -ge 2 ] && exit 2
  n=$((n + 1)); [ $n -gt $(( ${WAIT_H:-10} * 12 )) ] && exit 2; sleep 300
done
mkdir -p $O/gate
J=$O/job.log
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $J
bash $T/hold_timeouts.sh $O 57600 $O/hold_timeouts.log &
cd $HP || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1
fin() { echo "job rc $1 $(date -u +%H:%M:%S)" >> $J; echo "job rc $1 $(date -u +%H:%M:%S)" >> $O/run.log; exit $1; }
PYTHONPATH=$SITE:$HP $PY $T/resample_m.py $S $O/gate/h13_M48.npz 48 > $O/gate/prep.log 2>&1 || fin 3
PYTHONPATH=$SITE:$HP $PY $T/variant_state.py $HP $O/gate/h13_M48.npz $O/gate/h13_M48_ks6160.npz mob13.8825,ks=6160 \
  >> $O/gate/prep.log 2>&1 || fin 3
PYTHONPATH=$SITE nice -n 10 $PY -u ks_gate.py $O/gate/h13_M48_ks6160.npz --bar 1e-64 --step 100 --tries 6 --threads 6 \
  > $O/gate/ks_gate.log 2>&1
KSG=$(grep -oE "^gate ks [0-9]+" $O/gate/ks_gate.log | awk '{print $3}')
echo "ks gate at M 48 from 6160 (bar 1e-64): ${KSG:-none} ($(tail -2 $O/gate/ks_gate.log | head -1)) $(date -u +%H:%M:%S)" >> $J
[ -n "$KSG" ] || fin 4
MT=48 KS=$KSG KMAX=23 INNER_CHORD=0 EXTRA= COMMIT=$COMMIT bash $T/ladder_tail.sh mob 5555 $S $O 6
echo "tail rc $? $(date -u +%H:%M:%S)" >> $J
$PY $T/kmax_rule.py $O/release_ls.jsonl > $O/kmax_rule.log 2>&1
r=$?
echo "kmax_rule rc $r ($(tail -1 $O/kmax_rule.log))" >> $J
if [ $r = 2 ]; then
  H23=$O/release_ls_h23_D5555.0000.npz
  [ -s $H23 ] || fin 5
  PYTHONPATH=$SITE nice -n 10 timeout 8h $PY -u form_s.py release_ls $H23 $O --harm 25 --kmax 25 --jac_by 25:qq --res od \
    --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 6 --outer 8 --inner_chord 0 --commit $COMMIT > $O/rls25.log 2>&1
  echo "h25 extension rc $? $(date -u +%H:%M:%S)" >> $J
  HP=$HP SITE=$SITE PY=$PY EXTRA= INNER_CHORD=0 COMMIT=$COMMIT bash $T/kstar_stage.sh $O $O/kstar25 6
  echo "kstar25 rc $? $(date -u +%H:%M:%S)" >> $J
  $PY $T/kmax_rule.py $O/release_ls.jsonl > $O/kmax_rule25.log 2>&1
  echo "kmax_rule after h25 rc $? ($(tail -1 $O/kmax_rule25.log)): a second extension is not run here" >> $J
fi
fin 0
}
