#!/bin/bash
# #1064 part 9 (coordinator's hc ~21:45 UTC 21 Nov): part 6's exact command PLUS --proj_o_bar 2e-34 on part 7's build (anm_run.py from main 268a6b2d over the 8179068d-built kernel), same state and plan; NOT stopped after the first
# od line: the polish runs to its end or the cap (timeout -s TERM 7200, 2 h); gates gate903d.py and gate973.py on the log at the end.
P=/home/nathan/Source/choptuik-large-d-raw-1064w/I1064-dh170/discrim2_D262.0099
ROOT=/home/nathan/scratch949
WT=/home/nathan/Source/choptuik-large-d-1058b
PY=$WT/.venv/bin/python
S=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.0099.npz
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1 PATH=$WT/.venv/bin:$HOME/.local/bin:$HOME/.cargo/bin:$PATH VIRTUAL_ENV=$WT/.venv HP_DIR=$WT/hp
say() { echo "== $(date -u '+%F %T') UTC $*" >> $P/exits_discrim2.txt; }
N=discrim2_p6cmd_pob
[ -e $P/$N.log ] && { say "refuse: $N.log exists (no overwrite)"; exit 3; }
[ "$(git hash-object --no-filters $ROOT/$S | cut -c1-12)" = eb34f3c845a4 ] || { say "refuse: state blob is not eb34f3c845a4"; exit 2; }
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --corrector od --tol_od 1e-60 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 0 --proj_o 1 --reseed_qd_bar 1e-13"
# anm_run.py from the main checkout at 268a6b2d (as part 7), over the venv's kernel
WT2=/home/nathan/Source/choptuik-large-d-268a
export HP_DIR=$WT2/hp
cd $WT2/hp || exit 9
mkdir -p $P/$N
say "start $N: ks 293 keep_plan 1 from $S, load $(cut -d' ' -f1-3 /proc/loadavg)"
s0=$(date +%s)
nice -n 10 /usr/bin/time -v timeout -s TERM 7200 $PY -u anm_run.py $ROOT $P/$N --state $S $F --proj_o_bar 2e-34 --threads 4 --steps 0 --keep_plan 1 --save_base 1 --ks 293 > $P/$N.log 2>&1 &
tp=$!
while kill -0 $tp 2>/dev/null; do
  av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
  py=$(pgrep -P $(pgrep -P $tp | head -1) 2>/dev/null | head -1); rss=0
  [ -n "$py" ] && rss=$(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status 2>/dev/null)
  echo "$(date -u '+%T') $N MemAvailable $av MiB, anm_run pid ${py:-none} RSS ${rss:-0} MiB" >> $P/memlog_discrim2.log
  [ "$av" -lt 2048 ] && echo "ALERT $(date -u '+%T') $N MemAvailable $av MiB (alert only)" >> $P/alert_discrim2.log
  sleep 30
done
wait $tp; rc=$?
say "$N exit $rc, $(( $(date +%s) - s0 )) s wall"
say "$N gate903d: $($PY -I $P/gate903d.py $P/$N.log)"
say "$N gate973: $($PY -I $P/gate973.py $P/$N.log $P/$N)"
say "done"
