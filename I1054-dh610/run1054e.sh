#!/bin/bash
# #1043 / PR #1054, job (2) of notes/EXACT_RECIP.md 3.6: the default-bound pair at four bases between D 241.96 and 246.44, same worktree of main and venv-i1054 as job (1). A braced block ending in exit.
{
. "$(dirname "$0")/common1054.sh"
X=$OUT/exits_1054.txt; SUM=$OUT/summary_1054.txt
log() { echo "1054e $* $(stamp) UTC" >> $X; }
W59=/home/nathan/Source/choptuik-large-d-1059
[ -d $W59/hp ] || { log "no $W59: stop"; exit 1; }
M59=$(git -C $W59 rev-parse HEAD); [ -z "$(git -C $W59 status --short)" ] || { log "worktree $W59 not clean: stop"; exit 1; }
log "worktree $W59 at $M59, venv-i1054, load $(cut -d' ' -f1-3 /proc/loadavg)"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
. $VENV/bin/activate
cd $W59/hp || exit 1
F="--kfreeze 3 --held_fit data/held_fit.json --held_o 1 --N 31 --jet_o 1 --corrector od --tol_od 1e-60 --qd_it 40 --lam_stall 0.04 --od_junk 0 --reseed 2 --reseed_q 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --reseed_qd_bar 1e-21 --threads 10 --steps 0 --save_base 1 --log_proj 1"
TAGS=""
for S in leg00_D237.7132_ks291/anm_pin3_D242.8630 leg00_D237.7132_ks291/anm_pin3_D243.8361 leg01_D243.8361_ks293/anm_pin3_D244.7177 leg01_D243.8361_ks293/anm_pin3_D245.5586; do
  T=${S##*_D}; TAGS="$TAGS $T"
  for R in 0 1; do
    cd $W59/hp
    { echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $OUT/resolve${T}_r$R --state I966-dh370/ks_chain3b/$S.npz $F --exact_recip $R"; } > $OUT/resolve${T}_r$R.log
    s0=$(date +%s); nice -n 10 timeout -s TERM 21600 python3 -u anm_run.py $RAW $OUT/resolve${T}_r$R --state I966-dh370/ks_chain3b/$S.npz $F --exact_recip $R >> $OUT/resolve${T}_r$R.log 2>&1; rc=$?
    echo "exit $rc" >> $OUT/resolve${T}_r$R.log
    echo "resolve${T}_r$R: exit $rc, $(( $(date +%s) - s0 )) s (cap 21600 s); $(python3 $OUT/classify.py $OUT/resolve${T}_r$R.log)" >> $SUM; log "resolve${T}_r$R exit $rc"
  done
  cd $W59/hp
  { echo "# $(stamp) UTC cmd: python3 exact_recip_check.py delta $OUT/resolve${T}_r0/base_pin3_D$T.npz $OUT/resolve${T}_r1/base_pin3_D$T.npz --out $OUT/delta$T.json"; } > $OUT/delta$T.log
  nice -n 10 timeout -s TERM 1800 python3 exact_recip_check.py delta $OUT/resolve${T}_r0/base_pin3_D$T.npz $OUT/resolve${T}_r1/base_pin3_D$T.npz --out $OUT/delta$T.json >> $OUT/delta$T.log 2>&1; rc=$?
  echo "exit $rc" >> $OUT/delta$T.log
  echo "delta$T: exit $rc: $(grep 'Delta(b) - Delta(a)' $OUT/delta$T.log | sed 's/^ *//')" >> $SUM; log "delta$T exit $rc"
done
cd $OUT
python3 table1054.py 1 $TAGS > table_job2.md 2>&1
echo "job 2: table_job2.md written for$TAGS" >> $SUM; log "job 2 done"
exit
}
