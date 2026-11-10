#!/bin/bash
# Second round: #267's three planted runs with --fmax=1e-19 (the first attempt was skipped at M 32, |F| 1.2e-20), then #271's (d).
# Usage: run_second.sh WORKTREE PYTHON
wt=$1
py=$2
raw=$(cd "$(dirname "$0")/../.." && pwd)
a=$raw/I271-macm3
b=$raw/I267-macm3
planted=$b/states/up6_D30.0688_kc100.npz
cd "$wt" || exit 2

run() {
    # run FOLDER NAME SCRIPT ARGS...
    folder=$1
    name=$2
    script=$3
    shift 3
    start=$(date -u '+%Y-%m-%d %H:%M:%S')
    caffeinate -is nice -n 10 "$py" -u "$script" "$@" > "$folder/logs/$name.log" 2>&1
    rc=$?
    echo "$name exit $rc ($start to $(date -u '+%H:%M:%S') UTC): $script $*" >> "$folder/logs/exits.txt"
}

run "$b" b_planted_fmax hp/gamma_dd.py "$b/gamma_planted_fmax.jsonl" "$planted" --threads=1 --polish=4 --M48 --fmax=1e-19
run "$b" c_no_gate_fmax hp/gamma_dd.py "$b/gamma_no_gate_fmax.jsonl" "$planted" --threads=1 --polish=4 --M48 --fmax=1e-19 --mutate=no_tail_gate
run "$b" d_override_fmax hp/gamma_dd.py "$b/gamma_override_fmax.jsonl" "$planted" --threads=1 --polish=4 --M48 --fmax=1e-19 --series_override
run "$a" d_series_D50 hp/series_truncation.py "$a/series_D50.jsonl" hp/data/states/up8_D50.0075.npz --polish=4 --Mhi=48
echo "second round done $(date -u '+%Y-%m-%d %H:%M:%S')" >> "$a/logs/exits.txt"
