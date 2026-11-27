#!/bin/bash
# #1105 step 1d: root a re-solved state again on a widened bracket after its first root run was refused (same-signed ends); same command and pins as run_resolve1d.sh's root.
# The refused run's root_$TAG.jsonl stays; this writes root_${TAG}w.jsonl.
# usage: run_root_wide1d.sh TAG D BRLO BRHI [STATE RECORD]    e.g. r165 16.5 2.138 2.172;  c165 16.5 2.138 2.172 in/sol_l1kc55Fb1025_D16.5000.npy in/l1kc55Fb1025.jsonl
{
TAG=${1:?tag}; D=${2:?D}; BLO=${3:?lo}; BHI=${4:?hi}
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1105-dh170/step1d
WT2=/home/nathan/Source/choptuik-large-d-1102/solver/matter
SITE=/home/nathan/Source/ellrs-site-1102
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
printf -v DT 'D%.4f' $D
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [${TAG}w] $*" >> $OUT/steps_1d.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $OUT || exit 9
ST=$OUT/${5:-sol_l1kc55${TAG}_$DT.npy}; REC=$OUT/${6:-l1kc55$TAG.jsonl}
[ "$(git -C $WT2/.. rev-parse --short=8 HEAD 2>/dev/null)" = d4b6b6ce ] && [ "$(blob $WT2/d18_secant.py)" = 9706e506 ] || { step "STOP: the #1102 worktree is not d4b6b6ce / d18_secant.py 9706e506"; exit 1; }
[ -f root_$TAG.jsonl ] && [ ! -e root_${TAG}w.jsonl ] || { step "STOP: no refused run to widen, or root_${TAG}w.jsonl exists"; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
step "the first run on ($(jq -r 'select(.kind=="root")|.bracket|tostring' root_$TAG.jsonl)) was refused (same-signed ends); root starts on ($BLO, $BHI): d18_secant.py run $TAG $D $BLO $BHI --tol=1e-7 --maxev=20 --b12=rust --b12_threads=1 --pin=$(blob $ST),$(blob $REC)"
t1=$(date +%s)
( cd $WT2 && PYTHONPATH=$SITE nice -n 10 /usr/bin/time -v $PY -u d18_secant.py run $REC $ST $D $BLO $BHI $OUT/root_${TAG}w.jsonl --tol=1e-7 --maxev=20 --b12=rust --b12_threads=1 --pin=$(blob $ST),$(blob $REC) > $OUT/root_${TAG}w.log 2>&1 ); r=$?
step "root exit $r, $(( $(date +%s) - t1 )) s; $(tail -1 $OUT/root_${TAG}w.jsonl 2>/dev/null | jq -c 'select(.kind=="root") | {status,bracket,width,signs,robust,lam_lin,lam_brent,n_eval}' 2>/dev/null)"
echo "${TAG}w DONE $(stamp) UTC, root exit $r" > $OUT/DONE_${TAG}w.txt
exit 0
}
