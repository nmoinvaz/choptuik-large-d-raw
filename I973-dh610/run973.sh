#!/bin/bash
# #973 on dh610: base polishes from ks_chain2's D 237.7132 state at --ks 297, 301, 303, 307 side by side (5 threads each, nice 10, 1 h cap
# each), then --ks 293 alone (6 threads, as #971). run903e.sh's flags, --steps 0 --keep_plan 0 --save_base 1.
. "$(dirname "$0")/common973.sh"
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
EX=$OUT/exits_973.txt; SUM=$OUT/summary_973.txt
log() { echo "973 $* $(stamp) UTC" >> $EX; }
[ -s $R/$S ] || { log "missing $S"; exit 9; }
log "start, hp $(git rev-parse --short=8 HEAD), hpkernel $(python -c 'import hpkernel; print(hpkernel.__file__)'), load $(cut -d' ' -f1-3 /proc/loadavg)"
polish() { # K threads name
  local K=$1 T=$2 N=$3; mkdir -p $OUT/$N
  s=$(date +%s); timeout -s TERM 3600 nice -n 10 python -u anm_run.py $R $OUT/$N --state $S $F --threads $T --steps 0 --keep_plan 0 --save_base 1 --ks $K > $OUT/$N.log 2>&1
  rc=$?; echo "973 $N exit $rc wall $(( $(date +%s) - s )) s $(stamp) UTC" >> $EX
  echo "$N: $(python3 $OUT/gate973.py $OUT/$N.log $OUT/$N)" >> $SUM
}
PIDS=""
for K in 297 301 303 307; do polish $K 5 ks$K & PIDS="$PIDS $!"; done
wait $PIDS
log "the four side-by-side polishes ended, load $(cut -d' ' -f1-3 /proc/loadavg)"
polish 293 6 ks293_rerun
echo "# run973 done $(stamp) UTC" >> $SUM
