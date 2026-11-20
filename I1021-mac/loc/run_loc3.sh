#!/bin/bash
# #1021: b11-15's +1 (box A 3.4123-3.6623 x w/w_inf 0.2065-0.3065, cells under the 10 sigma guard at the edge midpoint
# (3.52562685, 0.21279321)) counted and located at xi1 0.17 and again at 0.18, argcount 6da7da7b, default starts,
# in a box twice the leaf size that puts that midpoint at 0.4 of each range. Writes loc/b1115p_6da7da7b.
set -u
C=/Users/nathan/Source/choptuik-large-d-1021b
H=6da7da7be3f2325208f2d4f9570a5e5a8790bd78
PY=/Users/nathan/venv-314/bin/python
R=$(cd "$(dirname "$0")/.." && pwd)
AC=$C/solver/inner_stokes/argcount.py
[ "$(git -C $C rev-parse HEAD)" = $H ] || { echo "HEAD is not 6da7da7b"; exit 1; }
[ -z "$(git -C $C status --short)" ] || { echo "worktree not clean"; exit 1; }
O=$R/loc/b1115p_6da7da7b
[ -e $O ] && { echo "$O exists"; exit 1; }
B="--M=3 --r1=0.17 --r1b=0.18 --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=1"
echo "b1115p_6da7da7b start $(date -u '+%F %T')" >> $R/loc/exits.txt
timeout 6h nice -n 10 $PY -u $AC $B --recount=$R/loc/leaf_b1115p.jsonl --seed=$R/loc/in/b11-15_points_M3_r0.17.jsonl \
  --out=$O --tag=M3_loc_b1115p_6da7da7b > $R/loc/loc_b1115p_6da7da7b.log 2>&1
echo "b1115p_6da7da7b exit $? $(date -u '+%F %T')" >> $R/loc/exits.txt
