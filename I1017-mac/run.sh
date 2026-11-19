#!/bin/bash
# I1017-mac: the runs of the protocol, in order; code 1506f53f of wip/p2-h8
cd /Users/nathan/Source/choptuik-large-d-1017/solver/proof/review_p2c
PY=/Users/nathan/venv-314/bin/python
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/raw995/I1017-mac
mkdir -p $R/logs
run() { local name=$1; shift; nice -n 10 $PY -u p2c_h8.py "$@" > $R/logs/$name.log 2>&1; echo "$name exit $?" | tee -a $R/logs/exits.txt; }
: > $R/logs/exits.txt
run centre --centre
run centre_mut_A --centre --mutate=A
run centre_mut_sign --centre --mutate=sign
run box_d0_0 --out=$R
run box_d0_0_point --point --out=$R
run box_d0_1e7 --d0=1e7 --out=$R
run box_d0_0_mut_hS --mutate=hS --out=$R
echo "end $(date -u '+%F %T')" >> $R/logs/exits.txt
