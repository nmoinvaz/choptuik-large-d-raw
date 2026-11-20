#!/bin/bash
# PR #1054, #1043's flag-on pairs at D 246.44 and 249.47 (coordinator's task of 20 Nov ~18:15 UTC): the worktree at 4204c9f9 as the D 251.88 rerun left it (no fetch, no rebuild), venv-i1054, from hp/:
# for each state the flag-off and flag-on polish (--exact_recip 0 and 1, the D 251.88 flags with --log_proj 1) and exact_recip_check.py delta, then the pass rule per polish (check251b.py) and the changes against D (fit_change.py).
# The whole script is one braced block that ends in exit, so that bash has read it all before it runs (an edit of the file cannot change a running unit).
{
. "$(dirname "$0")/common1054.sh"
X=$OUT/exits_1054.txt; SUM=$OUT/summary_1054.txt
log() { echo "1054c $* $(stamp) UTC" >> $X; }
cd $W || exit 1
HC=$(git rev-parse HEAD)
[ "$HC" = 4204c9f94d030aef508131c41a4573cd9b9de64e ] || { log "worktree HEAD is $HC, not 4204c9f9: stop"; exit 1; }
[ -z "$(git status --short)" ] || { log "worktree not clean: stop"; exit 1; }
log "git rev-parse HEAD $HC (no fetch, no rebuild), load $(cut -d' ' -f1-3 /proc/loadavg)"
echo "# $(stamp) UTC 1054c: HEAD $HC, hpkernel $($VENV/bin/python -c 'import hpkernel;print(hpkernel.__file__, hpkernel.isa())' 2>&1 | tail -1)" >> $SUM
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
. $VENV/bin/activate
cd $W/hp || exit 1
F="--kfreeze 3 --held_fit data/held_fit.json --held_o 1 --N 31 --jet_o 1 --corrector od --tol_od 1e-60 --qd_it 40 --lam_stall 0.04 --od_junk 0 --reseed 2 --reseed_q 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --reseed_qd_bar 1e-21 --threads 10 --steps 0 --save_base 1 --log_proj 1"
for ST in leg01_D243.8361_ks293/anm_pin3_D246.4399 leg02_D247.2801_ks293/anm_pin3_D249.4664; do
  T=${ST##*_D}
  for R in 0 1; do
    cd $W/hp
    { echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $OUT/resolve${T}_r$R --state I966-dh370/ks_chain3b/$ST.npz $F --exact_recip $R"; } > $OUT/resolve${T}_r$R.log
    s0=$(date +%s); nice -n 10 timeout -s TERM 21600 python3 -u anm_run.py $RAW $OUT/resolve${T}_r$R --state I966-dh370/ks_chain3b/$ST.npz $F --exact_recip $R >> $OUT/resolve${T}_r$R.log 2>&1; rc=$?
    echo "exit $rc" >> $OUT/resolve${T}_r$R.log
    cd $OUT; python3 check251b.py resolve${T}_r$R.log > check_${T}_r$R.txt 2>&1; rr=$?
    echo "resolve${T}_r$R: exit $rc, $(( $(date +%s) - s0 )) s (cap 21600 s); rule (check251b.py) exit $rr: $(tail -1 check_${T}_r$R.txt); $(grep -E 'octo-double Newton:|attempt stopped|base polish' resolve${T}_r$R.log | cut -c1-140 | tr '\n' ';')" >> $SUM
    log "resolve${T}_r$R exit $rc, rule exit $rr"
  done
  cd $W/hp
  { echo "# $(stamp) UTC cmd: python3 exact_recip_check.py delta $OUT/resolve${T}_r0/base_pin3_D$T.npz $OUT/resolve${T}_r1/base_pin3_D$T.npz --out $OUT/delta$T.json"; } > $OUT/delta$T.log
  nice -n 10 timeout -s TERM 1800 python3 exact_recip_check.py delta $OUT/resolve${T}_r0/base_pin3_D$T.npz $OUT/resolve${T}_r1/base_pin3_D$T.npz --out $OUT/delta$T.json >> $OUT/delta$T.log 2>&1; rc=$?
  echo "exit $rc" >> $OUT/delta$T.log
  echo "delta$T: exit $rc: $(grep 'Delta(b) - Delta(a)' $OUT/delta$T.log | sed 's/^ *//')" >> $SUM; log "delta$T exit $rc"
done
# the changes against D: the pairs whose two polishes both pass the rule, with D 241.96's (resolve241_r0/r1 of the D 251.88 task's first runs)
cd $OUT
FILES="delta241.json"; for T in 246.4399 249.4664; do
  if python3 check251b.py resolve${T}_r0.log > /dev/null 2>&1 && python3 check251b.py resolve${T}_r1.log > /dev/null 2>&1 && [ -f delta$T.json ]; then FILES="$FILES delta$T.json"; fi
done
python3 fit_change.py $FILES > fit_change.txt 2>&1; rc=$?
python3 fit_change.py --selftest > fit_change_selftest.txt 2>&1; r1=$?; python3 fit_change.py --selftest --mutate > fit_change_selftest_mutate.txt 2>&1; r2=$?
echo "fit_change.py $FILES: exit $rc; selftest exit $r1 (0), --selftest --mutate exit $r2 (1)" >> $SUM; log "fit exit $rc selftest $r1 mutate $r2"
log "all steps done"
exit
}
