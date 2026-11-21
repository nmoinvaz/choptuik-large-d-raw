#!/bin/bash
# #1043 job 6 (coordinator's task of 21 Nov): job 4 again with notes/EXACT_RECIP.md 3.5's Newton flags. The two D 241.96 bases (resolve241_r0, flag off, resolve241_r1, flag on) continued 4 steps of a fixed 0.25
# (D 242.21, 242.46, 242.71, 242.96) with --od_accept natural --od_strong 4 --reseed_start pred --reseed_qd_bar 1e-21 and --N 31 --qd_it 40 --lam_stall 0.04. Reading (b): when one run refuses an attempt, both stop
# (refusal.py, polled every 30 s, the run's exact pid; the flag-off run goes first, and the flag-on run is not started if it refused). Main 796f4bac in the job 4 worktree, venv-i1054. A braced block ending in exit.
{
. "$(dirname "$0")/common1054.sh"
X=$OUT/exits_1054.txt; SUM=$OUT/summary_1054.txt
log() { echo "1054i $* $(stamp) UTC" >> $X; }
W=/home/nathan/Source/choptuik-large-d-1043g
M=$(git -C $W rev-parse HEAD) || exit 1
git -C $REPO merge-base --is-ancestor 796f4bac $M || { log "796f4bac is not an ancestor of $M: stop"; exit 1; }
[ -z "$(git -C $W status --short)" ] || { log "worktree $W not clean: stop"; exit 1; }
for R in 0 1; do [ -f $OUT/resolve241_r$R/base_pin3_D241.9602.npz ] || { log "the base of r$R is missing: stop"; exit 1; }; done
log "worktree $W at $M, venv-i1054, load $(cut -d' ' -f1-3 /proc/loadavg)"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
. $VENV/bin/activate
cd $OUT
python3 refusal.py --selftest > refusal_selftest_job6.txt 2>&1; q1=$?; python3 refusal.py --selftest --mutate > refusal_selftest_mutate_job6.txt 2>&1; q2=$?
echo "job 6: refusal.py selftest exit $q1 (0), --mutate exit $q2 (1)" >> $SUM; log "refusal selftest $q1 mutate $q2"
[ $q1 = 0 ] && [ $q2 = 1 ] || { log "refusal.py controls wrong: stop"; exit 1; }
cd $W/hp || exit 1
F="--kfreeze 3 --held_fit data/held_fit.json --held_o 1 --N 31 --jet_o 1 --corrector od --tol_od 1e-60 --qd_it 40 --lam_stall 0.04 --od_junk 0 --reseed 2 --reseed_q 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --reseed_qd_bar 1e-21 --threads 10 --a0 0.25 --h_max 0.25 --a_grow 1 --steps 4 --D_max 300"
refused=""
for R in 0 1; do
  [ -z "$refused" ] || { echo "job6_r$R: not started, job6_r$refused refused an attempt (reading (b): both stop)" >> $SUM; log "job6_r$R not started"; continue; }
  cd $W/hp
  { echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $OUT/job6_r$R --state $OUT/resolve241_r$R/base_pin3_D241.9602.npz $F --exact_recip $R"; } > $OUT/job6_r$R.log
  s0=$(date +%s); stop=""
  nice -n 10 python3 -u anm_run.py $RAW $OUT/job6_r$R --state $OUT/resolve241_r$R/base_pin3_D241.9602.npz $F --exact_recip $R >> $OUT/job6_r$R.log 2>&1 &
  pid=$!; log "job6_r$R started, pid $pid"
  while kill -0 $pid 2>/dev/null; do
    sleep 30
    python3 $OUT/refusal.py $OUT/job6_r$R.log > $OUT/refusal_job6_r$R.txt 2>&1; rr=$?
    if [ $rr = 1 ]; then stop="stopped at its first refusal: $(cat $OUT/refusal_job6_r$R.txt)"; refused=$R; kill -TERM $pid; break; fi
    if [ $(( $(date +%s) - s0 )) -ge 18000 ]; then stop="cap 18000 s"; refused=$R; kill -TERM $pid; break; fi
  done
  wait $pid; rc=$?
  echo "exit $rc" >> $OUT/job6_r$R.log
  python3 $OUT/refusal.py $OUT/job6_r$R.log > $OUT/refusal_job6_r$R.txt 2>&1; rr=$?
  [ $rr = 1 ] && refused=$R
  echo "job6_r$R: exit $rc, $(( $(date +%s) - s0 )) s; refusal.py exit $rr: $(head -1 $OUT/refusal_job6_r$R.txt); ${stop:-ran to its end}; states: $(ls $OUT/job6_r$R 2>/dev/null | grep -c 'anm_pin3_D') saved" >> $SUM; log "job6_r$R exit $rc, refusal.py $rr ${stop}"
done
cd $W/hp
dl() {  # dl OFF.npz ON.npz OUTJSON LOG
  { echo "# $(stamp) UTC cmd: python3 exact_recip_check.py delta $1 $2 --out $3"; } > $4
  nice -n 10 timeout -s TERM 1800 python3 exact_recip_check.py delta $1 $2 --out $3 >> $4 2>&1; rc=$?
  echo "exit $rc" >> $4
  echo "$(basename $3): exit $rc: $(grep 'Delta(b) - Delta(a)' $4 | sed 's/^ *//')" >> $SUM; log "$(basename $3) exit $rc"
}
for p in $OUT/job6_r0/anm_pin3_D*.npz; do
  [ -f "$p" ] || continue
  b=$(basename $p .npz); Ds=${b#anm_pin3_D}
  [ -f $OUT/job6_r1/$b.npz ] || { echo "delta_job6_$Ds: no flag-on state" >> $SUM; continue; }
  dl $OUT/job6_r0/$b.npz $OUT/job6_r1/$b.npz $OUT/delta_job6_$Ds.json $OUT/delta_job6_$Ds.log
done
# consistency checks at the two D that jobs 4 and 5 also have (xcheck_job6.py: same equations, same D, Delta to 1e-30; ctl: the flag's own change, must exceed it)
for Ds in 242.2102 242.4602; do
  b=anm_pin3_D$Ds
  [ -f $OUT/job6_r0/$b.npz ] && dl $OUT/cont241_r0/$b.npz $OUT/job6_r0/$b.npz $OUT/xc_off_$Ds.json $OUT/xc_off_$Ds.log
  [ -f $OUT/job6_r1/$b.npz ] && dl $OUT/resolve${Ds}_r1/base_pin3_D$Ds.npz $OUT/job6_r1/$b.npz $OUT/xc_on_$Ds.json $OUT/xc_on_$Ds.log
  [ -f $OUT/job6_r0/$b.npz ] && [ -f $OUT/resolve${Ds}_r1/base_pin3_D$Ds.npz ] && dl $OUT/job6_r0/$b.npz $OUT/resolve${Ds}_r1/base_pin3_D$Ds.npz $OUT/xc_ctl_$Ds.json $OUT/xc_ctl_$Ds.log
done
cd $OUT
python3 xcheck_job6.py > xcheck_job6.txt 2>&1; x1=$?; python3 xcheck_job6.py --mutate > xcheck_job6_mutate.txt 2>&1; x2=$?
python3 table1054i.py > table_job6.md 2>&1
echo "job 6: table_job6.md written; xcheck exit $x1 (0), --mutate exit $x2 (1)" >> $SUM; log "job 6 summary: xcheck $x1 mutate $x2"
log "job 6 done"
exit
}
