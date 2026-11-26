#!/bin/bash
# #1098: Delta's error from the double-double d/dtheta matrices (hp/dmat_perturb.py, a3e6ca3b) on fastmul5 (site_x):
# release_ls --harm 13 --kmax 13 with the matrices moved to D_dd - S e, S = 2^16 and the linearity control 2^12, from
# a state given as $2 (name $1), qq Jacobian, octo-double residual, tol 1e-48, 3 threads each, 1 h cap each
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
grep -q "D_dd - S e" dmat_perturb.py || exit 1
PY=$(cat $W/python_path)
export HP_EXACT_RECIP=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_x
O=$W/out/fix
run() {  # name state scale
  mkdir -p $O/$1
  date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/$1/run.log
  HP_DMAT_SCALE=$3 timeout 1h $PY -u dmat_perturb.py release_ls $2 $O/$1 --harm 13 --kmax 13 --jac_by 13:qq --res od \
    --tol 1e-48 --tol_h 1e-44 --threads 3 --outer 8 --commit a3e6ca3b --allow_unraw > $O/$1/rls.log 2>&1
  echo "rc $?" >> $O/$1/run.log
  date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/$1/run.log
}
run $1_dmat16 $2 65536 &
run $1_dmat12 $2 4096 &
wait
exit
}
