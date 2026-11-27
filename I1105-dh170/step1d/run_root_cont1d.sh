#!/bin/bash
# #1105 step 1d: root a continuation state of record 5be40af4 (D 15 or D 16.5) with d18_secant.py run (Rust block, --tol=1e-7 --maxev=20, 1 thread, nice 10) on the given bracket.
# Waits for WAITFILE's DONE/STOP (R2's scan, #1101, keeps priority) before it starts.
# usage: run_root_cont1d.sh TAG D STATE_BLOB BRLO BRHI WAITDIR    e.g. c150 15 ad055605 2.410 2.435 /home/nathan/Source/choptuik-large-d-raw-p4/I1101-dh170
{
TAG=${1:?tag}; D=${2:?D}; SSB=${3:?state blob}; BLO=${4:?lo}; BHI=${5:?hi}; WD=${6:?wait dir}
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1105-dh170/step1d
WT2=/home/nathan/Source/choptuik-large-d-1102/solver/matter
SITE=/home/nathan/Source/ellrs-site-1102
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
printf -v DT 'D%.4f' $D
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps_1d.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
[ "$(blob in/sol_l1kc55Fb1025_$DT.npy)" = "$SSB" ] && [ "$(blob in/l1kc55Fb1025.jsonl)" = 5be40af4 ] || stop "in/ state or record is not the pinned blob"
[ "$(git -C $WT2/.. rev-parse --short=8 HEAD 2>/dev/null)" = d4b6b6ce ] && [ "$(blob $WT2/d18_secant.py)" = 9706e506 ] || stop "the #1102 worktree is not d4b6b6ce / d18_secant.py 9706e506"
step "pins ok: continuation state $SSB (D $D), record 5be40af4; waiting for R2's scan (DONE_r2.txt or STOP_r2.txt in $WD)"
until [ -f $WD/DONE_r2.txt ] || [ -f $WD/STOP_r2.txt ]; do sleep 20; done
step "R2's scan ended ($(cat $WD/DONE_r2.txt $WD/STOP_r2.txt 2>/dev/null | head -1)); root starts"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
t1=$(date +%s)
( cd $WT2 && PYTHONPATH=$SITE nice -n 10 /usr/bin/time -v $PY -u d18_secant.py run $OUT/in/l1kc55Fb1025.jsonl $OUT/in/sol_l1kc55Fb1025_$DT.npy $D $BLO $BHI $OUT/root_$TAG.jsonl --tol=1e-7 --maxev=20 --b12=rust --b12_threads=1 --pin=$SSB,5be40af4 > $OUT/root_$TAG.log 2>&1 ); r=$?
step "root exit $r (0: tol reached; 4: maxev or non-robust interior; 2: refused; 3: not the record system), $(( $(date +%s) - t1 )) s; $(tail -1 $OUT/root_$TAG.jsonl 2>/dev/null | jq -c 'select(.kind=="root") | {status,bracket,width,signs,robust,lam_lin,lam_brent,n_eval}' 2>/dev/null)"
echo "$TAG DONE $(stamp) UTC, root exit $r" > $OUT/DONE_$TAG.txt
exit 0
}
