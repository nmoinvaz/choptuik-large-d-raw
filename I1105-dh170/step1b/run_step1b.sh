#!/bin/bash
# #1105 step 1b (t5's order, comment 7213197061): re-solve the k_c 55 D 16 state at one u0 with ell_refine.py (2 threads, nice 10, cap 3 h on the exact python pid),
# then root it with d18_secant.py run on the bracket 2.238-2.250 (--tol=1e-7, 1 thread, --b12=rust) unless |F| > 1e-8 (then it is reported, not rooted).
# usage: run_step1b.sh TAG U0   (TAG u030, u040 or u050). Stops at the first failure (STOP_<TAG>.txt); steps in ../steps_1b.txt.
{
TAG=${1:?tag}; U0=${2:?u0}
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1105-dh170/step1b
WT=/home/nathan/Source/choptuik-large-d-1025k79; WTM=$WT/solver/matter
WT2=/home/nathan/Source/choptuik-large-d-1102/solver/matter
SITE=/home/nathan/Source/ellrs-site-1102
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
NEW=l1kc55$TAG; SRC=l1kc55Fb1025
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps_1b.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "regrid worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(blob $WTM/ell_refine.py)" = 631e5801 ] || stop "ell_refine.py is not 631e5801"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
[ "$(blob $WTM/data/sol_${SRC}_D16.0000.npy)" = 94c8b048 ] && [ "$(blob $WTM/data/$SRC.jsonl)" = 5be40af4 ] || stop "the source state or record in data/ is not 94c8b048 / 5be40af4"
[ "$(blob in/sol_${SRC}_D16.0000.npy)" = 94c8b048 ] && [ "$(blob in/$SRC.jsonl)" = 5be40af4 ] || stop "in/ source is not the pinned blob"
for f in $WTM/data/$NEW.jsonl $WTM/data/sol_${NEW}_D16.0000.npy; do [ -e $f ] && stop "$f exists"; done
[ "$(git -C $WT2/.. rev-parse --short=8 HEAD 2>/dev/null)" = d4b6b6ce ] && [ "$(blob $WT2/d18_secant.py)" = 9706e506 ] || stop "the #1102 worktree is not d4b6b6ce / d18_secant.py 9706e506"
step "pins ok: regrid worktree 48c36355 (ell_refine.py 631e5801, dss_ell equal 505d8399), source state 94c8b048 record 5be40af4, scanner worktree d4b6b6ce (d18_secant.py 9706e506); u0 $U0"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
CMD="nice -n 10 timeout 10800 $PY -u ell_refine.py $SRC 55 $NEW 55 1 16 2.2426280416106374 --kappa 0.7 --u0 $U0 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 2 threads, nice 10, cap 10800 s): $CMD" > $OUT/resolve_$TAG.log
step "re-solve starts: $CMD"
t0=$(date +%s)
( cd $WTM && $CMD >> $OUT/resolve_$TAG.log 2>&1 ); rc=$?
step "re-solve exit $rc, wall $(( $(date +%s) - t0 )) s (0 wanted; 124 is the cap)"
[ $rc = 0 ] || stop "the re-solve exit $rc"
[ -s $WTM/data/$NEW.jsonl ] && [ -s $WTM/data/sol_${NEW}_D16.0000.npy ] || stop "the re-solve wrote no state or record"
cp $WTM/data/$NEW.jsonl $WTM/data/sol_${NEW}_D16.0000.npy $OUT/
REC=$OUT/$NEW.jsonl; ST=$OUT/sol_${NEW}_D16.0000.npy
step "record: $(tail -1 $REC | jq -c '{u0,F,F_start,steps,Delta,constraint,seconds}'); state $(blob $ST), record $(blob $REC)"
if [ "$(tail -1 $REC | jq '.F <= 1e-8')" != true ]; then
  step "|F| exceeds 1e-8: not rooted"; echo "NOT ROOTED $(stamp) UTC: |F| $(tail -1 $REC | jq .F)" > $OUT/DONE_$TAG.txt; exit 0
fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
( cd $WT2 && nice -n 10 $PY -I d18_secant.py selftest > $OUT/selftest_secant_$TAG.txt 2>&1 ); e0=$?
step "d18_secant.py selftest exit $e0 (0 wanted)"; [ $e0 = 0 ] || stop "d18_secant.py selftest failed"
step "root starts: d18_secant.py run $NEW 16 2.238 2.250 --tol=1e-7 --maxev=20 --b12=rust --b12_threads=1 --pin=$(blob $ST),$(blob $REC)"
t1=$(date +%s)
( cd $WT2 && PYTHONPATH=$SITE nice -n 10 /usr/bin/time -v $PY -u d18_secant.py run $REC $ST 16 2.238 2.250 $OUT/root_$TAG.jsonl --tol=1e-7 --maxev=20 --b12=rust --b12_threads=1 --pin=$(blob $ST),$(blob $REC) > $OUT/root_$TAG.log 2>&1 ); r=$?
step "root exit $r (0: tol reached; 4: maxev or non-robust interior; 2: refused; 3: not the record system), $(( $(date +%s) - t1 )) s; $(tail -1 $OUT/root_$TAG.jsonl 2>/dev/null | jq -c 'select(.kind=="root") | {status,bracket,width,signs,robust,lam_lin,lam_brent,n_eval}' 2>/dev/null)"
echo "$TAG DONE $(stamp) UTC, re-solve exit $rc, root exit $r" > $OUT/DONE_$TAG.txt
step "done"
exit 0
}
