#!/bin/bash
# #506: the R 0.0075 circle around lambda_phys at n0 20, with dh[10,11] one ulp up (ulp) or as it is (plain, shift 0).
# Each run has an empty cache, so every determinant is computed, none is replayed.
cd ~/Source/choptuik-large-d
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
out=../choptuik-large-d-raw/I506-macm3
for spec in "kf27_ulp 27 1" "kf27_plain 27 0" "kf22_plain 22 0" "kf22_ulp 22 1"; do
    set -- $spec
    caffeinate -is nice -n 10 python3 $out/ulp_circle.py 10 11 $3 -- hp/data/seeds/local/up23_D61.0264.npz 2.043532530673195,0,0.0075 --M=48 --kf=$2 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf$2 --data=$out/$1/data > $out/$1/circle.log 2>&1
    echo "$1 exit $? at $(date -u +%FT%TZ)" >> $out/exits.txt
done
