#!/bin/bash
# lam_phys circles at R 0.05 and 0.0125 on the kf 27 and kf 25 states.  Usage: run.sh
out=$(cd "$(dirname "$0")" && pwd)
cd $HOME/Source/choptuik-large-d || exit 2
PATH=$HOME/Source/venv-macm3-314/bin:$PATH
for K in 27 25
do
    start=$(date -u '+%Y-%m-%d %H:%M:%S')
    caffeinate -is nice -n 10 python3 hp/modecount_circle.py hp/data/seeds/local/up23_D61.0264.npz 2.043532530673195,0,0.05 2.043532530673195,0,0.0125 --M=48 --kf=$K --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf$K --data="$out/kf$K/data" > "$out/kf$K/circles.log" 2>&1
    echo "kf$K exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> "$out/exits.txt"
done
echo "all done $(date -u '+%Y-%m-%d %H:%M:%S')" >> "$out/exits.txt"
