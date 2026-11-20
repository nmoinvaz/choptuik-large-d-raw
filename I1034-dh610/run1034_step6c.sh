# #1034 step 6, third attempt on dh610: the chain step at --series_split 0, 1, 2 from the leg08 state (est. 70-90 min each; cap 4.5 h each). Run 1 (run1034.sh) ran the issue's command as written and
# was refused at once (relative OUT). Run 2 (run1034_step6.sh, OUT absolute) ran in 68 s with no chain step: the leg08 state is at D 237.527 and anm_run.py's --D_max defaults to 200
# (`if D >= opt["D_max"]: break`), so its loop does nothing. Here --D_max 300 is added (any value above D + h_max 1.0 does the same) and OUT is $OUT/step_s<S>_dmax300; every other argument is the issue's.
. "$(dirname "$0")/common1034.sh"
X=$OUT/exits_1034.txt; S=$OUT/summary_1034.txt
log() { echo "1034 $* $(stamp) UTC" >> $X; }
cd $WT/hp || exit 1
[ "$(git rev-parse HEAD | cut -c1-8)" = 9980cd93 ] || { echo "WT is not at 9980cd93"; exit 1; }
. $VENV/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
log "step 6 rerun start, load $(cut -d' ' -f1-3 /proc/loadavg)"
for sp in 0 1 2; do
  name=step6c_chain_s$sp; { echo "# $(stamp) UTC cmd: python3 anm_run.py $RAW $OUT/step_s${sp}_dmax300 ... --series_split $sp"; } > $OUT/$name.log
  s=$(date +%s)
  nice -n 10 timeout -s TERM 16200 python3 anm_run.py $RAW $OUT/step_s${sp}_dmax300 --state I903-win2/ks_chain/leg08_D232.0000_ks250/anm_pin3_D237.5270.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred --steps 1 --D_max 300 --series_split $sp >> $OUT/$name.log 2>&1
  rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit 0, got $rc, $(( $(date +%s) - s )) s (cap 16200 s) $([ $rc = 0 ] && echo OK || echo MISMATCH); series lines: $(grep -E 'series saved' $OUT/$name.log | tail -2 | tr '\n' ';')" >> $S
  log "$name exit $rc (expected 0)"
done
log "step 6 rerun done"
