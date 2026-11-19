#!/bin/bash
# #996 on dh170, third launch (coordinator's hc, 2026-11-19 about 02:20 UTC), after the control showed the 60-digit M 7 run wrong (sigma_1, sigma_2 off by 1.6e-6 and 6.6e-6 while the
# fit residual read 1e-61; the 60-digit M 7 job, pid 487040, was stopped at 02:22:40 UTC, exit 143, 3267 s, its log kept to k 11). Three more jobs from a third worktree
# ~/Source/choptuik-large-d-996c at origin/main 2d393061 (code as e4d70167, docstring only): (a) M 5 at 120 digits, to be compared with the 60-digit M 5 run that keeps running,
# (b) M 3 at 120 digits, (c) M 9's own precision control, K 9 at 180 digits, against the 120-digit M 9. nice 10, 24 h timeout each.
HERE=/home/nathan/Source/choptuik-large-d-raw/I996-dh170
WT=/home/nathan/Source/choptuik-large-d-996c
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
L=$HERE/exits_996.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1
one() {   # NAME M K DPS
  local name=$1 M=$2 K=$3 D=$4 t=$(date +%s)
  echo "996 $name start $(date -u '+%F %T') worktree $(git -C $WT rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" >> $L
  ( cd $WT/solver/proof && nice -n 10 timeout -s TERM 86400 /usr/bin/time -f "time %e s, max rss %M kB" $PY -u amp_trunc_hiermodel.py $M $K 1000 1.0 $D ) > $HERE/$name.log 2>&1
  local rc=$?
  cp -p $WT/solver/proof/trunc_hier_M${M}_K${K}_J1000_w1.0000_dps${D}.json $HERE/ 2>/dev/null
  echo "996 $name exit $rc wall $(( $(date +%s) - t )) s $(date -u '+%F %T')" >> $L
}
one M5_dps120 5 18 120 &
one M3_dps120 3 18 120 &
one M9_K9_dps180 9 9 180 &
wait
