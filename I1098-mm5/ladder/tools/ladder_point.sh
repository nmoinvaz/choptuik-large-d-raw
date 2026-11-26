#!/bin/bash
# #1098 ladder: one full direct solve at D on fastmul6 (d368a0c0's kernel; dcd93f55's Python), M 32, the Moebius
# horizon a 8 with ks = ceil(1.5 (D - 2)) + 20:
#   1. jump: the held solve (p1's harmonics 5-13 held at the guess) from a guess fitted in 1/n to fastmul6's full
#      states at D 300 and D 1000 (degree 1), the double-double solve and a quad-double check (form_s.py jump);
#   2. release h5..h13 one at a time (release_ls, kmax 13, the qd Jacobian handed to qq at its floor), octo-double
#      residual, tol 1e-48, --ddelta 1e-25;
#   3. the tail h15..h31 (kmax 31, qq);
# each stage's log and states in OUT/<stage>/, each accepted outer step saved by release_ls
#
#     ladder_point.sh D KC THREADS OUT S300 S1000
{
D=$1; KC=$2; T=$3; O=$4; S300=$5; S1000=$6
HP=${HP:-$HOME/Source/choptuik-fastmul6/hp}
SITE=${SITE:-$HOME/Source/fastmul6-site}
PY=${PY:-$HOME/venv-314/bin/python}
EXTRA=${EXTRA:-}
[ -d "$O" ] && [ -s "$S300" ] && [ -s "$S1000" ] || { echo "usage: ladder_point.sh D KC THREADS OUT S300 S1000"; exit 1; }
cd $HP || exit 1
grep -q 'ddelta="1e-25"' form_s.py || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
KS=$($PY -c "import math; print(math.ceil(1.5 * ($D - 2)) + 20)")
DF=$($PY -c "print(f'{float($D):.4f}')")
H="15,17,19,21,23,25,27,29,31"
JB=$($PY -c "print(','.join(f'{k}:qq' for k in range(15, 32, 2)))")
mkdir -p $O/jump $O/rls $O/tail
{
  date -u "+start %Y-%m-%d %H:%M:%S UTC"
  echo "D $D, ks $KS, kc $KC, threads $T"
} > $O/run.log
nice -n 10 timeout 3h $PY -u form_s.py jump $O/jump --D $D --states_s "$S300,$S1000" --deg 1 --held 1 --mob 8 --ks $KS \
  --kc $KC --delta fit --tol 1e-300 --it_max 12 --threads $T --commit dcd93f55 $EXTRA > $O/jump/jump.log 2>&1
echo "jump rc $? $(date -u +%H:%M:%S)" >> $O/run.log
J=$O/jump/jump_s_D$DF.npz
[ -s $J ] || exit 2
nice -n 10 timeout 6h $PY -u form_s.py release_ls $J $O/rls --harm 5,7,9,11,13 --kmax 13 --jac qd --res od --tol 1e-48 \
  --tol_h 1e-44 --ddelta 1e-25 --threads $T --outer 8 --commit dcd93f55 $EXTRA > $O/rls/rls.log 2>&1
echo "rls rc $? $(date -u +%H:%M:%S)" >> $O/run.log
R=$O/rls/release_ls_h13_D$DF.npz
[ -s $R ] || exit 3
nice -n 10 timeout 8h $PY -u form_s.py release_ls $R $O/tail --harm $H --kmax 31 --jac_by $JB --res od --tol 1e-48 \
  --tol_h 1e-44 --ddelta 1e-25 --threads $T --outer 8 --commit dcd93f55 $EXTRA > $O/tail/rls.log 2>&1
echo "tail rc $? $(date -u +%H:%M:%S)" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
