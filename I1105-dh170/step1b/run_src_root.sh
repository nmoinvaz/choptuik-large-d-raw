#!/bin/bash
# #1105 step 1b, ADDED control (not in t5's order): root the SOURCE record (k_c 55 D 16, 94c8b048 / 5be40af4) on this scanner with the same command as the three re-solves,
# to tell a solve scatter from a scanner difference against P4's 2.2440428096. 1 thread, nice 10.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1105-dh170/step1b
WT2=/home/nathan/Source/choptuik-large-d-1102/solver/matter
SITE=/home/nathan/Source/ellrs-site-1102
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [src] $*" >> $OUT/steps_1b.txt; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
cd $OUT || exit 9
step "ADDED control starts (not ordered): d18_secant.py run in/l1kc55Fb1025.jsonl in/sol_l1kc55Fb1025_D16.0000.npy 16 2.238 2.250 --tol=1e-7 --maxev=20 --b12=rust --b12_threads=1 --pin=94c8b048,5be40af4"
t1=$(date +%s)
( cd $WT2 && PYTHONPATH=$SITE nice -n 10 /usr/bin/time -v $PY -u d18_secant.py run $OUT/in/l1kc55Fb1025.jsonl $OUT/in/sol_l1kc55Fb1025_D16.0000.npy 16 2.238 2.250 $OUT/root_src.jsonl --tol=1e-7 --maxev=20 --b12=rust --b12_threads=1 --pin=94c8b048,5be40af4 > $OUT/root_src.log 2>&1 ); r=$?
step "source root exit $r, $(( $(date +%s) - t1 )) s; $(tail -1 $OUT/root_src.jsonl 2>/dev/null | jq -c 'select(.kind=="root") | {status,bracket,width,signs,robust,lam_lin,lam_brent,n_eval}' 2>/dev/null)"
echo "src DONE $(stamp) UTC, root exit $r" > $OUT/DONE_src.txt
exit 0
}
