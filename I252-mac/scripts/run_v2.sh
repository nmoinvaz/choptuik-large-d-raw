#!/bin/bash
# #252, option (c) (../README.md "Restated gate"): one D per slot. Replays the lambda_phys circle from its cache, gates it
# with gate_phys_v2.py, then runs the circles at the M 48 and M 40 positions. Run: caffeinate -i nice -n 10 bash run_v2.sh D61|D55
PY=/Users/nathan/venv-314/bin/python
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-af41abeb756ed7275/hp
F=/Users/nathan/Source/choptuik-large-d-raw/I252-mac
ex() { echo "$1 exit $2 at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $F/exits.txt; }
C="--kf=23 --n0=20 --fmax=1e-15"
if [ "$1" = D61 ]; then
    L=2.043532530673195; S=$F/states/modecount_state_D61.0264_M64_kf23.npz; T=D61.0264_M64_kf23
    M48="1.306478,1.415783,0.2 2.007279,0.972720,0.2 2.558385,0.582474,0.2 3.019571,0,0.2"
    M40="2.7626,0.6308,0.2 2.9141,1.5885,0.2 1.98,1.20,0.3 1.83,0.49,0.3 0.032,3.086,0.2"
else
    L=2.04768412771239; S=$F/states/modecount_state_D55.0351_M64_kf23.npz; T=D55.0351_M64_kf23
    M48="0.19957,0.25475,0.2 0.31895,3.33140,0.2 0.06118,3.85263,0.3 -0.226688,4.280040,0.2"
    M40="0.477308,1.453280,0.2 0.24271,0.92524,0.2 0.09923,4.48036,0.2 0.34863,2.61221,0.2 0.36031,2.16089,0.2 0.59532,5.03932,0.2"
fi
D=$F/$1
$PY $HP/modecount_circle.py $S $L,0,0.2 $C --tag=$T --data=$D/circles > $D/v2_phys_replay.log 2>&1
ex v2_${1}_phys_replay $?
$PY $F/scripts/gate_phys_v2.py $D/circles/modecount_circles.jsonl $L > $D/gate_phys_v2.log 2>&1
rc=$?; ex v2_gate_${1}_phys $rc
[ $rc -eq 0 ] || exit 1
$PY $HP/modecount_circle.py $S $M48 $C --tag=$T --data=$D/circles > $D/v2_circles_M48.log 2>&1
ex v2_circles_${1}_M48 $?
$PY $HP/modecount_circle.py $S $M40 $C --tag=$T --data=$D/circles > $D/v2_circles_M40.log 2>&1
ex v2_circles_${1}_M40 $?
