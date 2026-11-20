#!/bin/bash
# #1043 job 4 (coordinator's task of 20 Nov): the two D 241.96 bases (resolve241_r0, flag off, and resolve241_r1, flag on) continued two steps of a fixed 0.25 in D each, with crawlJ's flags (notes/EXACT_RECIP.md 3.3)
# plus --a0 0.25 --h_max 0.25 --a_grow 1 --steps 2 --D_max 300; main 796f4bac in a new worktree, venv-i1054's python. Reading (a): a run is stopped at its first refused attempt (refusal.py, polled every 30 s, the
# run's exact pid) and the other run still goes, so that both logs' step lines exist. A braced block ending in exit.
{
. "$(dirname "$0")/common1054.sh"
X=$OUT/exits_1054.txt; SUM=$OUT/summary_1054.txt
log() { echo "1054g $* $(stamp) UTC" >> $X; }
W=/home/nathan/Source/choptuik-large-d-1043g
M=$(git -C $W rev-parse HEAD) || exit 1
git -C $REPO merge-base --is-ancestor 796f4bac $M || { log "796f4bac is not an ancestor of $M: stop"; exit 1; }
[ -z "$(git -C $W status --short)" ] || { log "worktree $W not clean: stop"; exit 1; }
for R in 0 1; do [ -f $OUT/resolve241_r$R/base_pin3_D241.9602.npz ] || { log "the base of r$R is missing: stop"; exit 1; }; done
log "worktree $W at $M, venv-i1054, load $(cut -d' ' -f1-3 /proc/loadavg)"
echo "# $(stamp) UTC 1054g: main $M in $W; hp changes against 8179068d (the worktree of jobs 1 to 3): $(git -C $REPO diff --name-only 8179068d $M -- hp | tr '\n' ' ')" >> $SUM
echo "# 1054g: Solver.set_exact_recip in venv-i1054: $($VENV/bin/python -c 'import hpkernel;print(hasattr(hpkernel.Solver, "set_exact_recip"))' 2>&1 | tail -1)" >> $SUM
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
. $VENV/bin/activate
cd $W/hp || exit 1
F="--kfreeze 3 --held_fit data/held_fit.json --held_o 1 --N 24 --jet_o 1 --corrector od --tol_od 1e-60 --qd_it 12 --lam_stall 0.04 --od_junk 0 --reseed 2 --reseed_q 1 --reseed_o 3 --threads 10 --a0 0.25 --h_max 0.25 --a_grow 1 --steps 2 --D_max 300"
for R in 0 1; do
  cd $W/hp
  { echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $OUT/cont241_r$R --state $OUT/resolve241_r$R/base_pin3_D241.9602.npz $F --exact_recip $R"; } > $OUT/cont241_r$R.log
  s0=$(date +%s); stop=""
  nice -n 10 python3 -u anm_run.py $RAW $OUT/cont241_r$R --state $OUT/resolve241_r$R/base_pin3_D241.9602.npz $F --exact_recip $R >> $OUT/cont241_r$R.log 2>&1 &
  pid=$!; log "cont241_r$R started, pid $pid"
  while kill -0 $pid 2>/dev/null; do
    sleep 30
    python3 $OUT/refusal.py $OUT/cont241_r$R.log > $OUT/refusal_r$R.txt 2>&1; rr=$?
    if [ $rr = 1 ]; then stop="stopped at its first refusal: $(cat $OUT/refusal_r$R.txt)"; kill -TERM $pid; break; fi
    if [ $(( $(date +%s) - s0 )) -ge 21600 ]; then stop="cap 21600 s"; kill -TERM $pid; break; fi
  done
  wait $pid; rc=$?
  echo "exit $rc" >> $OUT/cont241_r$R.log
  python3 $OUT/refusal.py $OUT/cont241_r$R.log > $OUT/refusal_r$R.txt 2>&1; rr=$?
  echo "cont241_r$R: exit $rc, $(( $(date +%s) - s0 )) s; refusal.py exit $rr: $(cat $OUT/refusal_r$R.txt | head -1); ${stop:-ran to its end}; states: $(ls $OUT/cont241_r$R 2>/dev/null | grep -c 'anm_pin3_D') saved" >> $SUM; log "cont241_r$R exit $rc, refusal.py $rr ${stop}"
done
cd $W/hp
for p in $OUT/cont241_r0/anm_pin3_D*.npz; do
  [ -f "$p" ] || continue
  b=$(basename $p .npz); Ds=${b#anm_pin3_D}
  [ -f $OUT/cont241_r1/$b.npz ] || { echo "delta_cont$Ds: no flag-on state" >> $SUM; continue; }
  { echo "# $(stamp) UTC cmd: python3 exact_recip_check.py delta $OUT/cont241_r0/$b.npz $OUT/cont241_r1/$b.npz --out $OUT/delta_cont$Ds.json"; } > $OUT/delta_cont$Ds.log
  nice -n 10 timeout -s TERM 1800 python3 exact_recip_check.py delta $OUT/cont241_r0/$b.npz $OUT/cont241_r1/$b.npz --out $OUT/delta_cont$Ds.json >> $OUT/delta_cont$Ds.log 2>&1; rc=$?
  echo "exit $rc" >> $OUT/delta_cont$Ds.log
  echo "delta_cont$Ds: exit $rc: $(grep 'Delta(b) - Delta(a)' $OUT/delta_cont$Ds.log | sed 's/^ *//')" >> $SUM; log "delta_cont$Ds exit $rc"
done
cd $OUT
python3 refusal.py --selftest > refusal_selftest.txt 2>&1; r1=$?; python3 refusal.py --selftest --mutate > refusal_selftest_mutate.txt 2>&1; r2=$?
python3 table1054g.py > table_job4.md 2>&1
echo "job 4: table_job4.md written; refusal.py selftest exit $r1 (0), --mutate exit $r2 (1)" >> $SUM; log "job 4 summary: refusal selftest $r1 mutate $r2"
log "job 4 done"
exit
}
