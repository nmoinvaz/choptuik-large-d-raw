#!/bin/bash
# #1079 macm3b step 1: F_3 at each excited zero, value_mp.py point A WF <F_3 of the nearest valued cache record>, 2 processes (one per zero), nice 10, 1 thread per BLAS.
# Code ~/Source/choptuik-inner-mp at 79d4af3b. Records in $P/steps.txt; the rows in $P/point_x1.json and point_x2.json.
{
P=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3
CODE=/Users/nathan/Source/choptuik-inner-mp
CODE1=79d4af3b47ea39310ab5263f63ff3b8f1609f6eb
IS=$CODE/solver/inner_stokes
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
H=$P/steps.txt
stamp() { date -u '+%F %T'; }
[ "$(git -C $CODE rev-parse HEAD)" = "$CODE1" ] && [ -z "$(git -C $CODE status --porcelain -- solver)" ] || { echo "$(stamp) STOP: the code worktree is not at $CODE1 or has local changes in solver" >> $H; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
# x1: zero (3.446218246366727, 0.347606965217407); nearest valued record (3.55248231875, 0.41279321)
A1=3.446218246366727; W1=0.347606965217407; F1R=0.006042995233562286; F1I=-0.3800117921568823
# x2: zero (3.526473056695715, 0.211497981391215); nearest valued record (3.526359271875, 0.21279321)
A2=3.526473056695715; W2=0.211497981391215; F2R=-0.0009128684534629451; F2I=-0.48753546856333585
echo "step1 x1 command: cd $IS && nice -n 10 $PY -u value_mp.py point $A1 $W1 $F1R $F1I > $P/point_x1.json 2> $P/point_x1.err" >> $H
echo "step1 x2 command: cd $IS && nice -n 10 $PY -u value_mp.py point $A2 $W2 $F2R $F2I > $P/point_x2.json 2> $P/point_x2.err" >> $H
echo "step1 start $(stamp)" >> $H
(cd $IS && nice -n 10 $PY -u value_mp.py point $A1 $W1 $F1R $F1I > $P/point_x1.json 2> $P/point_x1.err; echo "step1 x1 end $(stamp) exit $?" >> $H) &
(cd $IS && nice -n 10 $PY -u value_mp.py point $A2 $W2 $F2R $F2I > $P/point_x2.json 2> $P/point_x2.err; echo "step1 x2 end $(stamp) exit $?" >> $H) &
wait
echo "step1 done $(stamp)" >> $H
exit 0
}
