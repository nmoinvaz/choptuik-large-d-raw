#!/bin/bash
# #252: the D 55 circles, rebalanced (16:30 UTC). run_circles_D55.sh's shell was stopped during its lambda_phys circle so
# that the D 61 slot can take half of the M 40 circles when it frees up (run_circles_D55_part2.sh); the circle itself ran
# on (PID $1). This part waits for it, then gates on it, then runs the M 48 circles and the first three M 40 circles.
# Run: caffeinate -i nice -n 10 bash run_circles_D55_part1.sh PID
PY=/Users/nathan/venv-314/bin/python
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-af41abeb756ed7275/hp
F=/Users/nathan/Source/choptuik-large-d-raw/I252-mac
ex() { echo "$1 exit $2 at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $F/exits.txt; }
C="--kf=23 --n0=20 --fmax=1e-15"
L55=2.04768412771239
S55=$F/states/modecount_state_D55.0351_M64_kf23.npz
while kill -0 $1 2>/dev/null; do sleep 20; done
echo "circles_D55_phys ended at $(date -u +%Y-%m-%dT%H:%M:%SZ) (exit not observed: its shell was stopped)" >> $F/exits.txt
$PY $F/scripts/gate_phys.py $F/D55/circles/modecount_circles.jsonl $L55 > $F/D55/gate_phys.log 2>&1
rc=$?; ex gate_D55_phys $rc
[ $rc -eq 0 ] || exit 1
$PY $HP/modecount_circle.py $S55 0.19957,0.25475,0.2 0.31895,3.33140,0.2 0.06118,3.85263,0.3 -0.226688,4.280040,0.2 \
    $C --tag=D55.0351_M64_kf23 --data=$F/D55/circles > $F/D55/circles_M48.log 2>&1
ex circles_D55_M48 $?
$PY $HP/modecount_circle.py $S55 0.477308,1.453280,0.2 0.24271,0.92524,0.2 0.09923,4.48036,0.2 \
    $C --tag=D55.0351_M64_kf23 --data=$F/D55/circles > $F/D55/circles_M40a.log 2>&1
ex circles_D55_M40a $?
