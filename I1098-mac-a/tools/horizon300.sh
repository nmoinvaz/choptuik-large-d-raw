#!/bin/bash
# #1098: which D 300 horizon is right to 1e-23 on the fastmul5 kernel (f350aa62: lane-precision reciprocals, the Moebius
# series' relaxed products). Wave 1 left the Moebius horizon (a 8, ks 600) +3.23e-21 above the u horizon (ks 306).
# Each run re-solves one of wave 1's two converged states with one horizon parameter changed (variant_state.py), by
# release_ls --harm 13 --kmax 13, the qq Jacobian, the octo-double residual, tol 1e-48; its rls.log ends with "h13's
# change", Delta's change from that state. Three runs at a time, 3 threads each, 1 h cap each; 8 runs in 3 rounds.
#
#     horizon300.sh U_STATE MOB_STATE OUT_DIR
#
# U_STATE, MOB_STATE: wave 1's D300_u_base and D300_mob_base outputs (release_ls_h13_D300.0000.npz in each folder)
{
U=$1
B=$2
O=$3
HP=$HOME/Source/choptuik-fastmul5/hp
SITE=$HOME/Source/fastmul5-site
PY=$HOME/venv-314/bin/python
T=$(cd "$(dirname "$0")" && pwd)
[ -s "$U" ] && [ -s "$B" ] && [ -d "$O" ] || { echo "usage: horizon300.sh U_STATE MOB_STATE OUT_DIR"; exit 1; }
grep -q "def exact_recip" $HP/form_s.py || exit 1
cd $HP || exit 1
export HP_EXACT_RECIP=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
run() {  # name state variant relaxed
  mkdir -p $O/$1
  {
    date -u "+start %Y-%m-%d %H:%M:%S UTC"
    $PY $T/variant_state.py $HP $2 $O/$1/start.npz $3
  } > $O/$1/run.log 2>&1
  HP_HORIZON_RELAXED=$4 nice -n 10 timeout 1h $PY -u form_s.py release_ls $O/$1/start.npz $O/$1 --harm 13 --kmax 13 \
    --jac_by 13:qq --res od --tol 1e-48 --tol_h 1e-44 --threads 3 --outer 8 --commit f350aa62 > $O/$1/rls.log 2>&1
  echo "rc $?" >> $O/$1/run.log
  date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/$1/run.log
}
$PY -c "import hpkernel; print(hpkernel.__file__)" > $O/kernel.txt
grep -q fastmul5-site $O/kernel.txt || exit 2
run u_ks+200 $U ks+200 1 &
run mob_ks=800 $B ks=800 1 &
run mob_relax0 $B base 0 &
wait
run u_ks+400 $U ks+400 1 &
run mob_mob16 $B mob16 1 &
run mob_mob16,ks=800 $B mob16,ks=800 1 &
wait
run mob_mob4 $B mob4 1 &
run mob_mob4,ks=800 $B mob4,ks=800 1 &
wait
exit
}
