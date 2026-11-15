#!/bin/bash
# Every run of I869-mac, from solver/proof/ of the checkout (branch wip/sa-869).
# Usage: run_i869.sh <python> <this folder> <run> ...; runs: clean, w0, sign, and with a box suffix clean:1e-9 etc.
# Each line of exits.txt has the run, its exit status, the status it must have, its wall time and its command.
PY=$1; RAW=$2; shift 2
run() {   # run <log name> <expected exit> <command...>
  local log=$1 want=$2; shift 2
  local t0=$(date +%s)
  nice -n 10 "$@" > $RAW/$log.log 2>&1
  local rc=$?
  echo "$log: exit $rc (must be $want), $(( $(date +%s) - t0 )) s: $*" | sed "s|$PY|python3|" >> $RAW/exits.txt
}
for r in "$@"; do
  kind=${r%%:*}; h=1e-10; [[ $r == *:* ]] && h=${r##*:}
  B=data/A_M2_box_M5_$h.json
  if [ $kind = clean ]; then run cert2_M5_$h 0 $PY fixed_point_M_b_check.py cert2 --box=$B
  else run cert2_M5_${h}_mut_$kind 3 $PY fixed_point_M_b_check.py cert2 --box=$B --mutate=$kind; fi
done
