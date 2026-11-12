#!/bin/bash
# #569's control of the 0.5 rad rule (the coordinator's message of 2026-11-12 07:23 UTC): modecount_pivots.py of main 80b5056 at a point
# of a circle that closed; the rule's quiet side passes when every control shows less than 0.01 rad of arg change under one
# double-double ulp, at both signs. Usage: run_ctl.sh NAME STATE RE IM M KF   (state relative to the worktree's hp/ or absolute)
cd ~/Source/choptuik-large-d-b80/hp
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
name=$1; state=$2; re=$3; im=$4; M=$5; kf=$6
date -u +%FT%TZ > $raw/I569-macm3/started_$name.txt
caffeinate -is nice -n 10 python3 modecount_pivots.py $state $re $im --M=$M --kf=$kf --fmax=1e-15 --json=$raw/I569-macm3/$name.json > $raw/I569-macm3/$name.log 2>&1
echo "$name exit $? at $(date -u +%FT%TZ)" >> $raw/I569-macm3/exits.txt
