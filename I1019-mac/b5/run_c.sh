#!/bin/bash
# I1019-mac b5: stage C runs; code 5f58c30b of wip/p2-b5
cd /Users/nathan/Source/choptuik-large-d-1019/solver/proof/review_p2c
PY=/Users/nathan/venv-314/bin/python
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/raw995/I1019-mac/b5
run() { local name=$1; shift; nice -n 10 $PY -u p2c_b5.py "$@" > $R/logs/$name.log 2>&1; echo "$name exit $?" >> $R/logs/exits_c.txt; }
: > $R/logs/exits_c.txt
run sector_centre --sector --nr=32 --na=64 --out=$R
run sector_box --sector --box --nr=32 --na=64 --out=$R
run sector_mut_jacC --sector --nr=16 --na=32 --mutate=jacC --out=$R
run sector_mut_jacC2 --sector --nr=16 --na=32 --mutate=jacC2 --out=$R
run sector_mut_jacP2 --sector --nr=16 --na=32 --mutate=jacP2 --out=$R
echo "end $(date -u '+%F %T')" >> $R/logs/exits_c.txt
