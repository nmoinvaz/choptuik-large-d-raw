#!/bin/bash
# #1064 part 5 (coordinator's hc ~17:43 UTC 21 Nov, amendment 2): where the raise still converges, nearer the front. Part 4's command (leg 13's line with --tol_od 1e-60 --od_floor_delta 0, --steps 0 --save_base 1 --keep_plan 0 --ks K),
# 4 threads, nice 10, 3 h cap each (timeout -s TERM 10800), gates gate903d.py and gate973.py. Pair 1: base I966-dh370/ks_chain3b/leg09_D255.0004_ks293/anm_pin3_D256.1776.npz, the control --ks 293 then --ks 307.
# If ks 307 fails at its first step (no 'on 0: |F|' od step line completed), pair 2 at leg02's D 250.7060 base, then stop either way. A failed control stops the work.
P=/home/nathan/Source/choptuik-large-d-raw-1064w/I1064-dh170/raise_D256.1776
ROOT=/home/nathan/scratch1064b/raw
WT=/home/nathan/Source/choptuik-large-d-1058b
PY=$WT/.venv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1 PATH=$WT/.venv/bin:$HOME/.local/bin:$HOME/.cargo/bin:$PATH VIRTUAL_ENV=$WT/.venv HP_DIR=$WT/hp
say() { echo "== $(date -u '+%F %T') UTC $*" >> $P/exits_raise.txt; }
B1=I966-dh370/ks_chain3b/leg09_D255.0004_ks293/anm_pin3_D256.1776.npz; H1=8bf87d8f94cf
B2=I966-dh370/ks_chain3b/leg02_D247.2801_ks293/anm_pin3_D250.7060.npz; H2=104dddd2748a
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --corrector od --tol_od 1e-60 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 0 --proj_o 1 --reseed_qd_bar 1e-13"
cd $WT/hp || exit 9
run() { local N=$1 K=$2 S=$3
  [ -e $P/$N.log ] && { say "refuse: $N.log exists (no overwrite)"; return 3; }
  mkdir -p $P/$N
  say "start $N: ks $K from $S"
  local s0=$(date +%s)
  nice -n 10 /usr/bin/time -v timeout -s TERM 10800 $PY -u anm_run.py $ROOT $P/$N --state $S $F --threads 4 --steps 0 --keep_plan 0 --save_base 1 --ks $K > $P/$N.log 2>&1 &
  local tp=$!
  while kill -0 $tp 2>/dev/null; do
    local av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
    local py=$(pgrep -P $(pgrep -P $tp | head -1) 2>/dev/null | head -1); local rss=0
    [ -n "$py" ] && rss=$(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status 2>/dev/null)
    echo "$(date -u '+%T') $N MemAvailable $av MiB, anm_run pid ${py:-none} RSS ${rss:-0} MiB" >> $P/memlog_raise.log
    [ "$av" -lt 2048 ] && echo "ALERT $(date -u '+%T') $N MemAvailable $av MiB (alert only)" >> $P/alert_raise.log
    sleep 30
  done
  wait $tp; local rc=$?
  say "$N exit $rc, $(( $(date +%s) - s0 )) s wall"
  say "$N gate903d: $($PY -I $P/gate903d.py $P/$N.log)"
  say "$N gate973: $($PY -I $P/gate973.py $P/$N.log $P/$N)"
  return $rc
}
ok() { case "$($PY -I $P/gate903d.py $P/$1.log)" in OK*) return 0;; *) return 1;; esac; }
first_step_failed() { ! grep -q "^  on 0: |F|" $P/$1.log; }
pair() { local T=$1 S=$2 H=$3
  [ "$(git hash-object --no-filters $ROOT/$S | cut -c1-12)" = $H ] || { say "refuse: base blob of $S is not $H"; exit 2; }
  run ${T}_ctl293 293 $S
  ok ${T}_ctl293 || { say "STOP: the $T control (ks 293) did not pass the gate; ks 307 not started"; exit 1; }
  run ${T}_ks307 307 $S
  if ok ${T}_ks307; then say "$T ks 307 PASSED the gate"; return 0; fi
  if first_step_failed ${T}_ks307; then say "$T ks 307 FAILED AT ITS FIRST STEP (no od step line completed)"; return 2; fi
  say "$T ks 307 failed the gate after its first od step completed"; return 3
}
pair d256 $B1 $H1; r=$?
if [ $r -eq 0 ]; then say "done: ks 307 converges at D 256.1776; stop (the order arm is the coordinator's)"; exit 0; fi
if [ $r -eq 2 ]; then say "ks 307 failed at its first step at D 256.1776: pair 2 at D 250.7060"; pair d250 $B2 $H2; r2=$?; say "done: pair 2 result code $r2 (0 passed, 2 failed at its first step, 3 failed later); stop either way"; exit 0; fi
say "done: ks 307 failed after its first step at D 256.1776 (code $r): stopped, not the order's first-step case; the coordinator decides"
