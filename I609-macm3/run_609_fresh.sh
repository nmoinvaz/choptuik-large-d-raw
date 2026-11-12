#!/bin/bash
# I609 control: the M 48 D 30 state in hp/data of the worktree dated before this run (12:52 UTC) was moved aside
# (states_aside/), so that D30_M48_phys is rerun with a state made by setup in this run.
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
out=/Users/nathan/Source/choptuik-large-d-raw/I609-macm3
cd /Users/nathan/Source/choptuik-large-d-b596/hp
caffeinate -is nice -n 10 python3 -u modecount_smooth.py data/states/up6_D30.0688.npz 48 none 2.0797477 0 > $out/D30_M48_phys_fresh.log 2>&1
echo "D30_M48_phys_fresh exit $? at $(date -u +%FT%TZ)" >> $out/exits.txt
