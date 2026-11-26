#!/bin/bash
# #1098: release_ls's inner chord steps (e1cd7a84, hp_y2) against fresh Jacobians: D 300's tail h15 and h17 from
# fastmul6's D300_mob6 state, 2 threads each, side by side; Delta and the times compared from the logs
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp_y2 || exit 1
grep -q 'inner_chord="1"' form_s.py || exit 1
PY=$(cat $W/python_path)
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_y
O=$W/out/chord_test
for c in 1 0; do
  mkdir -p $O/c$c
  ( date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/c$c/run.log
    timeout 2h $PY -u form_s.py release_ls $W/out/ladder/inputs/S300.npz $O/c$c --harm 15,17 --kmax 31 --jac_by 15:qq,17:qq \
      --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --inner_chord $c --threads 2 --outer 8 --commit e1cd7a84 \
      --allow_unraw > $O/c$c/rls.log 2>&1
    echo "rc $?" >> $O/c$c/run.log
    date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/c$c/run.log ) &
done
wait
exit
}
