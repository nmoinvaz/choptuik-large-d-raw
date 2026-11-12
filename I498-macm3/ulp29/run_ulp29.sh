#!/bin/bash
# #498, the coordinator's test (message 023811Z): the R 0.01 circle around 3.1023 - 0.0068i on the kf 29 state, n0 20,
# once as it is (plain, shift 0) and once with dh[10,11] one ulp up (ulp), with I506's wrapper (copied here, identical).
# Each run has an empty cache of its own, so every determinant is computed, none is replayed.
cd ~/Source/choptuik-large-d
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
out=../choptuik-large-d-raw/I498-macm3/ulp29
for spec in "plain 0" "ulp 1"; do
    set -- $spec
    caffeinate -is nice -n 10 python3 $out/ulp_circle.py 10 11 $2 -- hp/data/seeds/local/up23_D61.0264.npz 3.1023,-0.0068,0.01 --M=48 --kf=29 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf29 --data=$out/$1/data > $out/$1/circle.log 2>&1
    echo "ulp29 $1 exit $? at $(date -u +%FT%TZ)" >> ../choptuik-large-d-raw/I498-macm3/exits.txt
done
