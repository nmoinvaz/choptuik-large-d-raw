#!/bin/bash
# #1034 step 6 again on dh610: the chain step at --series_split 0, 1, 2 from the leg08 state (est. 70-90 min each; cap 4.5 h each). The first driver ran the issue's command as written,
# with the OUT argument relative (`I1034-dh610/step_s<S>`), which anm_run.py resolves against the current directory (hp/), so raw_out.py refused it at once (exit 1, 0 s, step6_chain_s*.log
# of run1034.sh). Here OUT is the absolute path $RAW/I1034-dh610/step_s<S>; every other argument is the issue's.
. "$(dirname "$0")/common1034.sh"
X=$OUT/exits_1034.txt; S=$OUT/summary_1034.txt
log() { echo "1034 $* $(stamp) UTC" >> $X; }
cd $WT/hp || exit 1
[ "$(git rev-parse HEAD | cut -c1-8)" = 9980cd93 ] || { echo "WT is not at 9980cd93"; exit 1; }
. $VENV/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
log "step 6 rerun start, load $(cut -d' ' -f1-3 /proc/loadavg)"
for sp in 0 1 2; do
  name=step6b_chain_s$sp; { echo "# $(stamp) UTC cmd: python3 anm_run.py $RAW $OUT/step_s$sp ... --series_split $sp"; } > $OUT/$name.log
  s=$(date +%s)
  nice -n 10 timeout -s TERM 16200 python3 anm_run.py $RAW $OUT/step_s$sp --state I903-win2/ks_chain/leg08_D232.0000_ks250/anm_pin3_D237.5270.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred --steps 1 --series_split $sp >> $OUT/$name.log 2>&1
  rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit 0, got $rc, $(( $(date +%s) - s )) s (cap 16200 s) $([ $rc = 0 ] && echo OK || echo MISMATCH); series lines: $(grep -E 'series saved' $OUT/$name.log | tail -2 | tr '\n' ';')" >> $S
  log "$name exit $rc (expected 0)"
done
log "step 6 rerun done"
