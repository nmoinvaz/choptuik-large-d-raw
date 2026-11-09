#!/bin/bash
# #252, stage 2 (criterion 4 of ../README.md): D 61 circles on the M 64 state at the M 48 zeros, gated by the
# lambda_phys circle. The counts are held (coordinator, 2026-11-09). Run: caffeinate -i nice -n 10 bash run_circles_D61.sh
PY=/Users/nathan/venv-314/bin/python
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-af41abeb756ed7275/hp
F=/Users/nathan/Source/choptuik-large-d-raw/I252-mac
ex() { echo "$1 exit $2 at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $F/exits.txt; }
C="--kf=23 --n0=20 --fmax=1e-15"
# a D whose determinant check did not pass (criterion 2) is skipped
passed() { $PY -c "import json,sys; sys.exit(0 if json.load(open('$F/checks/det_check_$1_M64.json'))['passed'] else 1)" 2>/dev/null; }

# D 61: lambda_phys, then the M 48 kf 23 zeros of #230 (the pair near the axis by one circle on the axis, as #230)
L61=2.043532530673195
S61=$F/states/modecount_state_D61.0264_M64_kf23.npz
if passed D61; then
$PY $HP/modecount_circle.py $S61 $L61,0,0.2 $C --tag=D61.0264_M64_kf23 --data=$F/D61/circles > $F/D61/circles_phys.log 2>&1
ex circles_D61_phys $?
$PY $F/scripts/gate_phys.py $F/D61/circles/modecount_circles.jsonl $L61 > $F/D61/gate_phys.log 2>&1
rc=$?; ex gate_D61_phys $rc
if [ $rc -eq 0 ]; then
    $PY $HP/modecount_circle.py $S61 1.306478,1.415783,0.2 2.007279,0.972720,0.2 2.558385,0.582474,0.2 3.019571,0,0.2 \
        $C --tag=D61.0264_M64_kf23 --data=$F/D61/circles > $F/D61/circles_M48.log 2>&1
    ex circles_D61_M48 $?
fi
fi

