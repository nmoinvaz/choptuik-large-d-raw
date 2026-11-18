#!/bin/bash
# #971 on dh610 (the coordinator's order, hc 2026-11-18): base polishes from ks_chain2's D 237.7132 state at --ks 293, 295, 299 (+2, +4, +8),
# run903e.sh's flags at 6 threads each, side by side, nice 10, each capped at 1 h. A rung that fails stops the larger rungs still running.
. "$(dirname "$0")/common971.sh"
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 6 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
EX=$OUT/exits_971.txt; SUM=$OUT/summary_971.txt
log() { echo "971 $* $(stamp) UTC" >> $EX; }
[ -s $R/$S ] || { log "missing $S"; exit 9; }
log "start, hp $(git rev-parse --short=8 HEAD), hpkernel $(python -c 'import hpkernel; print(hpkernel.__file__)'), load $(cut -d' ' -f1-3 /proc/loadavg)"
KS="293 295 299"; declare -A PID
for K in $KS; do
  mkdir -p $OUT/ks$K
  ( s=$(date +%s); timeout -s TERM 3600 nice -n 10 python -u anm_run.py $R $OUT/ks$K --state $S $F --steps 0 --keep_plan 0 --save_base 1 --ks $K > $OUT/ks$K.log 2>&1
    rc=$?; echo "971 ks$K exit $rc wall $(( $(date +%s) - s )) s $(stamp) UTC" >> $EX ) &
  PID[$K]=$!
done
done_=""; stop=""
while :; do
  alive=0
  for K in $KS; do
    case " $done_ " in *" $K "*) continue;; esac
    if kill -0 ${PID[$K]} 2>/dev/null; then alive=1; continue; fi
    done_="$done_ $K"
    v=$(python3 $OUT/gate971.py $OUT/ks$K.log $OUT/ks$K); echo "ks$K: $v" >> $SUM
    if [ "${v%%:*}" = failed ]; then
      for K2 in $KS; do
        [ $K2 -gt $K ] && kill -0 ${PID[$K2]} 2>/dev/null && { pkill -TERM -P ${PID[$K2]} 2>/dev/null; log "ks$K failed, stopping ks$K2"; }
      done
    fi
  done
  [ $alive = 0 ] && break
  sleep 20
done
echo "# run971 done $(stamp) UTC" >> $SUM
