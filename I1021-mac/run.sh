#!/bin/bash
# I1021-mac: the recount of #1013's 32 cells at xi1 0.17 with --m3fix --retry, then the planted run; code 068913b4
cd /Users/nathan/Source/choptuik-large-d-1021/solver/inner_stokes
PY=/Users/nathan/venv-314/bin/python
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/raw995/I1021-mac
: > $R/logs/exits.txt
nice -n 10 $PY -u argcount.py --selftest > $R/logs/selftest.log 2>&1; echo "selftest exit $?" >> $R/logs/exits.txt
nice -n 10 $PY -u argcount.py --M=3 --recount=$R/m3/leaves_M3_cand_r0.25.jsonl --r1=0.17 --r1b=0.2 --seed=$R/m3/points_M3_r0.2.jsonl --m3fix --retry --procs=2 --out=$R/m3 --tag=M3_cand_r0.17_fix > $R/logs/recount_r0.17_fix.log 2>&1; echo "recount exit $?" >> $R/logs/exits.txt
nice -n 10 $PY -u argcount.py --M=3 --recount=$R/m3/leaves_M3_cand_r0.25.jsonl --r1=0.17 --r1b=0.2 --seed=$R/m3/points_M3_r0.2.jsonl --m3fix --plant=3.53,0.555 --procs=2 --out=$R/m3 --tag=M3_cand_r0.17_fix_plant > $R/logs/recount_r0.17_fix_plant.log 2>&1; echo "plant exit $?" >> $R/logs/exits.txt
echo "end $(date -u '+%F %T')" >> $R/logs/exits.txt
