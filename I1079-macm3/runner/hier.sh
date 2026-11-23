#!/bin/bash
# #1079 macm3b: main's hier.py at M = 3 started at each excited zero (the coordinator's order, hc 2026-11-23 about 14:50 UTC): (1) python -u hier.py 3 A wf --x=B3,C3 --procs 2 --verbose=2 for x1 and x2 side by side (2 processes each),
# then (2) the same through hier_driver.py (full-precision x and r). From ~/Source/choptuik-large-d-1079/solver/inner_stokes (main at a4cd5eaa), nice 10, 1 thread per BLAS. Logs in $P/hier_out, records in $P/steps.txt. Own session under caffeinate -is.
{
P=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3
W=/Users/nathan/Source/choptuik-large-d-1079
MAIN=a4cd5eaa7b297ffc6f171551fa15ba054e970e21
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
H=$P/steps.txt
stamp() { date -u '+%F %T'; }
[ "$(git -C $W rev-parse HEAD)" = "$MAIN" ] && [ -z "$(git -C $W status --porcelain --untracked-files=no)" ] || { echo "$(stamp) STOP: the main worktree is not at $MAIN or has tracked changes" >> $H; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $W/solver/inner_stokes || exit 1
A1=3.446218246366727; W1=0.347606965217407; B1=0.8054175863852927; C1=0.011780043848505818
A2=3.526473056695715; W2=0.211497981391215; B2=0.9765085451976188; C2=-0.0017633195225818952
echo "hier start $(stamp)" >> $H
for phase in plain driver; do
  if [ $phase = plain ]; then SCRIPT=hier.py; else SCRIPT=$P/hier_driver.py; fi
  for n in 1 2; do
    eval "A=\$A$n; WF=\$W$n; B=\$B$n; C=\$C$n"
    echo "hier $phase x$n command: cd $W/solver/inner_stokes && nice -n 10 $PY -u $SCRIPT 3 $A $WF --x=$B,$C --procs 2 --verbose=2 > $P/hier_out/hier_${phase}_x$n.log 2>&1" >> $H
  done
  echo "hier $phase start $(stamp)" >> $H
  for n in 1 2; do
    eval "A=\$A$n; WF=\$W$n; B=\$B$n; C=\$C$n"
    ( nice -n 10 $PY -u $SCRIPT 3 $A $WF --x=$B,$C --procs 2 --verbose=2 > $P/hier_out/hier_${phase}_x$n.log 2>&1; echo "hier $phase x$n end $(stamp) exit $?: $(grep -E '^(ZERO|FIXED)' $P/hier_out/hier_${phase}_x$n.log | tail -1 | cut -c1-260)" >> $H ) &
  done
  wait
done
echo "hier done $(stamp)" >> $H
exit 0
}
