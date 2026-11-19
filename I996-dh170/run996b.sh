#!/bin/bash
# #996 on dh170, second launch (coordinator's hc and the issue's latest comment, 2026-11-19 about 02:00 UTC): the M = 9 job of run996.sh stopped at k = 1 ("matrix is numerically
# singular": the fit basis has 93 columns at M = 9 and is singular at 60 mpmath digits), fixed in main e4d70167 by a 5th argument, dps. Two more jobs beside run996.sh's M = 5 and
# M = 7 (60 digits, worktree choptuik-large-d-996 at 005b99f3, still running): (1) M = 9 at dps 120 and (2) the precision control M = 7 at dps 120, from a second worktree
# ~/Source/choptuik-large-d-996b at origin/main e4d70167 (so the running jobs' files are not touched), nice 10, 24 h timeout each. The JSON names get _dps120.
HERE=/home/nathan/Source/choptuik-large-d-raw/I996-dh170
WT=/home/nathan/Source/choptuik-large-d-996b
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
L=$HERE/exits_996.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1
one() {
  local M=$1 t=$(date +%s)
  echo "996 M${M}_dps120 start $(date -u '+%F %T') worktree $(git -C $WT rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" >> $L
  ( cd $WT/solver/proof && nice -n 10 timeout -s TERM 86400 /usr/bin/time -f "time %e s, max rss %M kB" $PY -u amp_trunc_hiermodel.py $M 18 1000 1.0 120 ) > $HERE/M${M}_dps120.log 2>&1
  local rc=$?
  cp -p $WT/solver/proof/trunc_hier_M${M}_K18_J1000_w1.0000_dps120.json $HERE/ 2>/dev/null
  echo "996 M${M}_dps120 exit $rc wall $(( $(date +%s) - t )) s $(date -u '+%F %T')" >> $L
}
for M in 9 7; do one $M & done
wait
