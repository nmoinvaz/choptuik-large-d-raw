#!/bin/bash
# #1079 macm3b step 3: certify_M.py plan --centre=data/A_M_refine_M3_xN.json (numerics, seconds), then box 3 --centre=<refine json> --use_out --h=1e-10 --w=4e-16 --out=data/A_M_box_M3xN_1e-10.json
# --log=logs/A_M_box_M3xN_1e-10.log for N = 1 and 2 in parallel (2 processes), from main's solver/proof (worktree ~/Source/choptuik-large-d-1079 at a4cd5eaa), nice 10, 1 thread per BLAS.
# A box run that exits nonzero writes a STOP line (cause = the last lines of its stdout log); the run is not repeated and nothing is changed. Records in $P/steps.txt. Own session under caffeinate -is.
{
P=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3
W=/Users/nathan/Source/choptuik-large-d-1079
MAIN=a4cd5eaa7b297ffc6f171551fa15ba054e970e21
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
H=$P/steps.txt
stamp() { date -u '+%F %T'; }
[ "$(git -C $W rev-parse HEAD)" = "$MAIN" ] && [ -z "$(git -C $W status --porcelain --untracked-files=no)" ] || { echo "$(stamp) STOP: the main worktree is not at $MAIN or has tracked changes" >> $H; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $W/solver/proof || exit 1
for n in 1 2; do
  [ -f data/A_M_refine_M3_x$n.json ] || { echo "$(stamp) STOP: data/A_M_refine_M3_x$n.json is missing" >> $H; exit 1; }
  [ ! -e data/A_M_box_M3x${n}_1e-10.json ] || { echo "$(stamp) STOP: data/A_M_box_M3x${n}_1e-10.json exists" >> $H; exit 1; }
  echo "plan x$n command: cd $W/solver/proof && nice -n 10 $PY certify_M.py plan --centre=data/A_M_refine_M3_x$n.json > logs/A_M_plan_M3x$n.log 2>&1" >> $H
  nice -n 10 $PY certify_M.py plan --centre=data/A_M_refine_M3_x$n.json > logs/A_M_plan_M3x$n.log 2>&1; echo "plan x$n end $(stamp) exit $?" >> $H
done
for n in 1 2; do
  echo "box x$n command: cd $W/solver/proof && nice -n 10 $PY certify_M.py box 3 --centre=data/A_M_refine_M3_x$n.json --use_out --h=1e-10 --w=4e-16 --out=data/A_M_box_M3x${n}_1e-10.json --log=logs/A_M_box_M3x${n}_1e-10.log > logs/A_M_box_M3x${n}_1e-10_stdout.log 2>&1" >> $H
done
echo "box start $(stamp)" >> $H
for n in 1 2; do
  ( nice -n 10 $PY certify_M.py box 3 --centre=data/A_M_refine_M3_x$n.json --use_out --h=1e-10 --w=4e-16 --out=data/A_M_box_M3x${n}_1e-10.json --log=logs/A_M_box_M3x${n}_1e-10.log > logs/A_M_box_M3x${n}_1e-10_stdout.log 2>&1; rc=$?
    echo "box x$n end $(stamp) exit $rc: $(tail -1 logs/A_M_box_M3x${n}_1e-10_stdout.log | cut -c1-250)" >> $H
    [ $rc = 0 ] || echo "$(stamp) STOP: box x$n exit $rc: $(tail -3 logs/A_M_box_M3x${n}_1e-10_stdout.log | tr '\n' ' ' | cut -c1-500)" >> $H ) &
done
wait
echo "box done $(stamp)" >> $H
exit 0
}
