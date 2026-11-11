#!/bin/bash
# The series gate (hp/series_truncation.py) on every unique stored state of unique_states_f.txt, one process, one thread.
A=$(cd "$(dirname "$0")" && pwd)
cd $HOME/Source/choptuik-large-d || exit 2
PATH=$HOME/Source/venv-macm3-314/bin:$PATH
start=$(date -u '+%Y-%m-%d %H:%M:%S')
caffeinate -is nice -n 10 python3 -u hp/series_truncation.py $A/gate_all.jsonl $(cat $A/unique_states_f.txt | tr '\n' ' ') > $A/gate_all.log 2>&1
echo "gate_all exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> $A/exits.txt
