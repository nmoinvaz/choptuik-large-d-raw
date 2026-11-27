#!/bin/bash
# root.sh TAG LO HI : d18_secant run (wip/ell1-kappa-mm f56f91d2, block 12 ddm) on B/in/{TAG}.jsonl and its state
{
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101
K=/Users/nathan/Source/choptuik-kmm/solver/matter
tag=$1; lo=$2; hi=$3
rec=$W/B/in/$tag.jsonl; st=$W/B/in/sol_${tag}_D16.0000.npy
pr=$(git hash-object --no-filters $rec | cut -c1-8); ps=$(git hash-object --no-filters $st | cut -c1-8)
TH=${TH:-1}; TOL=${TOL:-1e-7}; B12=${B12:-ddm}
export VECLIB_MAXIMUM_THREADS=$TH OMP_NUM_THREADS=$TH OPENBLAS_NUM_THREADS=$TH
cd $K
echo "$(date -u '+%Y-%m-%d %H:%M:%S') root $tag ($lo, $hi) state $ps record $pr, d18_secant $(git hash-object --no-filters d18_secant.py | cut -c1-8) at $(git rev-parse --short HEAD), tol $TOL, b12 $B12, $TH threads" >> $W/B/run_roots.log
nice -n 10 /Users/nathan/venv-1025dd/bin/python -u d18_secant.py run $rec $st 16 $lo $hi $W/B/root_$tag.jsonl --tol=$TOL --maxev=20 --b12=$B12 --pin=$ps,$pr > $W/B/root_$tag.log 2>&1
echo "$(date -u '+%Y-%m-%d %H:%M:%S') root $tag exit $?" >> $W/B/run_roots.log
exit
}
