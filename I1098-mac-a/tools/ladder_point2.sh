#!/bin/bash
# #1098 ladder, version 2: one full direct solve at D on fastmul6 (d368a0c0's kernel; 478e9d86's Python or later), the
# Moebius horizon a = max(8, n/400) with ks = ceil(1.5 (D - 2)) + 20, raised by 200 until the octo-double residual
# changes by at most KSBAR (1e-64) at ks + 200 (ks_gate.py), and the tail to kmax 23 by default:
#   1. jump at M 32: the held solve (p1's harmonics 5-13 held at the guess) from a degree-1 fit in 1/n to two full
#      fastmul6 states SA and SB, the double-double solve and a quad-double check;
#   2. release h5..h11 to tol 1e-36 (their inner solves are re-converged by every later release), then h13 to 1e-48
#      with --ddelta 1e-25 (release_ls, kmax 13, the qd Jacobian handed to qq at its floor), octo-double residual;
#   3. the h13 state resampled to M MT (resample_m.py beside this script; none when MT is 32), h13 re-converged there
#      and the tail h15..KMAX released (kmax KMAX, qq, tol 1e-48, --ddelta 1e-25);
# each stage's log and states in OUT/<stage>/, each accepted outer step saved by release_ls
#
#     ladder_point2.sh D KC THREADS OUT SA SB [MT 48] [KMAX 23]
{
D=$1; KC=$2; T=$3; O=$4; SA=$5; SB=$6; MT=${7:-48}; KMAX=${8:-23}
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
nice -n 10 timeout 3h $PY -u form_s.py jump $O/jump --D $D --states_s "$SA,$SB" --deg 1 --held 1 --mob $A --ks $KS \
  --kc $KC --delta fit --tol 1e-300 --it_max 12 --threads $T --commit 478e9d86 $EXTRA > $O/jump/jump.log 2>&1
echo "jump ks $KS rc $? $(date -u +%H:%M:%S)" >> $O/run.log
J=$O/jump/jump_s_D$DF.npz
grep -q "^  converged" $O/jump/jump.log && [ -s $J ] || exit 2
# the Moebius series' order (ks_gate.py): the octo-double residual's change at the jump's state when the series runs to
# ks + 200, ks raised by 200 until it is at most KSBAR (1e-64: the gain at kfree 23 is about 1e39 at D 300, so the
# truncation leaves at most about 1e-25 in Delta; KMAX 31 needs about 1e-70, the gain at kfree 31 being 1.5e47 there).
# D 250 at ks 392 moved Delta by -2.5e-17 against u, D 300 at ks 600 turned the tail at h23 by -3.9e-22 and ks 800 did
# not. The jump's own ks+200 |dF| is a quad-double residual's and floors near 1e-45 at D 1291, so it cannot gate this
KSBAR=${KSBAR:-1e-64}
$PY -u $HP/ks_gate.py $J --bar $KSBAR --threads $T > $O/jump/ks_gate.log 2>&1
KSG=$(grep -oE "^gate [0-9]+" $O/jump/ks_gate.log | awk '{print $2}')
echo "ks gate (bar $KSBAR): ${KSG:-none} ($(tail -2 $O/jump/ks_gate.log | head -1))" >> $O/run.log
[ -n "$KSG" ] || exit 6
if [ "$KSG" != "$KS" ]; then
  PYTHONPATH=$SITE:$HP $PY $TOOLS/variant_state.py $HP $J $O/jump/jump_ks$KSG.npz ks=$KSG >> $O/run.log 2>&1 || exit 6
  J=$O/jump/jump_ks$KSG.npz
fi
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
