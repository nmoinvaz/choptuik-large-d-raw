#!/bin/bash
# #984 on dh610 (the coordinator's order): base polishes from ks_chain3b's D 242.8630 state (ks 291) at --ks 313 (+22) and 302 (+11) side by side at 8 threads, then
# the control --ks 299 (+8) at 8 threads; run903e.sh's flags with --steps 0 --keep_plan 0 --save_base 1 --reseed_qd_bar 1e-15, 2 h cap each, nice 10. Then near_null.py
# (4 threads) on the state (ks 291) and on every converged base, for sigma_Delta and sigma_pair. hp is origin/main's (the flag is in it), the kernel is #967's build.
. "$(dirname "$0")/common984.sh"
cd "$WT/hp" || exit 1; . $WTV/.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred --reseed_qd_bar 1e-15"
EX=$OUT/exits_984.txt; SUM=$OUT/summary_984.txt
log() { echo "984 $* $(stamp) UTC" >> $EX; }
[ -s $R/$S ] || { log "missing $S"; exit 9; }
log "start, hp $(git rev-parse --short=8 HEAD), hpkernel $(python -c 'import hpkernel; print(hpkernel.__file__)'), load $(cut -d' ' -f1-3 /proc/loadavg)"
polish() { local K=$1 T=$2; mkdir -p $OUT/ks$K
  local s=$(date +%s); timeout -s TERM 7200 nice -n 10 python -u anm_run.py $R $OUT/ks$K --state $S $F --threads $T --steps 0 --keep_plan 0 --save_base 1 --ks $K > $OUT/ks$K.log 2>&1
  local rc=$?; echo "984 ks$K exit $rc wall $(( $(date +%s) - s )) s $(stamp) UTC" >> $EX
  echo "ks$K: $(python3 $OUT/gate984.py $OUT/ks$K.log $OUT/ks$K)" >> $SUM; }
nn() { local N=$1 RD=$2 STATE=$3; nice -n 10 python -u near_null.py $RD $STATE --k=4 --its=16 --threads=4 --json=$OUT/near_null_$N.json > $OUT/near_null_$N.log 2>&1
  echo "984 near_null_$N exit $? $(stamp) UTC" >> $EX; }
polish 313 8 & P1=$!; polish 302 8 & P2=$!
wait $P1 $P2
log "ks313 and ks302 ended"
polish 299 8 & P3=$!
( nn ks291 $R $S
  for K in 313 302; do B=$(ls $OUT/ks$K/base_pin3_D*.npz 2>/dev/null | head -1); [ -n "$B" ] && grep -q "^ks$K: converged" $SUM && nn ks$K $RAW ${B#$RAW/}; done ) &
P4=$!
wait $P3 $P4
B=$(ls $OUT/ks299/base_pin3_D*.npz 2>/dev/null | head -1); [ -n "$B" ] && grep -q "^ks299: converged" $SUM && nn ks299 $RAW ${B#$RAW/}
log "all ended"
