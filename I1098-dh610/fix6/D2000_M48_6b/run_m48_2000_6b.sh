#!/bin/bash
# #1098 on fastmul6 (site_y, hp_y): D 2000 at M 48 from D2000_M48_6's released h13 state, with the Moebius ks raised from
# 2618 (1.31n) to 3417 (1.5n + 420), h13 re-converged at that ks (its change is the ks term at kfree 13), then the tail
# h15..h31 (kmax 31), qq, od, tol 1e-48, --ddelta 1e-25, 8 threads, 16 h cap
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp_y || exit 1
PY=$(cat $W/python_path)
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_y
O=$W/out/fix6/D2000_M48_6b
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$W/site_y:$W/hp_y $PY $W/out/ladder/variant_state.py $W/hp_y $W/out/fix6/D2000_M48_6/release_ls_h13_D2000.0000.npz \
  $O/start.npz ks=3417 >> $O/run.log 2>&1 || exit 2
timeout 16h $PY -u form_s.py release_ls $O/start.npz $O --harm 13,15,17,19,21,23,25,27,29,31 --kmax 31 \
  --jac_by 13:qq,15:qq,17:qq,19:qq,21:qq,23:qq,25:qq,27:qq,29:qq,31:qq --res od --tol 1e-48 --tol_h 1e-44 \
  --ddelta 1e-25 --threads 8 --outer 8 --commit 478e9d86 --allow_unraw > $O/rls.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
