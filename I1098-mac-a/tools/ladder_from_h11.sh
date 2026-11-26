#!/bin/bash
# #1098 ladder: a point of ladder_point2.sh resumed from its h11 state (OUT/rls/release_ls_h11_D<D>.npz), with the
# release options in EXTRA (for the chord-free path, EXTRA="--allow_unraw --inner_chord 0"):
#   0. UNIT set: waits (at most WAIT_H hours, 3 by default) for that unit's run.log line "rls h5-h11 rc", then stops the
#      unit, so its h13 release (begun with ladder_point2.sh's options) ends within its first outer step; its folder
#      OUT/rls13 is moved to OUT/rls13_<UTC time>, not deleted;
#   1. h13 to tol 1e-48 with ddelta 1e-25 (release_ls, kmax 13, qd Jacobian, od residual), as ladder_point2.sh's step 2;
#   2. STOP_AFTER=rls13 ends here; otherwise the h13 state resampled to M MT (resample_m.py beside this script; none
#      when MT is 32), h13 re-converged there and the tail h15..KMAX released, as ladder_point2.sh's step 3
#
#     [UNIT=name] [STOP_AFTER=rls13] ladder_from_h11.sh D THREADS OUT [MT 48] [KMAX 23]
{
D=$1; T=$2; O=$3; MT=${4:-48}; KMAX=${5:-23}
HP=${HP:-$HOME/Source/choptuik-fastmul6/hp}
SITE=${SITE:-$HOME/Source/fastmul6-site}
PY=${PY:-$HOME/venv-314/bin/python}
EXTRA=${EXTRA:-}
COMMIT=${COMMIT:-$(git -C $HP rev-parse --short=8 HEAD 2>/dev/null || echo unknown)}
TOOLS=$(cd "$(dirname "$0")" && pwd)
[ -d "$O/rls" ] && [ -n "$T" ] || { echo "usage: ladder_from_h11.sh D THREADS OUT [MT] [KMAX]"; exit 1; }
cd $HP || exit 1
grep -q "floor_dz=1e-12" form_s.py || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
DF=$($PY -c "print(f'{float($D):.4f}')")
H=$($PY -c "print(','.join(str(k) for k in range(15, $KMAX + 1, 2)))")
JB=$($PY -c "print(','.join(f'{k}:qq' for k in range(13, $KMAX + 1, 2)))")
if [ -n "${UNIT:-}" ]; then
  n=0
  while [ $n -lt $((${WAIT_H:-3} * 180)) ]; do
    grep -q "^rls h5-h11 rc" $O/run.log 2>/dev/null && break
    systemctl --user is-active --quiet $UNIT || break
    sleep 20; n=$((n + 1))
  done
  grep -q "^rls h5-h11 rc" $O/run.log || exit 7
  systemctl --user stop $UNIT
  [ -d $O/rls13 ] && mv $O/rls13 $O/rls13_$(date -u +%H%M%S)
  echo "$UNIT stopped after its h5-h11 release; h13 and the tail by ladder_from_h11.sh, EXTRA $EXTRA ($(date -u +%H:%M:%S))" >> $O/run.log
fi
R=$O/rls/release_ls_h11_D$DF.npz
[ -s $R ] || exit 3
mkdir -p $O/rls13 $O/tail
nice -n 10 timeout 4h $PY -u form_s.py release_ls $R $O/rls13 --harm 13 --kmax 13 --jac qd --res od --tol 1e-48 \
  --tol_h 1e-44 --ddelta 1e-25 --threads $T --outer 8 --commit $COMMIT $EXTRA > $O/rls13/rls.log 2>&1
echo "rls h13 rc $? $(date -u +%H:%M:%S)" >> $O/run.log
R=$O/rls13/release_ls_h13_D$DF.npz
[ -s $R ] || exit 4
if [ "${STOP_AFTER:-}" = "rls13" ]; then
  echo "stopped after rls13 (STOP_AFTER) $(date -u +%H:%M:%S)" >> $O/run.log
  exit 0
fi
HT=$H
if [ "$MT" != "32" ]; then
  PYTHONPATH=$SITE:$HP $PY $TOOLS/resample_m.py $R $O/tail/h13_M$MT.npz $MT > $O/tail/resample.log 2>&1 || exit 5
  R=$O/tail/h13_M$MT.npz
  HT=13,$H
fi
nice -n 10 timeout 10h $PY -u form_s.py release_ls $R $O/tail --harm $HT --kmax $KMAX --jac_by $JB --res od --tol 1e-48 \
  --tol_h 1e-44 --ddelta 1e-25 --threads $T --outer 8 --commit $COMMIT $EXTRA > $O/tail/rls.log 2>&1
echo "tail rc $? $(date -u +%H:%M:%S)" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
