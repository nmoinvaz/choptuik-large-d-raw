#!/bin/bash
# run_dd.sh M: the coordinator's order for quest P1 (#1090), hc of 25 Nov (read at about 04:12 UTC): continuation in D of form S with the Moebius horizon variable in double-double at M (12 or 14), one process of
# 1 thread at nice 10, cap 20 h (timeout 72000 s, TERM), code worktree ~/Source/c1090 (origin/wip/large-d-inner), venv ~/Source/venv-i1058. usage: bash run_dd.sh 12   (as the systemd user unit i1090-m12)
M=$1; RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1090-dh610
cd /home/nathan/Source/c1090/solver/inner_large_d || exit 1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
echo "# $(date -u '+%F %T') UTC start M $M: code $(git -C /home/nathan/Source/c1090 rev-parse --short=8 HEAD), python $(/home/nathan/Source/venv-i1058/bin/python3 -V 2>&1)" >> $F/run_M$M.txt
exec nice -n 10 timeout 72000 /home/nathan/Source/venv-i1058/bin/python3 solve_dd_cont.py $F/in/Sdd_D100_M10.json --M=$M --Ds=100,110,125,150,175,200,225,245.6366177558899,263.6,300,350,400,500,600,800,1000 --out=$F/dd_M${M}_cont
