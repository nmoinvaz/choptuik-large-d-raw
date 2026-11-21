#!/bin/bash
# #1064 part 5 (coordinator's hc ~17:40 UTC 21 Nov): cost pilot of a higher-order chain from D 237.7132: from part 4's ks 315 base, leg 13's line with --ks 315 --keep_plan 1 --steps 3,
# 4 threads, nice 10, 4 h cap (timeout -s TERM 14400), output here (a worktree of the raw repository: anm_run refuses output elsewhere). Writes exits_pilot315.txt, memlog_pilot315.log, stamps_pilot315.log, anm_run.log.
P=/home/nathan/Source/choptuik-large-d-raw-1064w/I1064-dh170/pilot315
RAW=/home/nathan/Source/choptuik-large-d-raw-1064w
WT=/home/nathan/Source/choptuik-large-d-1058b
S=I1064-dh170/p315/ks315/base_pin3_D237.7132.npz
PY=$WT/.venv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1 PATH=$WT/.venv/bin:$HOME/.local/bin:$HOME/.cargo/bin:$PATH VIRTUAL_ENV=$WT/.venv HP_DIR=$WT/hp
say() { echo "== $(date -u '+%F %T') UTC $*" >> $P/exits_pilot315.txt; }
[ -e $P/anm_run.log ] && { say "refuse: anm_run.log exists (no overwrite)"; exit 3; }
[ "$(git hash-object --no-filters $RAW/$S | cut -c1-12)" = 0f4858eef006 ] || { say "refuse: base blob is not 0f4858eef006"; exit 2; }
# leg 13's flags as in I966-dh370/ks_chain3b_q_dry.log line 17 (tol_od 2e-34, od_floor_delta 1e-30 as in leg 13), threads 4, --steps 3 --ks 315 --keep_plan 1, --D_max the leg's D + 10
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13"
cd $WT/hp || exit 9
say "start: $F --threads 4 --steps 3 --ks 315 --keep_plan 1 --D_max 247.7132, state $S, load $(cut -d' ' -f1-3 /proc/loadavg)"
s0=$(date +%s)
nice -n 10 /usr/bin/time -v timeout -s TERM 14400 $PY -u anm_run.py $RAW $P --state $S $F --threads 4 --steps 3 --ks 315 --keep_plan 1 --D_max 247.7132 > $P/anm_run.log 2>&1 &
tp=$!
( tail -n 0 -F $P/anm_run.log | awk '/ a [0-9.]+ -> D |^step [0-9]+:|re-seeded|refused|octo-double Newton|on [0-9]+: strong chord/ {cmd="date -u +%T"; cmd | getline t; close(cmd); print t " " $0; fflush()}' >> $P/stamps_pilot315.log ) &
sp=$!
while kill -0 $tp 2>/dev/null; do
  av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
  py=$(pgrep -P $(pgrep -P $tp | head -1) 2>/dev/null | head -1); rss=0
  [ -n "$py" ] && rss=$(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status 2>/dev/null)
  echo "$(date -u '+%T') MemAvailable $av MiB, anm_run pid ${py:-none} RSS ${rss:-0} MiB" >> $P/memlog_pilot315.log
  [ "$av" -lt 2048 ] && echo "ALERT $(date -u '+%T') MemAvailable $av MiB (alert only)" >> $P/alert_pilot315.log
  sleep 30
done
wait $tp; rc=$?
kill $sp 2>/dev/null
say "anm_run exit $rc, $(( $(date +%s) - s0 )) s wall"
say "done"
