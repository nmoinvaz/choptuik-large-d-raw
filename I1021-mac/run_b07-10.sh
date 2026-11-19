#!/bin/bash
# I1021-mac: the recount's restart on boxes 7-10 (stopped 2026-11-19 14:32 UTC in box 7 for the split), code 068913b4
cd /Users/nathan/Source/choptuik-large-d-1021run/solver/inner_stokes || exit 1
[ "$(git rev-parse HEAD)" = 068913b45669b01c74d5dbcba628f3b752d26d3a ] || { echo "not at 068913b4"; exit 1; }
PY=/Users/nathan/venv-314/bin/python
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/raw995/I1021-mac
{ echo "recount stopped 2026-11-19 14:32:41 UTC in box 7 (627 cache lines, all whole)"; echo "restart b07-10 $(date -u '+%F %T')"; $PY -c 'import sys, numpy, scipy, mpmath; print(sys.version.split()[0], numpy.__version__, scipy.__version__, mpmath.__version__)'; } >> $R/logs/exits.txt
nice -n 10 $PY -u argcount.py --M=3 --recount=$R/split/leaves_b07-10.jsonl --r1=0.17 --r1b=0.2 --seed=$R/m3/points_M3_r0.2.jsonl --m3fix --retry --procs=2 --out=$R/m3 --tag=M3_cand_r0.17_fix_b07-10 > $R/logs/recount_r0.17_fix_b07-10.log 2>&1; echo "recount b07-10 exit $? $(date -u '+%F %T')" >> $R/logs/exits.txt
echo "end $(date -u '+%F %T')" >> $R/logs/exits.txt
