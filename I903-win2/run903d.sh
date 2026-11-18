#!/usr/bin/env bash
# #903 ks ladder (coordinator's hc, 2026-11-18 ~05:25 UTC). Glue that chains the coordinator's commands and logs each exit in exits_903.txt (903d lines):
#  1. wait for the end of leg 8's current attempt (at most 1 h), then kill only that leg's anm_run python tree; ks_chain.py stops itself on the non-zero exit.
#  2. base polishes at the leg's last accepted state, each rung from the one before: anm_run.py with run_ks_chain.sh's flags (--steps 0) plus --ks K
#     --keep_plan 0 --save_base 1, K = 260, 270, 280, out I903-win2/ks_chain/ladder8/ks<K>, capped at 3 h each. A rung that exits non-zero, is capped, saves
#     no base or whose first octo-double Newton line is not converged at max|F| <= 1e-60 (gate903d.py) stops the ladder.
#  3. ks_chain.py --pad 30 from the last base, OUT I903-win2/ks_chain2 (a new OUT, since ks_chain resumes from the highest-D state of its own OUT), after a --dry
#     check that the first leg's ks is not above the last rung's.
# Worktree D:/choptuik-i603r at 3b60968f (its anm_run.py and ks_chain.py), venv-i600, 9 threads as run_ks_chain.sh. usage: bash run903d.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; RAWW=D:/choptuik-large-d-raw
R=$RAW/I903-win2
LEG=$R/ks_chain/leg08_D232.0000_ks250
W=/d/choptuik-i603r/hp
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
export PYTHONFAULTHANDLER=1
log() { echo "903d $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_903.txt; }
cnt() { local n; n=$(grep -cE "$1" "$2" 2>/dev/null); echo ${n:-0}; }
killtree() { local pid; pid=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '$1' } | Sort-Object ProcessId | Select-Object -First 1).ProcessId"); [ -n "$pid" ] && MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $pid > /dev/null 2>&1; echo "${pid:-none}"; }

# 1. stop after the current attempt
ex0=$(cnt '^903c ks_chain exit' $R/exits_903.txt)
a0=$(cnt '^ +a [0-9.]+ -> D' $LEG/anm_run.log); v0=$(cnt 'Delta of the saved state' $LEG/anm_run.log)
log "stop of ks_chain: waiting for the end of leg 8's current attempt (a-lines $a0), at most 1 h"
t0=$(date +%s); why="an attempt ended"
until [ "$(cnt '^ +a [0-9.]+ -> D' $LEG/anm_run.log)" -gt "$a0" ]; do
  [ $(( $(date +%s) - t0 )) -ge 3600 ] && { why="1 h without an attempt end"; break; }
  sleep 3
done
t1=$(date +%s)   # an accepted attempt's state is on disk just before the line 'Delta of the saved state'
while [ "$(cnt 'Delta of the saved state' $LEG/anm_run.log)" -le "$v0" ] && [ $(( $(date +%s) - t1 )) -lt 45 ]; do sleep 2; done
pid=$(killtree '*leg08_D232.0000_ks250*')
log "stop of ks_chain: leg 8's python tree killed (pid $pid) after $why"
t1=$(date +%s)
until [ "$(cnt '^903c ks_chain exit' $R/exits_903.txt)" -gt "$ex0" ]; do
  [ $(( $(date +%s) - t1 )) -ge 300 ] && { log "ks_chain did not exit within 5 min of the kill; ladder not started"; exit 1; }
  sleep 3
done
S0=$("$PY" -I -c "import glob,os,re; b=max((float(m.group(1)),p) for p in glob.glob('$RAWW/I903-win2/ks_chain/leg08_D232.0000_ks250/anm_pin*_D*.npz') for m in [re.search(r'anm_pin\d+_D(\d+\.\d+)\.npz\$', os.path.basename(p))] if m); print(os.path.relpath(b[1], '$RAWW').replace(os.sep, '/'))")
log "ks_chain stopped, leg 8's last accepted state $S0"

# 2. the ladder
prev=$S0
for K in 260 270 280; do
  out=$R/ks_chain/ladder8/ks$K; mkdir -p $out
  log "rung ks $K start from $prev"
  t=$(date +%s)
  ( cd $W && "$PY" -u anm_run.py $RAW $out --state $prev $F --steps 0 --ks $K --keep_plan 0 --save_base 1 ) >> $out/anm_run.log 2>&1 &
  bp=$!; capped=0
  while kill -0 $bp 2>/dev/null; do
    [ $(( $(date +%s) - t )) -ge 10800 ] && { capped=1; killtree "*ladder8*ks$K*" > /dev/null; break; }
    sleep 10
  done
  wait $bp; rc=$?
  base=$(ls $out/base_pin*_D*.npz 2>/dev/null | head -1)
  gate=$("$PY" -I $RAWW/I903-win2/gate903d.py $RAWW/I903-win2/ks_chain/ladder8/ks$K/anm_run.log)
  log "rung ks $K exit $rc wall $(( $(date +%s) - t ))s capped $capped base ${base:-none} gate: $gate"
  case "$gate" in OK*) ;; *) log "ladder STOPPED at ks $K (gate)"; exit 1;; esac
  { [ $capped -eq 0 ] && [ $rc -eq 0 ] && [ -n "$base" ]; } || { log "ladder STOPPED at ks $K (exit, cap or no base)"; exit 1; }
  prev=${base#$RAW/}
done

# 3. the chain from the last base
dry=$(cd $W && "$PY" -u ks_chain.py $RAW $R/ks_chain2 --state $prev --D_stop 400 --pad 30 --dry -- $F --steps 400 2>&1 | grep -m1 '^leg 0:')
K1=$(echo "$dry" | sed -n 's/.* at ks \([0-9]*\) from.*/\1/p')
log "dry run of the resume: $dry"
{ [ -n "$K1" ] && [ "$K1" -le 280 ]; } || { log "resume NOT started: the first leg's ks '$K1' is unreadable or above the last rung 280"; exit 1; }
log "ks_chain resume start from $prev, --pad 30, OUT I903-win2/ks_chain2, main $(git -C /d/choptuik-i603r rev-parse --short=8 HEAD)"
t=$(date +%s)
( cd $W && "$PY" -u ks_chain.py $RAW $R/ks_chain2 --state $prev --D_stop 400 --pad 30 -- $F --steps 400 ) >> $R/ks_chain2.log 2>&1
log "ks_chain2 exit $? wall $(( $(date +%s) - t ))s"
