#!/bin/bash
# #967 item 3, the control case's stage E (the fixed-D Newton from the chain's prediction where the bordered attempt converges) and its miss against the
# accepted state arc_062, with the same wrapper and flags as run_item3_967.sh; I967_STAGES=E, output i3_control_E*. $1 = threads (6, as #973 shares the machine).
. "$(dirname "$0")/common967.sh"
T=${1:-6}
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 I967_HP=$WT/hp PYTHONFAULTHANDLER=1 I967_STAGES=E I967_TAG=_E I967_CASE=control
SUM=$OUT/summary_item3.txt
echo "# item 3 control E start $(stamp) UTC, hp $(git -C $WT rev-parse --short HEAD), threads $T, load $(cut -d' ' -f1-3 /proc/loadavg)" >> $SUM
mkdir -p $OUT/i3_control_E; s=$(date +%s)
nice -n 10 python -u $OUT/step61_967.py $R $OUT/i3_control_E --state I842-dh610/chain/arc_061_D259.903243.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 \
  --eps 1e-14 --h_max 1.0 --steps 400 --threads $T --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 \
  --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 \
  --reseed_start pred --save_jet 1 --arclength 1 --a0 0.00097 --arc_dhold 1e-12 --turns_max 2 > $OUT/i3_control_E.log 2>&1
rc=$?
echo "control E: exit $rc, $(( $(date +%s) - s )) s, load at end $(cut -d' ' -f1-3 /proc/loadavg)" >> $SUM
exit $rc
