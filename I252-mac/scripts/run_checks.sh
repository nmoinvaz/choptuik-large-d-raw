#!/bin/bash
# #252, stage 1 (criteria 1 and 2 of ../README.md): the D 61 determinant check and its control, the D 55 M 64 setup and
# its determinant check. Run: caffeinate -i nice -n 10 bash run_checks.sh
PY=/Users/nathan/venv-314/bin/python
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-af41abeb756ed7275/hp
F=/Users/nathan/Source/choptuik-large-d-raw/I252-mac
ex() { echo "$1 exit $2 at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $F/exits.txt; }
echo "start checks $(date -u +%Y-%m-%dT%H:%M:%SZ) main $(git -C $HP rev-parse HEAD)" >> $F/exits.txt

$PY $F/scripts/det_check.py $HP $F/states/modecount_state_D61.0264_M64_kf23.npz 23 2.043532530673195 \
    $F/checks/det_check_D61_M64.json > $F/checks/det_check_D61_M64.log 2>&1
ex det_check_D61_M64 $?
# control: must fail
$PY $F/scripts/det_check.py $HP $F/states/modecount_state_D61.0264_M64_kf23_outer085.npz 23 2.043532530673195 \
    $F/checks/det_check_D61_M64_outer085_control.json > $F/checks/det_check_D61_M64_outer085_control.log 2>&1
ex det_check_D61_M64_outer085_control_must_fail $?

# D 55: setup at M 64 from the M 48 kf 23 state (saves hp/data/modecount_state_D55.0351_M64_kf23.npz)
$PY $HP/modecount_probe.py $F/states/modecount_state_D55.0351_M48_kf23_from_I232.npz --M=64 --kf=23 --setup \
    --fmax=1e-15 --json=$F/checks/probe_D55_M64.json --setup_json=$F/checks/setup_D55_M64.json > $F/checks/setup_D55_M64.log 2>&1
rc=$?
ex setup_D55_M64 $rc
if [ $rc -eq 0 ]; then
    cp $HP/data/modecount_state_D55.0351_M64_kf23.npz $F/states/
    $PY $F/scripts/det_check.py $HP $F/states/modecount_state_D55.0351_M64_kf23.npz 23 2.04768412771239 \
        $F/checks/det_check_D55_M64.json > $F/checks/det_check_D55_M64.log 2>&1
    ex det_check_D55_M64 $?
fi
