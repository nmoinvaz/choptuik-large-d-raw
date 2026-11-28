#!/bin/bash
# #1098 ladder, a new point by recipe v2's amendment 2 (2026-11-27): the last node x_l = x20(D_top), the L = 20 node of
# the largest D among the guess's sources, so the point's L = (n/2) ln(1/x_l^2 - 1) is at most 20; the guess by
# form_s_lastnode.py guess, deg 2 in 1/n from SOURCES carried outward to x_l by Taylor steps; form_s.py jump from it
# (ladder_point2.sh's jump with --deg 0: held, a = max(8, n/400), ks = ceil(1.5 n) + 20, dd then qd, it_max 12); then
# ladder_point2.sh beside this script, which keeps that converged jump, with the downward ks gate started at
# KS0 = 1.2 n rounded to 10 (KSGATE_EXTRA "--down 1 --step 100 --ks0 KS0"; ks_gate.py steps up from KS0 when KS0 fails
# the bar, so a monotone tail gates as from ks), KSBAR 1e-64, chord-free, M 32 stages and the M MT tail to KMAX unless
# STOP_AFTER=rls13. HP's ks_gate.py must be wip/large-d-form-s 3b3bfc60's or later (it takes --down and --ks0).
#
#     ladder_new.sh D KC THREADS OUT SOURCES XL [MT 48] [KMAX 23]      (SOURCES: comma-separated state paths)
{
D=$1; KC=$2; T=$3; O=$4; SRC=$5; XL=$6; MT=${7:-48}; KMAX=${8:-23}
HP=${HP:-$HOME/Source/choptuik-fastmul7/hp}
SITE=${SITE:-$HOME/Source/fastmul7-site}
PY=${PY:-$HOME/venv-314/bin/python}
COMMIT=${COMMIT:-$(git -C $HP rev-parse --short=8 HEAD 2>/dev/null || echo unknown)}
TOOLS=$(cd "$(dirname "$0")" && pwd)
[ -n "$XL" ] && [ -n "$SRC" ] || { echo "usage: ladder_new.sh D KC THREADS OUT SOURCES XL [MT] [KMAX]"; exit 1; }
grep -q '"ks0"' $HP/ks_gate.py && grep -q '"down"' $HP/ks_gate.py || { echo "HP's ks_gate.py has no --down/--ks0"; exit 1; }
[ -s $HP/form_s_lastnode.py ] || exit 1
mkdir -p $O/guess $O/jump
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
KS=$($PY -c "import math; print(math.ceil(1.5 * ($D - 2)) + 20)")
A=$($PY -c "print(max(8.0, ($D - 2) / 400.0))")
KS0=$($PY -c "print(int(round(1.2 * ($D - 2), -1)))")
DF=$($PY -c "print(f'{float($D):.4f}')")
P=$O/pre.log
{
  date -u "+start %Y-%m-%d %H:%M:%S UTC"
  echo "D $D, x_l $XL, a $A, ks $KS, gate from ks0 $KS0, kc $KC, threads $T, Python commit $COMMIT; sources $SRC"
} >> $P
GS=$O/guess/guess_D$DF.npz
J=$O/jump/jump_s_D$DF.npz
cd $HP || exit 1
if grep -q "^  converged" $O/jump/jump.log 2>/dev/null && [ -s $J ]; then
  echo "jump kept from the earlier run ($(date -u +%H:%M:%S))" >> $P
else
  [ -s $GS ] || nice -n 10 $PY -u form_s_lastnode.py guess $O/guess --D $D --mob $A --ks $KS --kc $KC --deg 2 \
    --threads $T --states_s $SRC --xl $XL >> $P 2>&1
  [ -s $GS ] || { echo "no guess" >> $P; exit 3; }
  nice -n 10 timeout 4h $PY -u form_s.py jump $O/jump --D $D --states_s $GS --deg 0 --held 1 --mob $A --ks $KS --kc $KC \
    --delta fit --tol 1e-300 --it_max 12 --threads $T --commit $COMMIT > $O/jump/jump.log 2>&1
  echo "jump rc $? $(date -u +%H:%M:%S)" >> $P
fi
grep -q "^  converged" $O/jump/jump.log && [ -s $J ] || exit 2
export HP SITE PY COMMIT KSBAR=${KSBAR:-1e-64} INNER_CHORD=${INNER_CHORD:-0} EXTRA=${EXTRA:-}
export KSGATE_EXTRA="--down 1 --step 100 --ks0 $KS0"
bash $TOOLS/ladder_point2.sh $D $KC $T $O $GS $GS $MT $KMAX
exit
}
