#!/bin/bash
# #1098: resume a ladder point's M 48 tail after its run ended (dh370, dh610 and mm5 were unplugged and moved,
# 2026-11-28 04:40 UTC), then its k* stage.
#
#     resume_tail.sh tail D STATE HARMS PREV OUT THREADS
#         release_ls from STATE (a release_ls_h<k>_D<D>.npz or its _step) into OUT for HARMS (e.g. 19,21,23) with
#         ladder_tail.sh's options (kmax 23, qq, od, tol 1e-48, tol_h 1e-44, ddelta 1e-25, outer 8, chord-free) under
#         timeout 16h; kmax_rule.py; then the k* stage on OUT/k, which merges PREV's release_ls.jsonl with OUT's and holds
#         PREV's (or OUT's) h15 state and OUT's h23 state, since kstar_stage.sh reads h15's release from the log
#     resume_tail.sh kstar D TAIL THREADS
#         the k* stage alone again, on TAIL (its release_ls.jsonl, h15 and h23 states), into TAIL/kstar_r
#
# The k* stage runs with hold_timeouts.sh (cap 8 h) on its folder, so kstar_stage.sh's 3 h limit on the re-converge
# cannot end it; the guard ends at the "job rc" line this script writes into that folder's run.log. Env: HP, SITE, PY,
# COMMIT, T (the tools folder, whose kmax_rule.py, kstar_stage.sh and hold_timeouts.sh are blob-checked here).
{
MODE=$1; D=$2
for f in kmax_rule.py:196f12a553edce9651fef58ef90353f3c7fb49b4 kstar_stage.sh:6d29dfc0225a2eff0be932cb849e656c190a0b6e \
         hold_timeouts.sh:b9a711cad555836b1887162281073b955c42ce21; do
  [ "$(git hash-object --no-filters $T/${f%%:*})" = "${f#*:}" ] || { echo "$T/${f%%:*}: blob differs"; exit 1; }
done
DS=$(printf "%.4f" $D)
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1
kstar() {  # FOLDER OUTDIR THREADS LOG: the guarded k* stage; "job rc N" into FOLDER/run.log and LOG
  bash $T/hold_timeouts.sh $1 28800 $1/hold_timeouts.log &
  HP=$HP SITE=$SITE PY=$PY EXTRA= INNER_CHORD=0 COMMIT=$COMMIT bash $T/kstar_stage.sh $1 $2 $3
  r=$?
  echo "kstar rc $r $(date -u +%H:%M:%S)" >> $4
  echo "job rc $r $(date -u +%H:%M:%S)" >> $1/run.log
  [ "$1/run.log" = "$4" ] || echo "job rc $r $(date -u +%H:%M:%S)" >> $4
  exit $r
}
if [ "$MODE" = tail ]; then
  S=$3; H=$4; P=$5; O=$6; TH=$7
  [ -s "$S" ] && [ -s "$P/release_ls.jsonl" ] && [ -n "$TH" ] || { echo "usage: resume_tail.sh tail D STATE HARMS PREV OUT THREADS"; exit 1; }
  mkdir -p $O/k
  echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC'): D $D from $S (blob $(git hash-object --no-filters $S)), harmonics $H, commit $COMMIT" > $O/run.log
  JB=$(echo $H | tr ',' '\n' | sed 's/$/:qq/' | paste -sd, -)
  cd $HP || exit 1
  PYTHONPATH=$SITE nice -n 10 timeout 16h $PY -u form_s.py release_ls $S $O --harm $H --kmax 23 --jac_by $JB --res od \
    --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads $TH --outer 8 --inner_chord 0 --commit $COMMIT > $O/rls.log 2>&1
  echo "rls $H rc $? $(date -u +%H:%M:%S)" >> $O/run.log
  FIN=$O/release_ls_h23_D$DS.npz
  [ -s $FIN ] || { echo "job rc 3 $(date -u +%H:%M:%S)" >> $O/run.log; exit 3; }
  cat $P/release_ls.jsonl $O/release_ls.jsonl > $O/k/release_ls.jsonl
  H15=$O/release_ls_h15_D$DS.npz; [ -s $H15 ] || H15=$P/release_ls_h15_D$DS.npz
  cp $H15 $FIN $O/k/
  $PY $T/kmax_rule.py $O/k/release_ls.jsonl > $O/kmax_rule.log 2>&1
  echo "kmax_rule rc $? ($(tail -1 $O/kmax_rule.log))" >> $O/run.log
  echo "k* stage on $O/k (h15 from $(dirname $H15)) $(date -u +%H:%M:%S)" >> $O/run.log
  kstar $O/k $O/k/kstar $TH $O/run.log
elif [ "$MODE" = kstar ]; then
  TD=$3; TH=$4
  [ -s "$TD/release_ls.jsonl" ] && [ -n "$TH" ] || { echo "usage: resume_tail.sh kstar D TAIL THREADS"; exit 1; }
  echo "k* stage again $(date -u '+%Y-%m-%d %H:%M:%S UTC'), into kstar_r, commit $COMMIT" >> $TD/run.log
  kstar $TD $TD/kstar_r $TH $TD/run.log
fi
echo "usage: resume_tail.sh tail D STATE HARMS PREV OUT THREADS | kstar D TAIL THREADS"
exit 1
}
