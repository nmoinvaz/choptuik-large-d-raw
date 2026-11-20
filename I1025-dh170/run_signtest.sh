#!/bin/bash
# #1025 on dh170: signtest of the four k_c 55 records (coordinator's hc, 2026-11-20 about 08:30 UTC). One D at a time, 4 BLAS threads, nice 10, timeout 7200 each.
HERE=/home/nathan/Source/choptuik-large-d-raw/I1025-dh170
ST=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/026ace6b-8e85-4de1-9fd2-85ec04d52786/scratchpad/ST1025
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
LOG=$HERE/signtest.log
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4
cd /home/nathan/Source/choptuik-large-d-1025st/solver/matter || exit 9
for pair in "15 15.0000" "15.5 15.5000" "16 16.0000" "16.5 16.5000"; do
  set -- $pair; D=$1; DDDD=$2
  echo "=== D $D start $(date -u '+%F %T') UTC" >> $LOG
  nice -n 10 timeout 7200 $PY -u $ST/signtest.py $ST/sol_l1kc55Fb1025_D${DDDD}.npy $D 55 around=$ST/l1kc55Fb1025.jsonl:$D:0.02 >> $LOG 2>&1
  echo "=== D $D exit $? $(date -u '+%F %T') UTC" >> $LOG
done
echo "=== all done $(date -u '+%F %T') UTC" >> $LOG
