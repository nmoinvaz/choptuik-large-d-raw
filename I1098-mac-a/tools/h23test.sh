#!/bin/bash
# #1098: which horizon is right at D 300's h23 (Moebius a 8 ks 600 turns there by -3.9e-22 at M 32 and M 48; u does not).
# From the M 32 h21 states of the Moebius tail (MOB21) and of the u tail (U21), the h23 release alone (release_ls --harm 23
# --kmax 31, qq, od, tol 1e-48, --ddelta 1e-25) with the horizon changed by variant_state.py:
#   mob_ks800, mob_ks1000 (a 8), mob_a4, mob_a6 (ks 800) from MOB21; u_ks706, u_ks906 from U21
# 3 threads each, all six together, 2 h cap each; fastmul6, Python 478e9d86 or later
#
#     h23test.sh MOB21 U21 OUT
{
MOB=$1; U=$2; O=$3
HP=${HP:-$HOME/Source/choptuik-fastmul6/hp}
SITE=${SITE:-$HOME/Source/fastmul6-site}
PY=${PY:-$HOME/venv-314/bin/python}
EXTRA=${EXTRA:-}
TOOLS=$(cd "$(dirname "$0")" && pwd)
[ -s "$MOB" ] && [ -s "$U" ] && [ -d "$O" ] || { echo "usage: h23test.sh MOB21 U21 OUT"; exit 1; }
cd $HP || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
run() {  # name state variant
  mkdir -p $O/$1
  {
    date -u "+start %Y-%m-%d %H:%M:%S UTC"
    PYTHONPATH=$SITE:$HP $PY $TOOLS/variant_state.py $HP $2 $O/$1/start.npz $3
  } > $O/$1/run.log 2>&1
  nice -n 10 timeout 2h $PY -u form_s.py release_ls $O/$1/start.npz $O/$1 --harm 23 --kmax 31 --jac_by 23:qq --res od \
    --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 3 --outer 8 --commit 478e9d86 $EXTRA > $O/$1/rls.log 2>&1
  echo "rc $?" >> $O/$1/run.log
  date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/$1/run.log
}
run mob_ks800 $MOB ks=800 &
run mob_ks1000 $MOB ks=1000 &
run mob_a4 $MOB mob4,ks=800 &
run mob_a6 $MOB mob6,ks=800 &
run u_ks706 $U ks=706 &
run u_ks906 $U ks=906 &
wait
exit
}
