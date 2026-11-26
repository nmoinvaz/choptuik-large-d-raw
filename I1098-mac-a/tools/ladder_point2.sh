#!/bin/bash
# #1098 ladder, version 2: one full direct solve at D on fastmul6 (d368a0c0's kernel; 478e9d86's Python or later), the
# Moebius horizon a = max(8, n/400) with ks = ceil(1.5 (D - 2)) + 20, raised by 200 until the jump's ks + 200 residual
# change is at most 1e-50:
#   1. jump at M 32: the held solve (p1's harmonics 5-13 held at the guess) from a degree-1 fit in 1/n to two full
#      fastmul6 states SA and SB, the double-double solve and a quad-double check;
#   2. release h5..h11 to tol 1e-36 (their inner solves are re-converged by every later release), then h13 to 1e-48
#      with --ddelta 1e-25 (release_ls, kmax 13, the qd Jacobian handed to qq at its floor), octo-double residual;
#   3. the h13 state resampled to M MT (resample_m.py beside this script; none when MT is 32), h13 re-converged there
#      and the tail h15..KMAX released (kmax KMAX, qq, tol 1e-48, --ddelta 1e-25);
# each stage's log and states in OUT/<stage>/, each accepted outer step saved by release_ls
#
#     ladder_point2.sh D KC THREADS OUT SA SB [MT 48] [KMAX 31]
{
D=$1; KC=$2; T=$3; O=$4; SA=$5; SB=$6; MT=${7:-48}; KMAX=${8:-31}
HP=${HP:-$HOME/Source/choptuik-fastmul6/hp}
SITE=${SITE:-$HOME/Source/fastmul6-site}
PY=${PY:-$HOME/venv-314/bin/python}
EXTRA=${EXTRA:-}
TOOLS=$(cd "$(dirname "$0")" && pwd)
[ -d "$O" ] && [ -s "$SA" ] && [ -s "$SB" ] || { echo "usage: ladder_point2.sh D KC THREADS OUT SA SB [MT] [KMAX]"; exit 1; }
cd $HP || exit 1
grep -q "floor_dz=1e-12" form_s.py || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
KS=$($PY -c "import math; print(math.ceil(1.5 * ($D - 2)) + 20)")
A=$($PY -c "print(max(8.0, ($D - 2) / 400.0))")
DF=$($PY -c "print(f'{float($D):.4f}')")
H=$($PY -c "print(','.join(str(k) for k in range(15, $KMAX + 1, 2)))")
JB=$($PY -c "print(','.join(f'{k}:qq' for k in range(13, $KMAX + 1, 2)))")
mkdir -p $O/jump $O/rls $O/rls13 $O/tail
{
  date -u "+start %Y-%m-%d %H:%M:%S UTC"
  echo "D $D, ks $KS, kc $KC, a $A, tail M $MT, kmax $KMAX, threads $T"
} > $O/run.log
# the Moebius series' order: the jump's discretization report gives the residual's change at ks + 200; above KSBAR
# (1e-50, so that the full system's gain of up to about 1e25 leaves at most 1e-25 in Delta) ks grows by 200 and the
# jump runs again, at most 4 times (D 250 at ks 392: 1.6e-36, and Delta moved by -2.5e-17 against u)
KSBAR=${KSBAR:-1e-50}
for try in 1 2 3 4; do
  nice -n 10 timeout 3h $PY -u form_s.py jump $O/jump --D $D --states_s "$SA,$SB" --deg 1 --held 1 --mob $A --ks $KS \
    --kc $KC --delta fit --tol 1e-300 --it_max 12 --threads $T --commit 478e9d86 $EXTRA > $O/jump/jump.log 2>&1
  echo "jump ks $KS rc $? $(date -u +%H:%M:%S)" >> $O/run.log
  DKS=$(grep -oE "ks\+200: \|dF\| [0-9.e+-]+" $O/jump/jump.log | tail -1 | awk '{print $3}')
  echo "jump ks $KS: ks+200 |dF| $DKS (bar $KSBAR)" >> $O/run.log
  $PY -c "import sys; sys.exit(0 if float('${DKS:-inf}') <= float('$KSBAR') else 1)" && break
  cp $O/jump/jump.log $O/jump/jump_ks$KS.log
  KS=$((KS + 200))
done
$PY -c "import sys; sys.exit(0 if float('${DKS:-inf}') <= float('$KSBAR') else 1)" || exit 6
J=$O/jump/jump_s_D$DF.npz
grep -q "^  converged" $O/jump/jump.log && [ -s $J ] || exit 2
nice -n 10 timeout 6h $PY -u form_s.py release_ls $J $O/rls --harm 5,7,9,11 --kmax 13 --jac qd --res od --tol 1e-36 \
  --tol_h 1e-30 --ddelta 1 --threads $T --outer 8 --commit 478e9d86 $EXTRA > $O/rls/rls.log 2>&1
echo "rls h5-h11 rc $? $(date -u +%H:%M:%S)" >> $O/run.log
R=$O/rls/release_ls_h11_D$DF.npz
[ -s $R ] || exit 3
nice -n 10 timeout 4h $PY -u form_s.py release_ls $R $O/rls13 --harm 13 --kmax 13 --jac qd --res od --tol 1e-48 \
  --tol_h 1e-44 --ddelta 1e-25 --threads $T --outer 8 --commit 478e9d86 $EXTRA > $O/rls13/rls.log 2>&1
echo "rls h13 rc $? $(date -u +%H:%M:%S)" >> $O/run.log
R=$O/rls13/release_ls_h13_D$DF.npz
[ -s $R ] || exit 4
HT=$H
if [ "$MT" != "32" ]; then
  PYTHONPATH=$SITE:$HP $PY $TOOLS/resample_m.py $R $O/tail/h13_M$MT.npz $MT > $O/tail/resample.log 2>&1 || exit 5
  R=$O/tail/h13_M$MT.npz
  HT=13,$H
fi
nice -n 10 timeout 10h $PY -u form_s.py release_ls $R $O/tail --harm $HT --kmax $KMAX --jac_by $JB --res od --tol 1e-48 \
  --tol_h 1e-44 --ddelta 1e-25 --threads $T --outer 8 --commit 478e9d86 $EXTRA > $O/tail/rls.log 2>&1
echo "tail rc $? $(date -u +%H:%M:%S)" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
