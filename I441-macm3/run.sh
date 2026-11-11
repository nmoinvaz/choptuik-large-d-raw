#!/bin/bash
# Usage: run.sh   (from anywhere); the two test-field counts, plain then planted
A=$(cd "$(dirname "$0")" && pwd)
cd $HOME/Source/choptuik-large-d || exit 2
PATH=$HOME/Source/venv-macm3-314/bin:$PATH
S=hp/data/lowD_states/lowD_D4.0000_M48.npz
start=$(date -u '+%Y-%m-%d %H:%M:%S')
caffeinate -is nice -n 10 python3 hp/modecount_test.py $S --kf=none --data=$A/data > $A/count_plain.log 2>&1
echo "plain exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> $A/exits.txt
start=$(date -u '+%Y-%m-%d %H:%M:%S')
caffeinate -is nice -n 10 python3 hp/modecount_test.py $S --kf=none --plant=3.1+1j --data=$A/data > $A/count_planted.log 2>&1
echo "planted exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> $A/exits.txt
echo "all done $(date -u '+%Y-%m-%d %H:%M:%S')" >> $A/exits.txt
