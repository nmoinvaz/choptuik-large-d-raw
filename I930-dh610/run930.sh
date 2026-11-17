#!/bin/bash
# #930 on dh610: the two test_stall.py runs of the issue, from hp/ of a worktree of origin/main (9cc648d2), with the hpkernel of
# #923's build (choptuik-large-d-923/.venv), 3 threads, nice 10. Exit codes go to exits_930.txt.
WT=/home/nathan/Source/choptuik-large-d-930
OUT=/home/nathan/Source/choptuik-large-d-raw/I930-dh610
PY=/home/nathan/Source/choptuik-large-d-923/.venv/bin/python
log() { echo "930 $1 $(date -u '+%F %T') UTC" >> $OUT/exits_930.txt; }
cd $WT/hp || exit 9
log "start, hp $(git rev-parse --short=8 HEAD), hpkernel $($PY -c 'import hpkernel; print(hpkernel.__file__)'), load $(cut -d' ' -f1-3 /proc/loadavg)"
export OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3
nice -n 10 $PY -u test_stall.py --cases 4 --threads 3 --mutate nostall > $OUT/nostall.log 2>&1
log "nostall exit $?"
nice -n 10 $PY -u test_stall.py --cases 4 --threads 3 > $OUT/plain.log 2>&1
log "plain exit $?"
