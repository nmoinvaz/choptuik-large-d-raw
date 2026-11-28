#!/bin/bash
# #1109 stage 1d, one state: jac, svd, report, valley (--ts=1e-3), each under timeout 7200, 2 threads, nice 10. Logs in d/.
#   run_d.sh TAG REC STATE        (REC, STATE file names in d/in/)
{
TAG=$1; REC=$HOME/Source/choptuik-large-d-raw/I1109-mm5/d/in/$2; ST=$HOME/Source/choptuik-large-d-raw/I1109-mm5/d/in/$3
Dd=$HOME/Source/choptuik-large-d-raw/I1109-mm5/d
W=$HOME/Source/choptuik-1109/solver/matter
PY=$HOME/venv-314/bin/python
export OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 VECLIB_MAXIMUM_THREADS=2
SB=$(git hash-object --no-filters $ST); RB=$(git hash-object --no-filters $REC)
cd $W || exit 1
L=$Dd/run_$TAG.log; t0=$(date +%s)
echo "start $TAG $(date -u '+%Y-%m-%d %H:%M:%S UTC'): state $SB rec $RB" >> $L
nice -n 10 timeout 7200 $PY i1101_weakdir.py jac $REC $ST 23.0 $Dd/jac_$TAG.npz --pin=$SB,$RB > $Dd/jac_$TAG.log 2>&1
rc=$?; echo "jac rc $rc $(( $(date +%s) - t0 )) s" >> $L
if [ $rc != 0 ] || ! grep -q "the record system" $Dd/jac_$TAG.log; then echo "SKIPPED $TAG: jac printed not the record system (rc $rc): $(head -n 2 $Dd/jac_$TAG.log | cut -c1-200 | tr '\n' ' ')" >> $L; exit 3; fi
nice -n 10 timeout 7200 $PY i1101_weakdir.py svd $Dd/jac_$TAG.npz $Dd/svd_$TAG.npz > $Dd/svd_$TAG.log 2>&1
echo "svd rc $? $(( $(date +%s) - t0 )) s" >> $L
nice -n 10 timeout 7200 $PY i1101_weakdir.py report $Dd/jac_$TAG.npz $Dd/svd_$TAG.npz 23.0 $TAG=$REC:$ST --out=$Dd/rep_$TAG.json > $Dd/report_$TAG.log 2>&1
echo "report rc $? $(( $(date +%s) - t0 )) s" >> $L
nice -n 10 timeout 7200 $PY i1101_weakdir.py valley $Dd/jac_$TAG.npz $Dd/svd_$TAG.npz $REC $ST 23.0 --ts=1e-3 > $Dd/valley_$TAG.log 2>&1
echo "valley rc $? $(( $(date +%s) - t0 )) s" >> $L
echo "done $TAG $(date -u '+%Y-%m-%d %H:%M:%S UTC') total $(( $(date +%s) - t0 )) s" >> $L
exit
}
