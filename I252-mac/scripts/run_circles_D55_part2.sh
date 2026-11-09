#!/bin/bash
# #252: the other three D 55 M 40 circles, in the D 61 slot once its circles end (PID $1, run_circles_D61.sh), and only
# if the D 55 lambda_phys gate passed. Its own tag (cache), so that the two slots never write one cache file.
# Run: caffeinate -i nice -n 10 bash run_circles_D55_part2.sh PID
PY=/Users/nathan/venv-314/bin/python
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-af41abeb756ed7275/hp
F=/Users/nathan/Source/choptuik-large-d-raw/I252-mac
ex() { echo "$1 exit $2 at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $F/exits.txt; }
C="--kf=23 --n0=20 --fmax=1e-15"
S55=$F/states/modecount_state_D55.0351_M64_kf23.npz
while kill -0 $1 2>/dev/null; do sleep 20; done
until grep -q '^gate_D55_phys' $F/exits.txt; do sleep 20; done
grep -q '^gate_D55_phys exit 0' $F/exits.txt || { ex skip_D55_M40b_gate_failed 1; exit 1; }
$PY $HP/modecount_circle.py $S55 0.34863,2.61221,0.2 0.36031,2.16089,0.2 0.59532,5.03932,0.2 \
    $C --tag=D55.0351_M64_kf23_b --data=$F/D55/circles > $F/D55/circles_M40b.log 2>&1
ex circles_D55_M40b $?
