#!/bin/bash
# #1098 ladder: the tail of a full fastmul6 h13 state (rls/release_ls_h13_D<D>.npz) to kmax KMAX (23 by default), in one
# of these forms (fastmul6, Python 478e9d86 or later):
#   u      the u horizon at M 32 with ks = ceil(1.7 (D - 2)); only for D <= 300 (at D 432 and 519 its inner solves did not
#          converge: the u series loses digits above about D 300, #1090)
#   mob    the Moebius horizon a = max(8, n/400) at M MT (32 by default; 48 resamples the state) with ks = KS, by default
#          ceil(1.5 (D - 2)) + 420: two steps of 200 past the jumps' 1.5n + 20, whose ks + 200 residual change was 5.8e-59
#          at D 432 and 2.8e-59 at D 519, each step of 200 cutting it by about 1e10 (D 300: 1.2e-53 at ks 600, 6.8e-64
#          at 800). The horizon's truncation must stay below about 1e-23 / gain(kmax): 1e-64 for kmax 23
#   mob48  the same as mob with MT 48
# The state's meta is set by variant_state.py, then h13 is re-converged and h15..KMAX released (release_ls kmax KMAX, qq,
# od, tol 1e-48, tol_h 1e-44, --ddelta 1e-25); variant_state.py and resample_m.py beside this script
#
#     [KMAX=23] [KS=N] [MT=32] ladder_tail.sh MODE D STATE OUT THREADS
{
MODE=$1; D=$2; S=$3; O=$4; T=$5
HP=${HP:-$HOME/Source/choptuik-fastmul6/hp}
SITE=${SITE:-$HOME/Source/fastmul6-site}
PY=${PY:-$HOME/venv-314/bin/python}
EXTRA=${EXTRA:-}
TOOLS=$(cd "$(dirname "$0")" && pwd)
[ -s "$S" ] && [ -n "$T" ] || { echo "usage: ladder_tail.sh u|mob|mob48 D STATE OUT THREADS"; exit 1; }
mkdir -p $O
cd $HP || exit 1
grep -q "floor_dz=1e-12" form_s.py || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
[ "$MODE" = "mob48" ] && MODE=mob && MT=48
if [ "$MODE" = "u" ]; then
  KS=$($PY -c "import math; print(math.ceil(1.7 * ($D - 2)))")
  PYTHONPATH=$SITE:$HP $PY $TOOLS/variant_state.py $HP $S $O/start.npz mob0,ks=$KS > $O/prep.log 2>&1 || exit 2
elif [ "$MODE" = "mob" ]; then
  KS=${KS:-$($PY -c "import math; print(math.ceil(1.5 * ($D - 2)) + 420)")}
  A=$($PY -c "print(max(8.0, ($D - 2) / 400.0))")
  MT=${MT:-32}
  if [ "$MT" != "32" ]; then
    PYTHONPATH=$SITE:$HP $PY $TOOLS/resample_m.py $S $O/resampled.npz $MT > $O/prep.log 2>&1 || exit 2
    S=$O/resampled.npz
  fi
  PYTHONPATH=$SITE:$HP $PY $TOOLS/variant_state.py $HP $S $O/start.npz mob$A,ks=$KS >> $O/prep.log 2>&1 || exit 2
else
  exit 1
fi
echo "$MODE (ks $KS, M ${MT:-32}) prepared $(date -u +%H:%M:%S)" >> $O/run.log
KMAX=${KMAX:-23}
JB=$($PY -c "print(','.join(f'{k}:qq' for k in range(13, $KMAX + 1, 2)))")
HT=$($PY -c "print(','.join(str(k) for k in range(13, $KMAX + 1, 2)))")
nice -n 10 timeout 10h $PY -u form_s.py release_ls $O/start.npz $O --harm $HT --kmax $KMAX \
  --jac_by $JB --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads $T --outer 8 --commit 478e9d86 $EXTRA \
  > $O/rls.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
