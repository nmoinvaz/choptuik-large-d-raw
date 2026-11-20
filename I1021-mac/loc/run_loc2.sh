#!/bin/bash
# #1021: box 16's and box 7's zeros counted and located at xi1 0.17 and again at 0.18 at argcount 6da7da7b (seeds
# copied from another file or radius keep 'fix', so continuation-valued neighbours seed), default starts (0.25, 0.2),
# each in a box that puts the zero near 0.4 of each range. Writes loc/z16_6da7da7b and loc/z7_6da7da7b.
set -u
C=/Users/nathan/Source/choptuik-large-d-1021b
H=6da7da7be3f2325208f2d4f9570a5e5a8790bd78
PY=/Users/nathan/venv-314/bin/python
R=$(cd "$(dirname "$0")/.." && pwd)
AC=$C/solver/inner_stokes/argcount.py
[ "$(git -C $C rev-parse HEAD)" = $H ] || { echo "HEAD is not 6da7da7b"; exit 1; }
[ -z "$(git -C $C status --short)" ] || { echo "worktree not clean"; exit 1; }
for z in z16 z7; do [ -e $R/loc/${z}_6da7da7b ] && { echo "$R/loc/${z}_6da7da7b exists"; exit 1; }; done
E=""
for m in "" seedfix nocap lowcap; do
  $PY $AC --selftest ${m:+--mutate=$m} >> $R/loc/selftest_6da7da7b.log 2>&1; E="$E$? "
done
echo "selftest 6da7da7b plain seedfix nocap lowcap exits: $E" >> $R/loc/exits.txt
[ "$E" = "0 1 1 1 " ] || { echo "selftest exits $E"; exit 1; }
B="--M=3 --r1=0.17 --r1b=0.18 --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=1"
for z in z16 z7; do
  [ $z = z16 ] && SEED=$R/loc/in/b16-20_points_M3_r0.17.jsonl || SEED=$R/m3/points_M3_r0.17.jsonl
  echo "${z}_6da7da7b start $(date -u '+%F %T')" >> $R/loc/exits.txt
  timeout 6h nice -n 10 $PY -u $AC $B --recount=$R/loc/leaf_$z.jsonl --seed=$SEED --out=$R/loc/${z}_6da7da7b \
    --tag=M3_loc_${z}_6da7da7b > $R/loc/loc_${z}_6da7da7b.log 2>&1
  echo "${z}_6da7da7b exit $? $(date -u '+%F %T')" >> $R/loc/exits.txt
done
