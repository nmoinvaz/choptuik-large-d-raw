#!/bin/bash
# Usage: run_445.sh NAME   (NAME = d61, d55a or d55b), from anywhere.  Needs the main checkout's modecount_cx build.
name=$1
A=$(cd "$(dirname "$0")" && pwd)
RAW=$(cd "$A/.." && pwd)
M=$HOME/Source/choptuik-large-d
PY=$HOME/Source/venv-macm3-314/bin/python3
C="--kf=23 --n0=20 --fmax=1e-15"
ex() { echo "$1 exit $2 at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $A/exits.txt; }
case $name in
    d61) L=2.043532530673195; S=$RAW/I252-mac/states/modecount_state_D61.0264_M64_kf23.npz; T=D61.0264_M64_kf23
         POS="1.98,1.20,0.3 1.83,0.49,0.3 0.032,3.086,0.2" ;;
    d55a) L=2.04768412771239; S=$RAW/I252-mac/states/modecount_state_D55.0351_M64_kf23.npz; T=D55.0351_M64_kf23
         POS="0.24271,0.92524,0.2 0.09923,4.48036,0.2 0.34863,2.61221,0.2" ;;
    d55b) L=2.04768412771239; S=$RAW/I252-mac/states/modecount_state_D55.0351_M64_kf23.npz; T=D55.0351_M64_kf23
         POS="0.36031,2.16089,0.2 0.59532,5.03932,0.2" ;;
esac
D=$A/$name
cd $M || exit 2
caffeinate -is nice -n 10 $PY hp/modecount_circle.py $S $L,0,0.2 $C --tag=$T --data=$D/data > $D/phys_replay.log 2>&1
ex ${name}_phys_replay $?
$PY $RAW/I252-mac/scripts/gate_phys_v2.py $D/data/modecount_circles.jsonl $L > $D/gate_phys_v2.log 2>&1
rc=$?; ex ${name}_gate $rc
[ $rc -eq 0 ] || exit 1
caffeinate -is nice -n 10 $PY hp/modecount_circle.py $S $POS $C --tag=$T --data=$D/data > $D/circles_M40.log 2>&1
ex ${name}_circles_M40 $?
