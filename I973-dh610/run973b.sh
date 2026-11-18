#!/bin/bash
# #973 second attempt on dh610: the four side-by-side runs hit the 1 h cap at 5 threads on a loaded machine (20 threads on 20 logical cpus, item 3 beside), with
# ks 297 and 301 on the converging path and ks 303 and 307 still in their first strong chord. The same polishes again, 6 threads each (#971's conditions: 18
# threads in all with the ks 293 rerun), 1 h cap each, nice 10: ks 297 and 301 first, then ks 303 and 307. Names ks<K>_r2.
. "$(dirname "$0")/common973.sh"
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
EX=$OUT/exits_973.txt; SUM=$OUT/summary_973.txt
log() { echo "973b $* $(stamp) UTC" >> $EX; }
log "second attempt start, load $(cut -d' ' -f1-3 /proc/loadavg)"
polish() { local K=$1 T=$2 N=$3; mkdir -p $OUT/$N
  local s=$(date +%s); timeout -s TERM 3600 nice -n 10 python -u anm_run.py $R $OUT/$N --state $S $F --threads $T --steps 0 --keep_plan 0 --save_base 1 --ks $K > $OUT/$N.log 2>&1
  local rc=$?; echo "973 $N exit $rc wall $(( $(date +%s) - s )) s $(stamp) UTC" >> $EX
  echo "$N: $(python3 $OUT/gate973.py $OUT/$N.log $OUT/$N)" >> $SUM; }
polish 297 6 ks297_r2 & P1=$!; polish 301 6 ks301_r2 & P2=$!
wait $P1 $P2
log "ks297_r2 and ks301_r2 ended"
polish 303 6 ks303_r2 & P3=$!; polish 307 6 ks307_r2 & P4=$!
wait $P3 $P4
log "ks303_r2 and ks307_r2 ended"
