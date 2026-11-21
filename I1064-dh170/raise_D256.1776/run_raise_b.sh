#!/bin/bash
# #1064 part 5, second wrapper (coordinator's hc 18:1x UTC 21 Nov: Nathan's decision, the large-D chain pauses; finish the D 256.1776 pair and DROP the D 250.7060 fallback).
# run_raise.sh (pair logic with the fallback) was stopped by exact pid while the control d256_ctl293 was running; the control continues as an orphan (time pid CTLPID). This wrapper waits for it by pid,
# gates it, runs ks 307 with the same command, gates it, and stops: no pair 2. Same flags, caps and gates as run_raise.sh.
CTLPID=${CTLPID:?time pid of the running control}
P=/home/nathan/Source/choptuik-large-d-raw-1064w/I1064-dh170/raise_D256.1776
ROOT=/home/nathan/scratch1064b/raw
WT=/home/nathan/Source/choptuik-large-d-1058b
PY=$WT/.venv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1 PATH=$WT/.venv/bin:$HOME/.local/bin:$HOME/.cargo/bin:$PATH VIRTUAL_ENV=$WT/.venv HP_DIR=$WT/hp
say() { echo "== $(date -u '+%F %T') UTC $*" >> $P/exits_raise.txt; }
B1=I966-dh370/ks_chain3b/leg09_D255.0004_ks293/anm_pin3_D256.1776.npz
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --corrector od --tol_od 1e-60 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 0 --proj_o 1 --reseed_qd_bar 1e-13"
sample() { local N=$1 tp=$2
  local av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
  local py=$(pgrep -P $(pgrep -P $tp | head -1) 2>/dev/null | head -1); local rss=0
  [ -n "$py" ] && rss=$(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status 2>/dev/null)
  echo "$(date -u '+%T') $N MemAvailable $av MiB, anm_run pid ${py:-none} RSS ${rss:-0} MiB" >> $P/memlog_raise.log
  [ "$av" -lt 2048 ] && echo "ALERT $(date -u '+%T') $N MemAvailable $av MiB (alert only)" >> $P/alert_raise.log; }
say "second wrapper armed: waiting for the control's time pid $CTLPID"
while kill -0 $CTLPID 2>/dev/null; do sample d256_ctl293 $CTLPID; sleep 30; done
say "d256_ctl293 ended: $(grep -E 'Exit status|Elapsed' $P/d256_ctl293.log | tr -s '\t ' ' ' | tr '\n' ';')"
say "d256_ctl293 gate903d: $($PY -I $P/gate903d.py $P/d256_ctl293.log)"
say "d256_ctl293 gate973: $($PY -I $P/gate973.py $P/d256_ctl293.log $P/d256_ctl293)"
case "$($PY -I $P/gate903d.py $P/d256_ctl293.log)" in OK*) ;; *) say "STOP: the d256 control (ks 293) did not pass the gate; ks 307 not started"; exit 1;; esac
cd $WT/hp || exit 9
N=d256_ks307
[ -e $P/$N.log ] && { say "refuse: $N.log exists (no overwrite)"; exit 3; }
mkdir -p $P/$N
say "start $N: ks 307 from $B1"
s0=$(date +%s)
nice -n 10 /usr/bin/time -v timeout -s TERM 10800 $PY -u anm_run.py $ROOT $P/$N --state $B1 $F --threads 4 --steps 0 --keep_plan 0 --save_base 1 --ks 307 > $P/$N.log 2>&1 &
tp=$!
while kill -0 $tp 2>/dev/null; do sample $N $tp; sleep 30; done
wait $tp; rc=$?
say "$N exit $rc, $(( $(date +%s) - s0 )) s wall"
say "$N gate903d: $($PY -I $P/gate903d.py $P/$N.log)"
say "$N gate973: $($PY -I $P/gate973.py $P/$N.log $P/$N)"
if ! grep -q "^  on 0: |F|" $P/$N.log; then say "$N: no first od step line completed (first-step failure by the README's reading)"; fi
say "done: pair at D 256.1776 finished; the D 250.7060 fallback is dropped (coordinator)"
