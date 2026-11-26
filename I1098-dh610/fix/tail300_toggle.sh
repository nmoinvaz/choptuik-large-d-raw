#!/bin/bash
# #1098: D 300's kfree-31 tail on fastmul6 from the old u state (I1088-dh610/rls300 h13 = D300_full_base, ks 306, M 32)
# with the old arithmetic switched back on: rd0 = HP_EXACT_RECIP=0 HP_EXACT_DMAT=0 (the old kernel's 1/k and d/dtheta;
# the old tail read -4.34487e-17), d0 = HP_EXACT_DMAT=0 alone; h15..h31, kmax 31, qq, od, tol 1e-48, --ddelta 1e-25,
# 2 threads each, 3 h cap
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp_y || exit 1
PY=$(cat $W/python_path)
export HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_y
O=$W/out/tail300
JB=15:qq,17:qq,19:qq,21:qq,23:qq,25:qq,27:qq,29:qq,31:qq
run() {  # name exact_recip exact_dmat
  mkdir -p $O/$1
  date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/$1/run.log
  HP_EXACT_RECIP=$2 HP_EXACT_DMAT=$3 timeout 3h $PY -u form_s.py release_ls $W/out/budget300_src/D300_full_base.npz $O/$1 \
    --harm 15,17,19,21,23,25,27,29,31 --kmax 31 --jac_by $JB --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 2 \
    --outer 8 --commit 478e9d86 --allow_unraw > $O/$1/rls.log 2>&1
  echo "rc $?" >> $O/$1/run.log
  date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/$1/run.log
}
run rd0 0 0 &
run d0 1 0 &
wait
exit
}
