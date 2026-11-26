#!/bin/bash
# #1098 part 1: D 1000's full solve (rls1000h13q, Moebius a 8, ks 1517, kc 200, kt 36, 186 Taylor steps, kfreeze 13)
# re-solved with one discretization parameter changed ($1: base, steps2, ks+200, kc+20, kt+8) by release_ls --harm 13
# --kmax 13 from the variant state (variant_state.py), the octo-double residual, tol 1e-48, tol_h 1e-44, the qd
# Jacobian with the hand-over to qq; 2 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
grep -q 'kmax = int(o\["kmax"\])' $W/hp/form_s.py || exit 1
V=$1
O=$W/out/budget1000/$V
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=1 $(cat $W/python_path) -u form_s.py release_ls $W/out/budget1000_src/D1000_full_$V.npz $O \
  --harm 13 --kmax 13 --jac qd --res od --tol 1e-48 --tol_h 1e-44 --threads 2 --outer 6 --commit 992c86c3 --allow_unraw > $O/rls.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
