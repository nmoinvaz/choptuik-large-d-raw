#!/bin/bash
# #967 item 3 on dh610: the step 61 predictor test, the control case (step 60's state to step 61's accepted D) first, then the main
# case (step 61's state to step 62's attempt 4). anm_run.py's chain flags are run842.sh's (I842-dh610), --threads T (9 as #842), the
# wrapper step61_967.py replaces arclength.run_chain. Uses this build (the worktree's hp and its .venv). $1 = threads, $2 = cases.
. "$(dirname "$0")/common967.sh"
T=${1:-9}; CASES=${2:-"control main"}
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 I967_HP=$WT/hp PYTHONFAULTHANDLER=1
SUM=$OUT/summary_item3.txt
echo "# item 3 start $(stamp) UTC, hp $(git -C $WT rev-parse --short HEAD), hpkernel $(python -c 'import hpkernel; print(hpkernel.__file__)'), threads $T" >> $SUM
for case in $CASES; do
  if [ $case = main ]; then S=I842-dh610/chain/arc_062_D259.903270.npz; else S=I842-dh610/chain/arc_061_D259.903243.npz; fi
  mkdir -p $OUT/i3_$case
  s=$(date +%s)
  I967_CASE=$case nice -n 10 python -u $OUT/step61_967.py $R $OUT/i3_$case --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 \
    --eps 1e-14 --h_max 1.0 --steps 400 --threads $T --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 \
    --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 \
    --reseed_start pred --save_jet 1 --arclength 1 --a0 0.00097 --arc_dhold 1e-12 --turns_max 2 > $OUT/i3_$case.log 2>&1
  rc=$?
  echo "$case: exit $rc, $(( $(date +%s) - s )) s, load at end $(cut -d' ' -f1-3 /proc/loadavg)" >> $SUM
  [ $rc = 0 ] || { echo "stopped: $case exit $rc" >> $SUM; exit $rc; }
done
echo "# item 3 done $(stamp) UTC" >> $SUM
