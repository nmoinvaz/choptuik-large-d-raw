#!/bin/bash
# #579: modecount_pivots.py (main 80b5056) at one of the eight points listed on the issue. Usage: run_579.sh NAME STATE RE IM M KF
cd ~/Source/choptuik-large-d-b80/hp
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
name=$1; state=$2; re=$3; im=$4; M=$5; kf=$6
date -u +%FT%TZ > $raw/I579-macm3/started_$name.txt
caffeinate -is nice -n 10 python3 modecount_pivots.py $state $re $im --M=$M --kf=$kf --fmax=1e-15 --json=$raw/I579-macm3/$name.json > $raw/I579-macm3/$name.log 2>&1
echo "$name exit $? at $(date -u +%FT%TZ)" >> $raw/I579-macm3/exits.txt
