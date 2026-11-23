#!/bin/bash
# #1025 reconv_d1975 (dh610), step 1 or 2 of the coordinator's re-convergence test of 23 Nov (the #1025 comment of 07:00 UTC): ell_refine.py with k_c equal to k_c_src (87 and 87), so no regrid and only the LM
# iterations, on one of the two accepted k_c 87 D 19.75 states, on Linux. usage: bash lane_reconv_refine.sh lin|mac
#   lin: ell_refine.py l1kc87dh170d1975 87 l1kc87linRe 87 1 19.75 2.1120935738 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma   (dh170's state 352107a8, record 6078a0b4)
#   mac: the same with src l1kc87macm3d1975 and tag l1kc87macRe                                                                                      (macm3's state 5825f5d0, record 84f75a48)
# 8 threads, nice 10, in solver/matter of the worktree ~/Source/choptuik-large-d-1025g at 48c36355 (the code that made both states: dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; ell_refine.py blob 631e5801), cap
# 21600 s (a time cap only). The state is copied into data/ under its tag and checked by blob. Free memory: refuses to start with less than 8 GiB available; nothing is stopped or terminated for memory (Nathan's rule
# of 2026-11-08): below 4 GiB the sampler only writes <lin|mac>/MEMALERT.txt, which the runner session posts to the coordinator. The result (state and record) goes to in/ with its blobs in in_blobs_reconv_<lin|mac>.txt.
{
set -u
W=${1:?lin or mac}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/reconv_d1975; IN=$F/in; OUT=$F/$W
WT=/home/nathan/Source/choptuik-large-d-1025g; WTM=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
D=19.75; LAM0=2.1120935738; MEMSTART=8388608; MEMSTOP=4194304
case $W in
  lin) SRC=l1kc87dh170d1975; TAG=l1kc87linRe; SB=352107a8e35e42d1cb0622a57a51132128f882ae; RB=6078a0b48e5fc09a2872aa0c6c5a6347aa173e78;;
  mac) SRC=l1kc87macm3d1975; TAG=l1kc87macRe; SB=5825f5d00f50a068c244d08e5b66847c207ebd99; RB=84f75a48beb7e245145ce8f0cf81cd0b425fdb00;;
  *) echo "usage: lin or mac"; exit 2;;
esac
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8
mkdir -p $OUT
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" | tee -a $OUT/steps.txt; }
stop() { echo "REFUSED: $*" > $OUT/DONE.txt; step "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
av0=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
step "start $W (load $(cut -d' ' -f1-3 /proc/loadavg), MemAvailable $av0 kB)"
[ "$av0" -ge $MEMSTART ] || stop "MemAvailable $av0 kB is below 8 GiB"
[ "$(blob $IN/sol_${SRC}_D19.7500.npy)" = $SB ] || stop "$IN/sol_${SRC}_D19.7500.npy is not blob $SB"
[ "$(blob $IN/$SRC.jsonl)" = $RB ] || stop "$IN/$SRC.jsonl is not blob $RB"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(blob $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] || stop "ell_refine.py is not blob 631e5801"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
[ -e $WTM/data/$TAG.jsonl ] && stop "$WTM/data/$TAG.jsonl exists"
[ -e $WTM/data/sol_${TAG}_D19.7500.npy ] && stop "$WTM/data/sol_${TAG}_D19.7500.npy exists"
L0=$($PY -c "import sys; sys.path.insert(0, '$WTM'); import ell_delta; print(round(ell_delta.lam0_at($D, *ell_delta.lam0_table())[0], 10))")
[ "$L0" = "$LAM0" ] || stop "lambda_0(19.75) reads $L0, not $LAM0"
# the source state under its tag in data/, checked by blob
if [ -e $WTM/data/sol_${SRC}_D19.7500.npy ]; then
  [ "$(blob $WTM/data/sol_${SRC}_D19.7500.npy)" = $SB ] || stop "data/sol_${SRC}_D19.7500.npy exists and is not blob $SB"
else
  cp $IN/sol_${SRC}_D19.7500.npy $WTM/data/sol_${SRC}_D19.7500.npy
  [ "$(blob $WTM/data/sol_${SRC}_D19.7500.npy)" = $SB ] || stop "copied source state blob differs"
fi
step "pins checked (state $SB, record $RB, worktree 48c36355, ell_refine.py 631e5801, lambda_0(19.75) $L0, $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')); source in data/ checked by blob"
CMD="nice -n 10 timeout 21600 $PY -u ell_refine.py $SRC 87 $TAG 87 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 8 threads, nice 10, cap 21600 s): $CMD" > $OUT/refine.log
step "ell_refine starts: $CMD"
( while sleep 60; do
    echo "$(stamp),$(ps -C python -o rss=,pcpu=,nlwp=,args= | grep "ell_refine.py $SRC " | grep -v grep | head -1 | cut -d' ' -f1-4)" >> $OUT/samples.csv
    av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    [ "$av" -lt $MEMSTOP ] && echo "$(stamp) UTC MemAvailable $av kB below 4 GiB (alert only; nothing is stopped)" >> $OUT/MEMALERT.txt
  done ) &
SAMP=$!
t0=$(date +%s)
( cd $WTM && $CMD >> $OUT/refine.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
wall=$(( $(date +%s) - t0 ))
step "ell_refine exit $rc, wall $wall s"
[ $rc = 0 ] || stop "ell_refine exit $rc (0 wanted; 124 is the cap)"
[ -s $WTM/data/$TAG.jsonl ] && [ -s $WTM/data/sol_${TAG}_D19.7500.npy ] || stop "ell_refine wrote no record or state"
cp $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.7500.npy $IN/
{ echo "$(blob $IN/sol_${TAG}_D19.7500.npy) sol_${TAG}_D19.7500.npy"; echo "$(blob $IN/$TAG.jsonl) $TAG.jsonl"; } > $F/in_blobs_reconv_$W.txt
echo "DONE exit 0, wall $wall s, $(stamp) UTC" > $OUT/DONE.txt
step "done: $(cat $F/in_blobs_reconv_$W.txt | tr '\n' ';')"
exit 0
}
