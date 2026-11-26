#!/bin/bash
# #1098 on fastmul6 (wip/large-d-fastmul6: d368a0c0's kernel, f1b3cb8b's Python): the D 300 u-against-Moebius gap with
# the d/dtheta remainders, D 1000's remainder term by a direct re-solve, and M 32 -> 48 at kfree 13 on fastmul6. Then the
# D 1000 M 48 tail h15..h31 on fastmul6. release_ls --harm 13 --kmax 13, qq, od, tol 1e-48; 1 h cap at D 300, 3 h at D 1000.
#
#     fix6_mm5.sh IN_DIR OUT_DIR
#
# IN_DIR holds D300_full_base.npz (blob 569779b2), D300_full_mob8,ks=600.npz (b8e2b000), D1000_base.npz (57af5b81,
# I1098-dh610/fix/D1000_base/release_ls_h13_D1000.0000.npz) and D1000_M48.npz (a3735a1f, I1098-dh610/fix/D1000_M48/...)
{
I=$1
O=$2
HP=$HOME/Source/choptuik-fastmul6/hp
SITE=$HOME/Source/fastmul6-site
PY=$HOME/venv-314/bin/python
[ -d "$I" ] && [ -d "$O" ] || { echo "usage: fix6_mm5.sh IN_DIR OUT_DIR"; exit 1; }
cd $HP || exit 1
grep -q "def kernel_dmats" taylor_mp_check.py || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
$PY -u taylor_mp_check.py $I/D300_full_base.npz > $O/taylor300_dmat1.log 2>&1
echo "taylor_mp_check HP_EXACT_DMAT=1 exit=$?" >> $O/exit_codes.txt
HP_EXACT_DMAT=0 $PY -u taylor_mp_check.py $I/D300_full_base.npz > $O/taylor300_dmat0.log 2>&1
echo "taylor_mp_check HP_EXACT_DMAT=0 exit=$?" >> $O/exit_codes.txt
run() {  # name state threads cap harms kmax jac_by
  mkdir -p $O/$1
  date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/$1/run.log
  nice -n 10 timeout $4 $PY -u form_s.py release_ls $2 $O/$1 --harm $5 --kmax $6 --jac_by $7 --res od --tol 1e-48 \
    --tol_h 1e-44 --threads $3 --outer 8 --commit d368a0c0 > $O/$1/rls.log 2>&1
  echo "rc $?" >> $O/$1/run.log
  date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/$1/run.log
}
run D300_u6 $I/D300_full_base.npz 3 1h 13 13 13:qq &
run D300_mob6 "$I/D300_full_mob8,ks=600.npz" 3 1h 13 13 13:qq &
run D1000_base6 $I/D1000_base.npz 4 3h 13 13 13:qq &
run D1000_M48_6 $I/D1000_M48.npz 6 3h 13 13 13:qq &
wait
S=$O/D1000_M48_6/release_ls_h13_D1000.0000.npz
[ -s $S ] && run D1000_M48_tail6 $S 16 12h 15,17,19,21,23,25,27,29,31 31 \
  15:qq,17:qq,19:qq,21:qq,23:qq,25:qq,27:qq,29:qq,31:qq
exit
}
