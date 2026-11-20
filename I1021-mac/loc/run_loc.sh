#!/bin/bash
# #1021: box 16's and box 7's zeros counted and located at xi1 0.17 and again at 0.18 (argcount 998fd290), each in
# a box that puts the zero near 0.4 of each range, then boxes 29-31 recounted with their two points without value
# computed again (--retry, starts 0.2 then 0.25). Usage: run_loc.sh JOB [STARTS] (JOB loc or fix2931; loc's
# STARTS default 0.2,0.25 writes loc/z16 and loc/z7, another order writes loc/z16_s<order>, e.g. z16_s0.25-0.2)
set -u
C=/Users/nathan/Source/choptuik-large-d-1021b
PY=/Users/nathan/venv-314/bin/python
R=$(cd "$(dirname "$0")/.." && pwd)
N=$1
AC=$C/solver/inner_stokes/argcount.py
[ "$(git -C $C rev-parse HEAD)" = 998fd290406b768c1e0e6e0b9a0dccf0844a9d1d ] || { echo "HEAD is not 998fd290"; exit 1; }
[ -z "$(git -C $C status --short)" ] || { echo "worktree not clean"; exit 1; }
ST=${2:-0.2,0.25}
SUF=""; [ "$ST" = 0.2,0.25 ] || SUF="_s$(echo $ST | tr , -)"
B="--M=3 --r1=0.17 --r1b=0.18 --m3fix --m3starts=$ST --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=1"
if [ "$N" = loc ]; then
  for z in z16 z7; do
    O=$R/loc/$z$SUF
    [ -e $O ] && { echo "$O exists"; exit 1; }
    [ $z = z16 ] && SEED=$R/loc/in/b16-20_points_M3_r0.17.jsonl || SEED=$R/m3/points_M3_r0.17.jsonl
    echo "$z$SUF start $(date -u '+%F %T') starts $ST" >> $R/loc/exits.txt
    timeout 6h nice -n 10 $PY -u $AC $B --recount=$R/loc/leaf_$z.jsonl --seed=$SEED --out=$O \
      --tag=M3_loc_${z}${SUF}_998fd290 > $R/loc/loc_$z$SUF.log 2>&1
    echo "$z$SUF exit $? $(date -u '+%F %T')" >> $R/loc/exits.txt
  done
elif [ "$N" = fix2931 ]; then
  F=$R/fix2931
  [ "$(wc -l < $F/points_M3_r0.17.jsonl)" -eq 807 ] || { echo "cache is not the 807-line copy"; exit 1; }
  [ -e $F/points_M3_r0.18.jsonl ] && { echo "$F holds a 0.18 cache"; exit 1; }
  for m in "" nocap lowcap; do
    $PY $AC --selftest ${m:+--mutate=$m} >> $F/selftest_998fd290.log 2>&1; echo -n "$? " >> $F/selftest_exits.txt
  done
  [ "$(cat $F/selftest_exits.txt)" = "0 1 1 " ] || { echo "selftest exits $(cat $F/selftest_exits.txt)"; exit 1; }
  echo "start $(date -u '+%F %T')" >> $F/exits.txt
  timeout 8h nice -n 10 $PY -u $AC $B --retry --recount=$F/in/leaves_M3_cand_r0.17_fix_b26-31_998fd290.jsonl \
    --seed=$F/in/b26-31_points_M3_r0.2.jsonl --out=$F --tag=M3_cand_r0.17_fix_b29-31_998fd290 > $F/recount.log 2>&1
  echo "exit $? $(date -u '+%F %T')" >> $F/exits.txt
fi
