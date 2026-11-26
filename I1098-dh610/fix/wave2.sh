#!/bin/bash
# #1098 wave 2 on dh610 (fastmul5 f350aa62 in site_x: lane-precision reciprocals, relaxed horizon products):
# recip_check at D 300 and D 1000 first (PASS needed: a halved-step plan moves the od residual by at most 1e-44 with the
# fix, the control above 1e-40), then D1000_base, D1000_steps2 and D1000_M48 together (4 threads each), then the D 1000
# M 48 tail h15..h23 from D1000_M48's state; release_ls with the qq Jacobian, the octo-double residual, tol 1e-48
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
grep -q "def exact_recip" form_s.py || exit 1
[ -s $W/site_x/hpkernel/__init__.py ] || exit 1
PY=$(cat $W/python_path)
export HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_x
O=$W/out/fix
mkdir -p $O
for st in $W/out/budget300_src/D300_full_base.npz $W/out/rls1000h13q/release_ls_h13_D1000.0000.npz; do
  $PY -u recip_check.py $st --threads 4 >> $O/recip_check.log 2>&1 || { echo "recip_check FAIL on $st" >> $O/recip_check.log; exit 2; }
done
export HP_EXACT_RECIP=1
run() {  # name state harms kmax jac_by
  mkdir -p $O/$1
  date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/$1/run.log
  $PY -u form_s.py release_ls $2 $O/$1 --harm $3 --kmax $4 --jac_by $5 --res od --tol 1e-48 --tol_h 1e-44 --threads 4 \
    --outer 8 --commit f350aa62 --allow_unraw > $O/$1/rls.log 2>&1
  echo "rc $?" >> $O/$1/run.log
  date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/$1/run.log
}
run D1000_base $W/out/budget1000_src/D1000_full_base.npz 13 13 13:qq &
run D1000_steps2 $W/out/budget1000_src/D1000_full_steps2.npz 13 13 13:qq &
run D1000_M48 $W/out/budget1000_src/D1000_full13_M48.npz 13 13 13:qq &
wait
[ -s $O/D1000_M48/release_ls_h13_D1000.0000.npz ] && run D1000_M48_tail $O/D1000_M48/release_ls_h13_D1000.0000.npz \
  15,17,19,21,23 31 15:qq,17:qq,19:qq,21:qq,23:qq
exit
}
