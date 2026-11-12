#!/bin/bash
# #526: ulp_circle.py (this folder's: dh, ph, seg) at R 0.0075, n0 20, an empty cache per run.
# ph[10] and seg[1][1] (0.4389384307685937, the first interior boundary of the second segment) are one ulp up.
cd ~/Source/choptuik-large-d
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
out=../choptuik-large-d-raw/I526-macm3
date -u +%FT%TZ > $out/started.txt
for spec in "c_seg0 27 seg 1 1 0" "k27_ph 27 ph 10 1" "k27_seg 27 seg 1 1 1" "k22_ph 22 ph 10 1" "k22_seg 22 seg 1 1 1" "c_ph0 27 ph 10 0"; do
    set -- $spec
    run=$1; kf=$2; shift 2
    caffeinate -is nice -n 10 python3 $out/ulp_circle.py "$@" -- hp/data/seeds/local/up23_D61.0264.npz 2.043532530673195,0,0.0075 --M=48 --kf=$kf --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf$kf --data=$out/$run/data > $out/$run/circle.log 2>&1
    echo "$run exit $? at $(date -u +%FT%TZ)" >> $out/exits.txt
done
