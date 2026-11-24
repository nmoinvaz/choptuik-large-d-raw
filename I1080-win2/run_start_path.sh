#!/bin/bash
# #1080 x2: the continuation x1 -> x2 at M = 3 (the control, against x2's certified M = 3 harmonics, and its --mutate=end)
# and at M = 5 (from macm3's x1fm, the extended-precision M = 5 solution at x1). From solver/inner_stokes of wip/i1080-x2.
R=/d/choptuik-raw-i1080/I1080-win2
P=/c/Users/nathan/source/venv-i962/Scripts/python.exe
cd /d/choptuik-i1080x2/solver/inner_stokes || exit 9
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
C="3.446218246366727 0.347606965217407 3.526473056695715 0.211497981391215"
REF=0.97650854519762,-0.00176331952258
X1FM=0.88914001749446293360181270928257870386002,-0.00370993271443150303565004655254413233895987,0.294447328870753944400582875709184198403469,0.0116549046677389267389605216368219609839516
echo "$(date -u '+%F %T') UTC start, HEAD $(git rev-parse --short=8 HEAD)" >> $R/steps_start_path.txt
$P -u start_path.py 3 $C --v0=0.8054175863852923,0.011780043848505832 --n=40 --h3=1e-4 --ref=$REF --tol=1e-6 --out=$R/path_m3.jsonl > $R/logs/path_m3.log 2>&1; a=$?
$P -u start_path.py 3 $C --v0=0.8054175863852923,0.011780043848505832 --n=40 --h3=1e-4 --ref=$REF --tol=1e-6 --mutate=end --out=$R/path_m3_mutate_end.jsonl > $R/logs/path_m3_mutate_end.log 2>&1; b=$?
$P -u start_path.py 5 $C --v0=$X1FM --n=20 --h3=1e-4 --out=$R/path_m5.jsonl > $R/logs/path_m5.log 2>&1; c=$?
$P -u start_path.py 5 $C --v0=$X1FM --n=40 --h3=1e-4 --out=$R/path_m5_n40.jsonl > $R/logs/path_m5_n40.log 2>&1; d=$?
echo "$(date -u '+%F %T') UTC exits: m3 check $a (0 wanted), m3 --mutate=end $b (1 wanted), m5 n20 $c, m5 n40 $d" >> $R/steps_start_path.txt
