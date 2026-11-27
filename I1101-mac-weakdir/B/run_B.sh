#!/bin/bash
{
M=/Users/nathan/Source/choptuik-1101w/solver/matter
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101/B
export VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
cd $M
for K in 035:0.35 050:0.5 025:0.25 070:0.7; do
  tag=l1kc55k${K%%:*}m; kap=${K##*:}
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') start $tag kappa $kap" >> $W/run_B.log
  timeout 14400 nice -n 10 /Users/nathan/venv-1025dd/bin/python -u ell_refine.py l1kc55u040 55 $tag 55 1 16 2.2426280416106374 --kappa $kap --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma > $W/resolve_$tag.log 2>&1
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') end $tag exit $?" >> $W/run_B.log
  touch $W/done_$tag
done
exit
}
