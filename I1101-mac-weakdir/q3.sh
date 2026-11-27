#!/bin/bash
{
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101
I=$W/in
while pgrep -f "w1101/q2b.sh" > /dev/null; do sleep 20; done
cd /Users/nathan/Source/choptuik-1101w/solver/matter
export VECLIB_MAXIMUM_THREADS=2
P="nice -n 10 /Users/nathan/venv-1025dd/bin/python -u i1101_weakdir.py"
echo "$(date -u '+%Y-%m-%d %H:%M:%S') segerr starts" >> $W/B/run_seg.log
$P segerr $I/l1kc55u040.jsonl $I/sol_l1kc55u040_D16.0000.npy 16.0 --svd=$W/jac/svd_src.npz --out=$W/B/seg/segerr_u40.json > $W/B/seg/segerr_u40.log 2>&1
echo "$(date -u '+%Y-%m-%d %H:%M:%S') segerr exit $?" >> $W/B/run_seg.log
for g in "all kappa=0.35" "inner seg=0,1,2,3,4,5:0.35" "middle seg=6,7,8,9:0.35" "outer seg=10,11,12:0.35"; do
  set -- $g
  $P chord $W/jac/svd_src.npz $I/l1kc55u040.jsonl $I/sol_l1kc55u040_D16.0000.npy 16.0 $2 $W/B/seg/sol_$1_D16.0000.npy > $W/B/seg/chord_$1.log 2>&1
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') chord $1 exit $?" >> $W/B/run_seg.log
  $P root $W/B/seg/sol_$1_D16.0000.npy 2.238 2.252 $W/B/seg/root_$1.jsonl --tol=1e-5 --maxev=16 --b12=fast > $W/B/seg/root_$1.log 2>&1
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') root $1 exit $?" >> $W/B/run_seg.log
done
echo "$(date -u '+%Y-%m-%d %H:%M:%S') q3 done" >> $W/B/run_seg.log
exit
}
