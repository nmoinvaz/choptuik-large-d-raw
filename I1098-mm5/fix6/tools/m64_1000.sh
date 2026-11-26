#!/bin/bash
# #1098: D 1000 at M 64 on fastmul6, for the D 1000 record's err_xcheck_M: tail6b's M 48 state after h23 (I1098-mm5/fix6/
# D1000_M48_tail6b/release_ls_h23_D1000.0000.npz) resampled to M 64 (resample_m.py beside this script), then release_ls
# --harm 23,25,27,29,31 --kmax 31: h23's outer steps re-converge every lower harmonic at M 64 (its change against tail6b's
# after h23 is the M 48 -> 64 shift at kfree 23), then h25..h31 (the final against tail6b's final, the shift at kfree 31);
# qq, od, tol 1e-48, --ddelta 1e-25, THREADS threads, 8 h cap
#
#     m64_1000.sh STATE OUT THREADS
{
S=$1; O=$2; T=$3
HP=${HP:-$HOME/Source/choptuik-fastmul6/hp}
SITE=${SITE:-$HOME/Source/fastmul6-site}
PY=${PY:-$HOME/venv-314/bin/python}
EXTRA=${EXTRA:-}
TOOLS=$(cd "$(dirname "$0")" && pwd)
[ -s "$S" ] && [ -d "$O" ] && [ -n "$T" ] || { echo "usage: m64_1000.sh STATE OUT THREADS"; exit 1; }
cd $HP || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$SITE:$HP $PY $TOOLS/resample_m.py $S $O/h23_M64.npz 64 > $O/resample.log 2>&1 || exit 2
echo "resampled $(date -u +%H:%M:%S)" >> $O/run.log
nice -n 10 timeout 8h $PY -u form_s.py release_ls $O/h23_M64.npz $O --harm 23,25,27,29,31 --kmax 31 \
  --jac_by 23:qq,25:qq,27:qq,29:qq,31:qq --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads $T --outer 8 \
  --commit 478e9d86 $EXTRA > $O/rls.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
