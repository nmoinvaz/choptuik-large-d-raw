#!/bin/bash
# #1105 step 1e (t5's order, the hc after comment 7218708645): re-solve a stored state at u0 0.04 (ell_refine.py, 2 threads, nice 10, cap 2 h on the python pid), then root the re-solve
# with run_root1e.sh unless |F| > 1e-8.
# usage: run_resolve1e.sh TAG D LAM0 SRCTAG SRC_STATE_BLOB SRC_RECORD_BLOB BRLO BRHI
#   r165b 16.5 2.159124821824751 l1kc55r165 cb69ffc3 61a375ff 2.138 2.172      (a re-solve of r165's own state)
#   r155  15.5 2.338788248005964 l1kc55Fb1025 990ccde2 5be40af4 2.3282 2.3522  (the continuation state at D 15.5)
{
TAG=${1:?tag}; D=${2:?D}; LAM0=${3:?lam0}; SRC=${4:?src tag}; SSB=${5:?src state blob}; SRB=${6:?src record blob}; BLO=${7:?lo}; BHI=${8:?hi}
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1105-dh170/step1e
WT=/home/nathan/Source/choptuik-large-d-1025k79; WTM=$WT/solver/matter
WT2=/home/nathan/Source/choptuik-large-d-1102/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
NEW=l1kc55$TAG; printf -v DT 'D%.4f' $D
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps_1e.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "regrid worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(blob $WTM/ell_refine.py)" = 631e5801 ] || stop "ell_refine.py is not 631e5801"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
[ "$(blob $WTM/data/sol_${SRC}_$DT.npy)" = "$SSB" ] && [ "$(blob $WTM/data/$SRC.jsonl)" = "$SRB" ] || stop "the start state or record in data/ is not $SSB / $SRB"
[ "$(blob in/sol_${SRC}_$DT.npy)" = "$SSB" ] && [ "$(blob in/$SRC.jsonl)" = "$SRB" ] || stop "in/ start is not the pinned blob"
for f in $WTM/data/$NEW.jsonl $WTM/data/sol_${NEW}_$DT.npy; do [ -e $f ] && stop "$f exists"; done
[ "$(git -C $WT2/.. rev-parse --short=8 HEAD 2>/dev/null)" = d4b6b6ce ] && [ "$(blob $WT2/d18_secant.py)" = 9706e506 ] || stop "the #1102 worktree is not d4b6b6ce / d18_secant.py 9706e506"
step "pins ok: regrid worktree 48c36355 (ell_refine.py 631e5801, dss_ell equal 505d8399), start state $SSB ($SRC, D $D), record $SRB, scanner worktree d4b6b6ce (d18_secant.py 9706e506)"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
CMD="nice -n 10 timeout 7200 $PY -u ell_refine.py $SRC 55 $NEW 55 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 2 threads, nice 10, cap 7200 s): $CMD" > $OUT/resolve_$TAG.log
step "re-solve starts: $CMD"
t0=$(date +%s)
( cd $WTM && $CMD >> $OUT/resolve_$TAG.log 2>&1 ); rc=$?
step "re-solve exit $rc, wall $(( $(date +%s) - t0 )) s (0 wanted; 124 is the cap)"
[ $rc = 0 ] || stop "the re-solve exit $rc"
[ -s $WTM/data/$NEW.jsonl ] && [ -s $WTM/data/sol_${NEW}_$DT.npy ] || stop "the re-solve wrote no state or record"
cp $WTM/data/$NEW.jsonl $WTM/data/sol_${NEW}_$DT.npy $OUT/
step "record: $(tail -1 $OUT/$NEW.jsonl | jq -c '{D,u0,F,F_start,steps,Delta,Delta_src,constraint,seconds}'); state $(blob $OUT/sol_${NEW}_$DT.npy), record $(blob $OUT/$NEW.jsonl)"
if [ "$(tail -1 $OUT/$NEW.jsonl | jq '.F <= 1e-8')" != true ]; then
  step "|F| exceeds 1e-8: not rooted"; echo "NOT ROOTED $(stamp) UTC: |F| $(tail -1 $OUT/$NEW.jsonl | jq .F)" > $OUT/DONE_$TAG.txt; exit 0
fi
( cd $WT2 && nice -n 10 $PY -I d18_secant.py selftest > $OUT/selftest_secant_$TAG.txt 2>&1 ); e0=$?
step "d18_secant.py selftest exit $e0 (0 wanted)"; [ $e0 = 0 ] || stop "d18_secant.py selftest failed"
exec $OUT/run_root1e.sh $TAG $D sol_${NEW}_$DT.npy $NEW.jsonl $BLO $BHI
}
