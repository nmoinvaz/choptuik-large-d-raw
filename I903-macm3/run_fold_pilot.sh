#!/bin/bash
# #903 (the coordinator): fold rule pilot on my chain's jets so far, before D 258.5, to check control 1 here.
cd /Users/nathan/Source/choptuik-large-d-903f/hp
t0=$(date +%s)
caffeinate -is nice -n 10 /Users/nathan/Source/venv-macm3-main/bin/python3 -u fold_est_903.py verdict /Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3/chain_k135 /Users/nathan/Source/choptuik-large-d-raw-903 --json=/Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3/fold_pilot.json > /Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3/fold_pilot.log 2>&1
echo "903m fold pilot exit $? wall $(($(date +%s)-t0)) s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> /Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3/exits_k135.txt
