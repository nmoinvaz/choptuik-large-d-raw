#!/bin/bash
# D 30 circles at M 64, no cut and then kf 13.  Usage: run.sh WORKTREE VENV_BIN
wt=$1
out=$(cd "$(dirname "$0")" && pwd)
cd "$wt" || exit 2
PATH=$2:$PATH
start=$(date -u '+%Y-%m-%d %H:%M:%S')
caffeinate -is nice -n 10 python3 hp/modecount_circle.py hp/data/states/up6_D30.0688.npz 2.079747703853262,0,0.2 4.267,1.324,0.35 --M=64 --kf=none --fmax=1e-15 --n0=20 --tag=D30.0688_M64 --data="$out/nocut" > "$out/circles_nocut.log" 2>&1
echo "nocut exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> "$out/exits.txt"
start=$(date -u '+%Y-%m-%d %H:%M:%S')
caffeinate -is nice -n 10 python3 hp/modecount_circle.py hp/data/states/up6_D30.0688.npz 2.079747703853262,0,0.2 4.267,1.324,0.35 --M=64 --kf=13 --fmax=1e-15 --n0=20 --tag=D30.0688_M64_kf13 --data="$out/kf13" > "$out/circles_kf13.log" 2>&1
echo "kf13 exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> "$out/exits.txt"
echo "all done $(date -u '+%Y-%m-%d %H:%M:%S')" >> "$out/exits.txt"
