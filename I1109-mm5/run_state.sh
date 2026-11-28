#!/bin/bash
# #1109 stage 1, one state: jac, svd, report, valley, each under timeout 3600, 2 threads, nice 10; logs in this folder.
#     run_state.sh TAG D REC STATE        (TAG names the files: jac_TAG.npz, svd_TAG.npz, rep_TAG.json, *_TAG.log)
{
TAG=$1; D=$2; REC=$3; ST=$4
H=$HOME/Source/choptuik-large-d-raw/I1109-mm5
W=$HOME/Source/choptuik-1109/solver/matter
PY=$HOME/venv-314/bin/python
export OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 VECLIB_MAXIMUM_THREADS=2
SB=$(git hash-object --no-filters $H/in/$ST); RB=$(git hash-object --no-filters $H/in/$REC)
cd $W || exit 1
t0=$(date +%s); echo "start $TAG D $D $(date -u '+%Y-%m-%d %H:%M:%S UTC'): state $SB rec $RB" >> $H/run_$TAG.log
nice -n 10 timeout 3600 $PY i1101_weakdir.py jac $H/in/$REC $H/in/$ST $D $H/jac_$TAG.npz --pin=$SB,$RB > $H/jac_$TAG.log 2>&1
echo "jac rc $? $(( $(date +%s) - t0 )) s" >> $H/run_$TAG.log
nice -n 10 timeout 3600 $PY i1101_weakdir.py svd $H/jac_$TAG.npz $H/svd_$TAG.npz > $H/svd_$TAG.log 2>&1
echo "svd rc $? $(( $(date +%s) - t0 )) s" >> $H/run_$TAG.log
nice -n 10 timeout 3600 $PY i1101_weakdir.py report $H/jac_$TAG.npz $H/svd_$TAG.npz $D base=$H/in/$REC:$H/in/$ST --out=$H/rep_$TAG.json > $H/report_$TAG.log 2>&1
echo "report rc $? $(( $(date +%s) - t0 )) s" >> $H/run_$TAG.log
nice -n 10 timeout 3600 $PY i1101_weakdir.py valley $H/jac_$TAG.npz $H/svd_$TAG.npz $H/in/$REC $H/in/$ST $D --ts=1e-3 > $H/valley_$TAG.log 2>&1
echo "valley rc $? $(( $(date +%s) - t0 )) s" >> $H/run_$TAG.log
echo "done $TAG $(date -u '+%Y-%m-%d %H:%M:%S UTC') total $(( $(date +%s) - t0 )) s" >> $H/run_$TAG.log
exit
}
