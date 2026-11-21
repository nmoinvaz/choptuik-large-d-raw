#!/bin/bash
# #1043 job 5: the flag-on polish (default start bound) of job 4's two flag-off states, D 242.2102 and 242.4602, with notes/EXACT_RECIP.md 3.5's flags (job 2's F), and delta against job 4's states
# and against the flag-off re-polish. Worktree of main 796f4bac (the one that made the states), venv-i1054. A braced block ending in exit.
{
. "$(dirname "$0")/common1054.sh"
X=$OUT/exits_1054.txt; SUM=$OUT/summary_1054.txt
log() { echo "1054h $* $(stamp) UTC" >> $X; }
W=/home/nathan/Source/choptuik-large-d-1043g
[ -d $W/hp ] || { log "no $W: stop"; exit 1; }
M=$(git -C $W rev-parse HEAD); [ -z "$(git -C $W status --short)" ] || { log "worktree $W not clean: stop"; exit 1; }
git -C $W merge-base --is-ancestor 796f4bac $M || { log "$M is not at or after 796f4bac: stop"; exit 1; }
log "worktree $W at $M, venv-i1054, load $(cut -d' ' -f1-3 /proc/loadavg)"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
. $VENV/bin/activate
cd $W/hp || exit 1
for T in 242.2102 242.4602; do [ -f $OUT/cont241_r0/anm_pin3_D$T.npz ] || { log "no job 4 state D $T: stop"; exit 1; }; done
echo "# $(stamp) UTC sha256 of the inputs: $(cd $OUT/cont241_r0 && sha256sum anm_pin3_D242.2102.npz anm_pin3_D242.4602.npz | cut -c1-16 | tr '\n' ' ')" >> $SUM
# control of exact_recip_check.py delta first: A vs A is 0, A vs B is the log's own difference of sums; its mutation must fail
python3 $OUT/check_delta_control.py $OUT/cont241_r0/anm_pin3_D242.2102.npz $OUT/cont241_r0/anm_pin3_D242.4602.npz $OUT/cont241_r0.log > $OUT/delta_control_job5.txt 2>&1; c0=$?
python3 $OUT/check_delta_control.py $OUT/cont241_r0/anm_pin3_D242.2102.npz $OUT/cont241_r0/anm_pin3_D242.4602.npz $OUT/cont241_r0.log --mutate > $OUT/delta_control_job5_mutate.txt 2>&1; c1=$?
echo "job 5 delta control: exit $c0 (must be 0), --mutate exit $c1 (must be 1)" >> $SUM; log "delta control exit $c0, mutate $c1"
[ $c0 = 0 ] && [ $c1 = 1 ] || { log "delta control failed: stop"; exit 1; }
F="--kfreeze 3 --held_fit data/held_fit.json --held_o 1 --N 31 --jet_o 1 --corrector od --tol_od 1e-60 --qd_it 40 --lam_stall 0.04 --od_junk 0 --reseed 2 --reseed_q 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --reseed_qd_bar 1e-21 --threads 10 --steps 0 --save_base 1 --log_proj 1"
for T in 242.2102 242.4602; do
  S=$OUT/cont241_r0/anm_pin3_D$T.npz
  for R in 0 1; do
    cd $W/hp
    cap=3600; [ $R = 1 ] && cap=7200
    { echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $OUT/resolve${T}_r$R --state $S $F --exact_recip $R"; } > $OUT/resolve${T}_r$R.log
    s0=$(date +%s); nice -n 10 timeout -s TERM $cap python3 -u anm_run.py $RAW $OUT/resolve${T}_r$R --state $S $F --exact_recip $R >> $OUT/resolve${T}_r$R.log 2>&1; rc=$?
    echo "exit $rc" >> $OUT/resolve${T}_r$R.log
    echo "resolve${T}_r$R: exit $rc, $(( $(date +%s) - s0 )) s (cap $cap s); $(python3 $OUT/classify.py $OUT/resolve${T}_r$R.log)" >> $SUM; log "resolve${T}_r$R exit $rc"
  done
  B1=$OUT/resolve${T}_r1/base_pin3_D$T.npz; B0=$OUT/resolve${T}_r0/base_pin3_D$T.npz
  cd $W/hp
  if [ -f $B1 ]; then
    { echo "# $(stamp) UTC cmd: python3 exact_recip_check.py delta $S $B1 --out $OUT/delta_job5_$T.json"; } > $OUT/delta_job5_$T.log
    nice -n 10 timeout -s TERM 1800 python3 exact_recip_check.py delta $S $B1 --out $OUT/delta_job5_$T.json >> $OUT/delta_job5_$T.log 2>&1; rc=$?
    echo "exit $rc" >> $OUT/delta_job5_$T.log
    echo "delta_job5_$T: exit $rc: $(grep 'Delta(b) - Delta(a)' $OUT/delta_job5_$T.log | sed 's/^ *//')" >> $SUM; log "delta_job5_$T exit $rc"
    if [ -f $B0 ]; then
      { echo "# $(stamp) UTC cmd: python3 exact_recip_check.py delta $B0 $B1 --out $OUT/delta$T.json"; } > $OUT/delta$T.log
      nice -n 10 timeout -s TERM 1800 python3 exact_recip_check.py delta $B0 $B1 --out $OUT/delta$T.json >> $OUT/delta$T.log 2>&1; rc=$?
      echo "exit $rc" >> $OUT/delta$T.log
      echo "delta$T: exit $rc: $(grep 'Delta(b) - Delta(a)' $OUT/delta$T.log | sed 's/^ *//')" >> $SUM; log "delta$T exit $rc"
    fi
  else
    echo "delta_job5_$T: no flag-on base saved, no delta" >> $SUM
  fi
done
cd $OUT
python3 classify.py --selftest > classify_selftest_job5.txt 2>&1; s0=$?
python3 classify.py --selftest --mutate > classify_selftest_mutate_job5.txt 2>&1; s1=$?
echo "job 5: classify selftest exit $s0 (0), --mutate exit $s1 (1)" >> $SUM
python3 table1054h.py 242.2102 242.4602 > table_job5.md 2>&1
echo "job 5: table_job5.md written" >> $SUM; log "job 5 done"
exit
}
