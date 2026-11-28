#!/bin/bash
# #1102 step 1: the fast solver Jacobian against DSSEll.jacobian at R0 (k_c 127, D 23.0). Run as a systemd user unit.
RAW=/home/nathan/Source/choptuik-large-d-raw-1102/I1102-dh610
IN=/home/nathan/scratch1102/in
cd /home/nathan/Source/choptuik-ell1fast/solver/matter || exit 9
export OPENBLAS_NUM_THREADS=4
echo "jac127 start $(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> $RAW/exits_1102.txt
timeout 7200 /home/nathan/Source/venv-i1058/bin/python ell_fastm.py jaccheck $IN/l1kc127k070w2.jsonl \
  $IN/sol_l1kc127k070w2_D23.0000.npy 23.0 --out=$RAW/jac127.json > $RAW/jac127.log 2>&1
echo "jac127 exit $? $(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> $RAW/exits_1102.txt
