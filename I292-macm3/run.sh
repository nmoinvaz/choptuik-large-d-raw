#!/bin/bash
# The two R 0.0125 and 0.003 lam_phys circles, (a) with the node then (b) without.  Usage: run.sh MAIN_CHECKOUT VENV_BIN
wt=$1
out=$(cd "$(dirname "$0")" && pwd)
cd "$wt" || exit 2
PATH=$2:$PATH
start=$(date -u '+%Y-%m-%d %H:%M:%S')
caffeinate -is nice -n 10 python3 hp/modecount_circle.py hp/data/states/up10_D55.0351.npz 2.04768412771239,0,0.0125 2.04768412771239,0,0.003 --M=64 --kf=23 --centre_tol=1e-150 --fmax=1e-15 --n0=20 --tag=D55.0351_M64_kf23_inner015 --data="$out/node/data" > "$out/node/circle.log" 2>&1
echo "node exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> "$out/exits.txt"
start=$(date -u '+%Y-%m-%d %H:%M:%S')
caffeinate -is nice -n 10 python3 hp/modecount_circle.py hp/data/states/up10_D55.0351.npz 2.04768412771239,0,0.0125 2.04768412771239,0,0.003 --M=64 --kf=23 --fmax=1e-15 --n0=20 --tag=D55.0351_M64_kf23 --data="$out/nonode/data" > "$out/nonode/circle.log" 2>&1
echo "nonode exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> "$out/exits.txt"
echo "all done $(date -u '+%Y-%m-%d %H:%M:%S')" >> "$out/exits.txt"
