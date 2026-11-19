#!/bin/bash
# #996 on dh170, fourth launch (coordinator's hc, 2026-11-19: "go on both 180-digit runs"): the 1.7% disagreement of sigma_7 (an exact order for both) between M 7 and M 9 at 120 digits
# needs a higher-digit run of each: `amp_trunc_hiermodel.py M 15 1000 1.0 180` for M = 7 and 9, K 15 (sigma_0 .. sigma_7), one single-process job each, nice 10, 24 h timeout each,
# worktree ~/Source/choptuik-large-d-996c at origin/main 2d393061 (no job of it is running now). JSON names get _K15_..._dps180.
HERE=/home/nathan/Source/choptuik-large-d-raw/I996-dh170
WT=/home/nathan/Source/choptuik-large-d-996c
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
L=$HERE/exits_996.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1
one() {   # M
  local M=$1 name=M${1}_K15_dps180 t=$(date +%s)
  echo "996 $name start $(date -u '+%F %T') worktree $(git -C $WT rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" >> $L
  ( cd $WT/solver/proof && nice -n 10 timeout -s TERM 86400 /usr/bin/time -f "time %e s, max rss %M kB" $PY -u amp_trunc_hiermodel.py $M 15 1000 1.0 180 ) > $HERE/$name.log 2>&1
  local rc=$?
  cp -p $WT/solver/proof/trunc_hier_M${M}_K15_J1000_w1.0000_dps180.json $HERE/ 2>/dev/null
  echo "996 $name exit $rc wall $(( $(date +%s) - t )) s $(date -u '+%F %T')" >> $L
}
one 7 &
one 9 &
wait
