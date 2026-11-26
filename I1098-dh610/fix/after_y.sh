#!/bin/bash
# after the fastmul6 build (rebuild_y.sh) and its checks: D 300's u and Moebius full states re-solved on fastmul6 with
# the d/dtheta remainders (HP_EXACT_DMAT=1), release_ls --harm 13 --kmax 13, qq, od, tol 1e-48, 3 threads each; their
# difference is the u-against-Moebius term with the remainders; waits at most 3 h for the build
{
W=/home/nathan/Source/choptuik-large-d-1088a
n=0
while [ $n -lt 540 ]; do grep -q "^end " $W/build_y.log 2>/dev/null && break; sleep 20; n=$((n + 1)); done
grep -q "^end " $W/build_y.log || exit 1
grep -q "exit=[^0]" $W/out/fastmul6_build/exit_codes.txt && exit 2
cd $W/hp_y || exit 3
PY=$(cat $W/python_path)
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_y
O=$W/out/fix6
mkdir -p $O
run() {  # name state
  mkdir -p $O/$1
  date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/$1/run.log
  timeout 2h $PY -u form_s.py release_ls $2 $O/$1 --harm 13 --kmax 13 --jac_by 13:qq --res od --tol 1e-48 --tol_h 1e-44 \
    --threads 3 --outer 8 --commit d368a0c0 --allow_unraw > $O/$1/rls.log 2>&1
  echo "rc $?" >> $O/$1/run.log
  date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/$1/run.log
}
run D300_u6 $W/out/budget300_src/D300_full_base.npz &
run D300_mob6 "$W/out/budget300_src/D300_full_mob8,ks=600.npz" &
wait
exit
}
