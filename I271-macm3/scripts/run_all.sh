#!/bin/bash
# The remaining runs of #271, then #267's three, one at a time from the worktree root.
# Usage: run_all.sh WORKTREE PYTHON
wt=$1
py=$2
raw=$(cd "$(dirname "$0")/../.." && pwd)
a=$raw/I271-macm3
b=$raw/I267-macm3
planted=$b/states/up6_D30.0688_kc100.npz
cd "$wt" || exit 2

run() {
    # run FOLDER NAME ARGS...
    folder=$1
    name=$2
    shift 2
    start=$(date -u '+%Y-%m-%d %H:%M:%S')
    caffeinate -is nice -n 10 "$py" -u hp/gamma_dd.py "$@" --threads=1 --polish=4 --M48 > "$folder/logs/$name.log" 2>&1
    rc=$?
    echo "$name exit $rc ($start to $(date -u '+%H:%M:%S') UTC): $*" >> "$folder/logs/exits.txt"
}

run "$a" b_old_rule "$a/gamma_old_rule.jsonl" hp/data/states/up8_D50.0075.npz --mutate=old_rule
run "$a" c_D20_30_40 "$a/gamma_dd.jsonl" hp/data/states/up2_D20.0437.npz hp/data/states/up6_D30.0688.npz hp/data/states/up7_D40.0201.npz
run "$a" e_D58 "$a/gamma_dd.jsonl" hp/data/states/up12_D58.0060.npz
run "$b" b_planted "$b/gamma_planted.jsonl" "$planted"
run "$b" c_no_gate "$b/gamma_no_gate.jsonl" "$planted" --mutate=no_tail_gate
run "$b" d_override "$b/gamma_override.jsonl" "$planted" --series_override
echo "all done $(date -u '+%Y-%m-%d %H:%M:%S')" >> "$a/logs/exits.txt"
