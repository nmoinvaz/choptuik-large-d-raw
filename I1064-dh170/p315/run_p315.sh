#!/bin/bash
# #1064 part 4 (coordinator's hc ~15:50 UTC 21 Nov): polish #973's ks 307 base (D 237.7132) to ks 315 with leg 13's flags, the ks 307 control first.
# Gate: start only after the #1025 D 17.75 part 2 lane (pid LANE) has exited; 4 threads, nice 10, 3 h cap each (timeout -s TERM 10800, by pid); verdict by gate903d.py and gate973.py.
# usage: bash run_p315.sh     (writes exits_p315.txt, memlog_p315.log, alert_p315.log, ks307_ctl.log/, ks315.log/ beside it)
LANE=${LANE:-1115101}
P=/home/nathan/Source/choptuik-large-d-raw-1064w/I1064-dh170/p315
WT=/home/nathan/Source/choptuik-large-d-1058b
ROOT=/home/nathan/scratch1064b/raw
S=I973-dh610/ks307_r2/base_pin3_D237.7132.npz
PY=$WT/.venv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1 PATH=$WT/.venv/bin:$HOME/.local/bin:$HOME/.cargo/bin:$PATH VIRTUAL_ENV=$WT/.venv HP_DIR=$WT/hp
say() { echo "== $(date -u '+%F %T') UTC $*" >> $P/exits_p315.txt; }
# leg 13's flags (I966-dh370 ks_chain3b_q_dry.log, line 17) with --tol_od 1e-60 as #973/ladder966 used for base polishes and --od_floor_delta 0 (coordinator's hc 16:2x UTC: leg 13's 1e-30 ends the corrector by the floor rule near 1e-41, dh610's comment 7065633932) (README), threads 4, and the order's --steps 0 --keep_plan 0 --save_base 1 --ks K
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --corrector od --tol_od 1e-60 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 0 --proj_o 1 --reseed_qd_bar 1e-13"
say "armed: waiting for the #1025 lane (pid $LANE)"
while kill -0 $LANE 2>/dev/null; do sleep 30; done
say "gate open: the lane has exited, load $(cut -d' ' -f1-3 /proc/loadavg)"
[ "$(git hash-object --no-filters $ROOT/$S | cut -c1-12)" = 5b10a9fd4cc4 ] || { say "refuse: base blob is not 5b10a9fd4cc4"; exit 2; }
cd $WT/hp || exit 9
run() { local K=$1 N=$2
  [ -e $P/$N.log ] && { say "refuse: $N.log exists (no overwrite)"; return 3; }
  say "start $N: ks $K"
  local s0=$(date +%s)
  nice -n 10 /usr/bin/time -v timeout -s TERM 10800 $PY -u anm_run.py $ROOT $P/$N --state $S $F --threads 4 --steps 0 --keep_plan 0 --save_base 1 --ks $K > $P/$N.log 2>&1 &
  local tp=$!
  while kill -0 $tp 2>/dev/null; do
    local av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
    local py=$(pgrep -P $(pgrep -P $tp | head -1) 2>/dev/null | head -1); local rss=0
    [ -n "$py" ] && rss=$(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status 2>/dev/null)
    echo "$(date -u '+%T') $N MemAvailable $av MiB, anm_run pid ${py:-none} RSS ${rss:-0} MiB" >> $P/memlog_p315.log
    [ "$av" -lt 2048 ] && echo "ALERT $(date -u '+%T') $N MemAvailable $av MiB (alert only)" >> $P/alert_p315.log
    sleep 30
  done
  wait $tp; local rc=$?
  say "$N exit $rc, $(( $(date +%s) - s0 )) s wall"
  say "$N gate903d: $($PY -I $P/gate903d.py $P/$N.log)"
  say "$N gate973: $($PY -I $P/gate973.py $P/$N.log $P/$N)"
  return $rc
}
run 307 ks307_ctl
g=$($PY -I $P/gate903d.py $P/ks307_ctl.log)
case "$g" in OK*) ;; *) say "STOP: the ks 307 control did not pass the gate ($g); the ks 315 run is not started"; exit 1;; esac
run 315 ks315
say "done"
