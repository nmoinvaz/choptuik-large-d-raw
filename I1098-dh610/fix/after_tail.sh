#!/bin/bash
# #1098: D 1000's M 48 kfreeze tail continued past wave 2 (wave2.sh's D1000_M48_tail, h15..h23 with kmax 31): h25..h31,
# then h33..h37, from its h23 state, kmax 37, the qq Jacobian, the octo-double residual, tol 1e-48, 8 threads, each
# accepted outer step's state saved by release_ls; waits at most 8 h for the tail, 12 h cap on the run
{
W=/home/nathan/Source/choptuik-large-d-1088a
T=$W/out/fix/D1000_M48_tail
n=0
while [ $n -lt 1440 ]; do grep -q "^end " $T/run.log 2>/dev/null && break; sleep 20; n=$((n + 1)); done
grep -q "^rc 0" $T/run.log || exit 1
S=$T/release_ls_h23_D1000.0000.npz
[ -s $S ] || exit 2
cd $W/hp || exit 3
PY=$(cat $W/python_path)
export HP_EXACT_RECIP=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_x
O=$W/out/fix/D1000_M48_tail2
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
timeout 12h $PY -u form_s.py release_ls $S $O --harm 25,27,29,31,33,35,37 --kmax 37 \
  --jac_by 25:qq,27:qq,29:qq,31:qq,33:qq,35:qq,37:qq --res od --tol 1e-48 --tol_h 1e-44 --threads 8 --outer 8 \
  --commit f350aa62 --allow_unraw > $O/rls.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
