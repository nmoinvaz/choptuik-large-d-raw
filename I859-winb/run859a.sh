#!/bin/bash
# stage 1 of #859 (runner's launcher; the issue's four width commands, control first, one at a time)
W=/c/Users/nathan/Source/choptuik-i859
RAW=/c/Users/nathan/Source/choptuik-large-d-raw-754
O=$RAW/I859-winb
PY=/c/Users/nathan/Source/venv-t179/Scripts/python.exe
export OPENBLAS_NUM_THREADS=3
cd "$W/solver/matter" || exit 99
ts() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
step() { n=$1; shift; echo "$n start $(ts)" >> "$O/exits_859.txt"; "$@" > "$O/$n.log" 2>&1; rc=$?; echo "$n exit $rc $(ts)" >> "$O/exits_859.txt"; }
step width_control_dcol_D9 $PY sigdss_band.py width data/sigdss_m1up.npz@9.0       --D 9  --eps 1 --kc 15 --mutate dcol --json $O/width.jsonl
step width_march_D8        $PY sigdss_band.py width data/sigdss_m1up_part6.npz@8.0 --D 8  --eps 1 --kc 15 --json $O/width.jsonl
step width_march_D9        $PY sigdss_band.py width data/sigdss_m1up.npz@9.0       --D 9  --eps 1 --kc 15 --json $O/width.jsonl
step width_march_D10       $PY sigdss_band.py width data/sigdss_m1up.npz@10.0      --D 10 --eps 1 --kc 15 --json $O/width.jsonl
echo "stage1 all done $(ts)" >> "$O/exits_859.txt"
