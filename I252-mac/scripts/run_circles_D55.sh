#!/bin/bash
# #252, stage 2 (criterion 4 of ../README.md): D 55 circles on the M 64 state at the M 48 and M 40 zeros, gated
# by the lambda_phys circle. The counts are held (coordinator, 2026-11-09). Run: caffeinate -i nice -n 10 bash run_circles_D55.sh
PY=/Users/nathan/venv-314/bin/python
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-af41abeb756ed7275/hp
F=/Users/nathan/Source/choptuik-large-d-raw/I252-mac
ex() { echo "$1 exit $2 at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $F/exits.txt; }
C="--kf=23 --n0=20 --fmax=1e-15"
# a D whose determinant check did not pass (criterion 2) is skipped
passed() { $PY -c "import json,sys; sys.exit(0 if json.load(open('$F/checks/det_check_$1_M64.json'))['passed'] else 1)" 2>/dev/null; }

# D 55: lambda_phys, then the M 48 zeros of #238 and the M 40 zeros of #231
L55=2.04768412771239
S55=$F/states/modecount_state_D55.0351_M64_kf23.npz
passed D55 || { ex skip_D55_det_check_not_passed 1; exit 1; }
$PY $HP/modecount_circle.py $S55 $L55,0,0.2 $C --tag=D55.0351_M64_kf23 --data=$F/D55/circles > $F/D55/circles_phys.log 2>&1
ex circles_D55_phys $?
$PY $F/scripts/gate_phys.py $F/D55/circles/modecount_circles.jsonl $L55 > $F/D55/gate_phys.log 2>&1
rc=$?; ex gate_D55_phys $rc
if [ $rc -eq 0 ]; then
    $PY $HP/modecount_circle.py $S55 0.19957,0.25475,0.2 0.31895,3.33140,0.2 0.06118,3.85263,0.3 -0.226688,4.280040,0.2 \
        $C --tag=D55.0351_M64_kf23 --data=$F/D55/circles > $F/D55/circles_M48.log 2>&1
    ex circles_D55_M48 $?
    $PY $HP/modecount_circle.py $S55 0.477308,1.453280,0.2 0.24271,0.92524,0.2 0.09923,4.48036,0.2 0.34863,2.61221,0.2 \
        0.36031,2.16089,0.2 0.59532,5.03932,0.2 $C --tag=D55.0351_M64_kf23 --data=$F/D55/circles > $F/D55/circles_M40.log 2>&1
    ex circles_D55_M40 $?
fi

