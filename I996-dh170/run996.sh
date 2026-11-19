#!/bin/bash
# #996 on dh170: solver/proof/amp_trunc_hiermodel.py M 18 1000 1.0 for M = 3, 5, 7 and 9, one single-process job each, in parallel at nice 10, each capped at 24 h
# (timeout -s TERM 86400). Worktree ~/Source/choptuik-large-d-996 (origin/main 005b99f3), Python of ~/Source/choptuik-large-d-935/.venv (3.14.10, mpmath 1.3.0,
# python-flint 0.9.0). Each job writes M<M>.log (stdout, unbuffered: one line per odd k with sigma_{(k-1)/2}, the fit residual and the seconds since the job's
# start) and, when it finishes, the script's own trunc_hier_M<M>_K18_J1000_w1.0000.json in solver/proof/ of the worktree, copied here. exits_996.txt gets
# "996 M<M> start/exit" lines with the wall seconds. usage: bash run996.sh
HERE=/home/nathan/Source/choptuik-large-d-raw/I996-dh170
WT=/home/nathan/Source/choptuik-large-d-996
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
L=$HERE/exits_996.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1
one() {
  local M=$1 t=$(date +%s)
  echo "996 M$M start $(date -u '+%F %T') pid $$ hp-free python, worktree $(git -C $WT rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" >> $L
  ( cd $WT/solver/proof && nice -n 10 timeout -s TERM 86400 /usr/bin/time -f "time %e s, max rss %M kB" $PY -u amp_trunc_hiermodel.py $M 18 1000 1.0 ) > $HERE/M$M.log 2>&1
  local rc=$?
  cp -p $WT/solver/proof/trunc_hier_M${M}_K18_J1000_w1.0000.json $HERE/ 2>/dev/null
  echo "996 M$M exit $rc wall $(( $(date +%s) - t )) s $(date -u '+%F %T')" >> $L
}
for M in 3 5 7 9; do one $M & done
wait
