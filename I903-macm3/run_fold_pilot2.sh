#!/bin/bash
# #903 (the coordinator): fold rule pilot 2, main 3c1b9582 with the reference of #841 (--ref_Dstar --ref_err), before D 258.5.
cd /Users/nathan/Source/choptuik-large-d-903f/hp
t0=$(date +%s)
caffeinate -is nice -n 10 /Users/nathan/Source/venv-macm3-main/bin/python3 -u fold_est_903.py verdict /Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3/chain_k135 /Users/nathan/Source/choptuik-large-d-raw-903 --ref_Dstar=259.90361142 --ref_err=5.3e-4 --json=/Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3/fold_pilot2.json > /Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3/fold_pilot2.log 2>&1
echo "903m fold pilot 2 (3c1b9582, ref #841) exit $? wall $(($(date +%s)-t0)) s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> /Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3/exits_k135.txt
