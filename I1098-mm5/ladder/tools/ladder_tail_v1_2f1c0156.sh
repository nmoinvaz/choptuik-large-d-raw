#!/bin/bash
# #1098 ladder: the kfree-31 tail of a full fastmul6 h13 state (ladder_point.sh's rls/release_ls_h13_D<D>.npz), in one of
# two forms (fastmul6, Python 478e9d86 or later):
#   u     the u horizon at M 32 with ks = ceil(1.7 (D - 2)), converged at D 300 (ks 506): the state's meta set to it by
#         variant_state.py (mob0,ks=N), h13 re-converged, then h15..h31
#   mob48 the Moebius horizon at M 48: the state resampled (resample_m.py), h13 re-converged, then h15..h31
# release_ls kmax 31, qq, od, tol 1e-48, tol_h 1e-44, --ddelta 1e-25; variant_state.py and resample_m.py beside this script
#
#     ladder_tail.sh MODE D STATE OUT THREADS
{
MODE=$1; D=$2; S=$3; O=$4; T=$5
HP=${HP:-$HOME/Source/choptuik-fastmul6/hp}
SITE=${SITE:-$HOME/Source/fastmul6-site}
PY=${PY:-$HOME/venv-314/bin/python}
EXTRA=${EXTRA:-}
TOOLS=$(cd "$(dirname "$0")" && pwd)
[ -s "$S" ] && [ -n "$T" ] || { echo "usage: ladder_tail.sh u|mob48 D STATE OUT THREADS"; exit 1; }
mkdir -p $O
cd $HP || exit 1
grep -q "floor_dz=1e-12" form_s.py || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
if [ "$MODE" = "u" ]; then
  KS=$($PY -c "import math; print(math.ceil(1.7 * ($D - 2)))")
  PYTHONPATH=$SITE:$HP $PY $TOOLS/variant_state.py $HP $S $O/start.npz mob0,ks=$KS > $O/prep.log 2>&1 || exit 2
elif [ "$MODE" = "mob48" ]; then
  PYTHONPATH=$SITE:$HP $PY $TOOLS/resample_m.py $S $O/start.npz 48 > $O/prep.log 2>&1 || exit 2
else
  exit 1
fi
echo "$MODE prepared $(date -u +%H:%M:%S)" >> $O/run.log
JB=13:qq,15:qq,17:qq,19:qq,21:qq,23:qq,25:qq,27:qq,29:qq,31:qq
nice -n 10 timeout 10h $PY -u form_s.py release_ls $O/start.npz $O --harm 13,15,17,19,21,23,25,27,29,31 --kmax 31 \
  --jac_by $JB --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads $T --outer 8 --commit 478e9d86 $EXTRA \
  > $O/rls.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
