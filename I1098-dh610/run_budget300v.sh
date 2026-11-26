#!/bin/bash
# #1098 part 1: D 300's full solve (rls300, u horizon, ks 306, kc 146, kt 36, 78 Taylor steps, kfreeze 13) re-solved
# with one discretization parameter changed ($1: kc+20 or kt+8) by release_ls --harm 13 --kmax 13 from the variant state
# (variant_state.py), the octo-double residual, tol 1e-48, tol_h 1e-44, the qd Jacobian with the hand-over to qq;
# 2 threads (moved from the loaded Mac)
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
grep -q 'kmax = int(o\["kmax"\])' $W/hp/form_s.py || exit 1
V=$1
O=$W/out/budget300/$V
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=1 $(cat $W/python_path) -u form_s.py release_ls $W/out/budget300_src/D300_full_$V.npz $O \
  --harm 13 --kmax 13 --jac qd --res od --tol 1e-48 --tol_h 1e-44 --threads 2 --outer 6 --commit 38a63d4b --allow_unraw > $O/rls.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
