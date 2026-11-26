#!/bin/bash
# after the fastmul6 build (rebuild_y.sh) and its checks: D 2000's full M 32 state (I1088-dh610/rls2000d: Moebius a 8,
# ks 2618, kfreeze 13, the double-double 1/k and d/dtheta) re-solved on fastmul6 (HP_EXACT_RECIP=1, HP_EXACT_DMAT=1),
# release_ls --harm 13 --kmax 13, qq, od, tol 1e-48, 6 threads, 4 h cap; its change is D 2000's dd-1/k and dd-d/dtheta
# terms together; waits at most 3 h for the build
{
W=/home/nathan/Source/choptuik-large-d-1088a
n=0
while [ $n -lt 540 ]; do grep -q "^end " $W/build_y.log 2>/dev/null && break; sleep 20; n=$((n + 1)); done
grep -q "^end " $W/build_y.log || exit 1
grep -q "exit=[^0]" $W/out/fastmul6_build/exit_codes.txt && exit 2
cd $W/hp_y || exit 3
PY=$(cat $W/python_path)
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_y
O=$W/out/fix6/D2000_base6
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
timeout 4h $PY -u form_s.py release_ls $W/out/rls2000d/release_ls_h13_D2000.0000.npz $O --harm 13 --kmax 13 --jac_by 13:qq \
  --res od --tol 1e-48 --tol_h 1e-44 --threads 6 --outer 8 --commit d368a0c0 --allow_unraw > $O/rls.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
