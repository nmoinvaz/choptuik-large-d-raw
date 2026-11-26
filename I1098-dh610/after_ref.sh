#!/bin/bash
# after site_r's build (#1098): the refinement test at D 300's base state (HP_SLAVE_REFINE_OD 4, 8, 12, 2), then the
# D 2000 M 48 test as unit i1088a-m48-2000; waits at most 3 h for the build
{
W=/home/nathan/Source/choptuik-large-d-1088a
n=0
while [ $n -lt 540 ]; do
  grep -q "^end " $W/build_ref.log 2>/dev/null && break
  sleep 20; n=$((n + 1))
done
grep -q "^end " $W/build_ref.log || exit 1
[ -s $W/site_r/hpkernel/__init__.py ] || exit 2
O=$W/out/refine300
mkdir -p $O
PY=$(cat $W/python_path)
S=$W/out/budget300_src/D300_full_base.npz
for r in 4 8 12 2; do
  if [ $r = 4 ]; then
    HP_SLAVE_REFINE_OD=4 PYTHONPATH=$W/site_r OPENBLAS_NUM_THREADS=1 $PY $W/refine_test.py $S $O/F_r4.npz >> $O/refine.log 2>&1
  else
    HP_SLAVE_REFINE_OD=$r PYTHONPATH=$W/site_r OPENBLAS_NUM_THREADS=1 $PY $W/refine_test.py $S $O/F_r$r.npz $O/F_r4.npz >> $O/refine.log 2>&1
  fi
done
S2=$W/out/budget300_src/D300_full_steps2.npz
[ -s $S2 ] && HP_SLAVE_REFINE_OD=12 PYTHONPATH=$W/site_r OPENBLAS_NUM_THREADS=1 $PY $W/refine_test.py $S2 $O/F_steps2_r12.npz >> $O/refine.log 2>&1
[ -s $S2 ] && HP_SLAVE_REFINE_OD=4 PYTHONPATH=$W/site_r OPENBLAS_NUM_THREADS=1 $PY $W/refine_test.py $S2 $O/F_steps2_r4.npz $O/F_steps2_r12.npz >> $O/refine.log 2>&1
systemd-run --user --unit=i1088a-m48-2000 --working-directory=$W nice -n 10 timeout 30h $W/run_m48_2000.sh
exit
}
