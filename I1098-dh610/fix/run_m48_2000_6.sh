#!/bin/bash
# #1098 on fastmul6 (site_y, hp_y at dcd93f55's Python): D 2000 at M 48 (I1098-mm5/m48_2000/h13_M48.npz, blob 6c513cf0,
# rls2000d's M 32 state resampled), h13 then the tail h15..h31 with kmax 31, the qq Jacobian, the octo-double residual,
# tol 1e-48, --ddelta 1e-25, 8 threads, 16 h cap; each accepted step's state saved
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp_y || exit 1
grep -q 'ddelta="1e-25"' form_s.py || exit 1
PY=$(cat $W/python_path)
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_y
O=$W/out/fix6/D2000_M48_6
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
timeout 16h $PY -u form_s.py release_ls $W/out/fix6/inputs/D2000_h13_M48.npz $O --harm 13,15,17,19,21,23,25,27,29,31 \
  --kmax 31 --jac_by 13:qq,15:qq,17:qq,19:qq,21:qq,23:qq,25:qq,27:qq,29:qq,31:qq --res od --tol 1e-48 --tol_h 1e-44 \
  --ddelta 1e-25 --threads 8 --outer 8 --commit dcd93f55 --allow_unraw > $O/rls.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
