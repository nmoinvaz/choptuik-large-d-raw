#!/bin/bash
# #1105 step 1e: root one state with d18_secant.py run (Rust block, --tol=1e-7 --maxev=20, 1 thread, nice 10) on the given bracket. If the run is refused for same-signed ends
# the bracket is widened once by 0.01 on the side the signs give (both +: the root is below the low end, so the low end falls by 0.01; both -: the high end rises by 0.01),
# as t5 accepted at D 16.5 (step 1d), and the run repeats into root_${TAG}w.jsonl; a second refusal stops.
# usage: run_root1e.sh TAG D STATE RECORD BRLO BRHI        STATE and RECORD are paths relative to step1e/ (in/... for the continuation state, ./... for a re-solve)
{
TAG=${1:?tag}; D=${2:?D}; STF=${3:?state}; RCF=${4:?record}; BLO=${5:?lo}; BHI=${6:?hi}
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1105-dh170/step1e
WT2=/home/nathan/Source/choptuik-large-d-1102/solver/matter
SITE=/home/nathan/Source/ellrs-site-1102
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps_1e.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
ST=$OUT/$STF; RC=$OUT/$RCF
[ -s $ST ] && [ -s $RC ] || stop "$STF or $RCF is missing"
[ "$(git -C $WT2/.. rev-parse --short=8 HEAD 2>/dev/null)" = d4b6b6ce ] && [ "$(blob $WT2/d18_secant.py)" = 9706e506 ] || stop "the #1102 worktree is not d4b6b6ce / d18_secant.py 9706e506"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
root() {   # root OUTFILE LO HI
  step "root starts: d18_secant.py run $RCF $STF $D $2 $3 $(basename $1) --tol=1e-7 --maxev=20 --b12=rust --b12_threads=1 --pin=$(blob $ST),$(blob $RC)"
  t1=$(date +%s)
  ( cd $WT2 && PYTHONPATH=$SITE nice -n 10 /usr/bin/time -v $PY -u d18_secant.py run $RC $ST $D $2 $3 $1 --tol=1e-7 --maxev=20 --b12=rust --b12_threads=1 --pin=$(blob $ST),$(blob $RC) > ${1%.jsonl}.log 2>&1 )
  r=$?
  step "root exit $r (0: tol reached; 4: maxev or non-robust interior; 2: refused; 3: not the record system), $(( $(date +%s) - t1 )) s; $(tail -1 $1 2>/dev/null | jq -c 'select(.kind=="root") | {status,bracket,width,signs,robust,lam_lin,lam_brent,n_eval}' 2>/dev/null)"
}
root $OUT/root_$TAG.jsonl $BLO $BHI
fin=$r
if [ $r = 2 ] && [ "$(tail -1 root_$TAG.jsonl | jq -c '.signs[0] == .signs[1]')" = true ]; then
  s=$(tail -1 root_$TAG.jsonl | jq '.signs[0]')
  if [ "$s" = 1 ] || [ "$s" = 1.0 ]; then NLO=$(python3 -I -c "print(repr(round($BLO - 0.01, 6)))"); NHI=$BHI; else NLO=$BLO; NHI=$(python3 -I -c "print(repr(round($BHI + 0.01, 6)))"); fi
  step "refused with both ends sign $s: widened by 0.01 to ($NLO, $NHI)"
  root $OUT/root_${TAG}w.jsonl $NLO $NHI
  fin=$r
fi
echo "$TAG DONE $(stamp) UTC, root exit $fin" > $OUT/DONE_$TAG.txt
step "done"
exit 0
}
