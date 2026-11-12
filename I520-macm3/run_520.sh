#!/bin/bash
# #520: ulp_circle.py (this folder's, shift allowed up to +-4) at kf 27, R 0.0075, n0 20, an empty cache per run
cd ~/Source/choptuik-large-d
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
out=../choptuik-large-d-raw/I520-macm3
date -u +%FT%TZ > $out/started.txt
for spec in "ulp_m1 10 11 -1" "ulp_p2 10 11 2" "e3_8 3 8 1" "e30_31 30 31 1"; do
    set -- $spec
    caffeinate -is nice -n 10 python3 $out/ulp_circle.py $2 $3 $4 -- hp/data/seeds/local/up23_D61.0264.npz 2.043532530673195,0,0.0075 --M=48 --kf=27 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf27 --data=$out/$1/data > $out/$1/circle.log 2>&1
    echo "$1 exit $? at $(date -u +%FT%TZ)" >> $out/exits.txt
done
