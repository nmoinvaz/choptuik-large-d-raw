#!/bin/bash
# Every run of I870-mac, from solver/proof/ of the checkout (branch wip/sa-870, main ecfc1b92).
# Usage: run_i870.sh <python> <this folder> <h: 1e-9 or 1e-11>. Each line of exits.txt has the run, its exit status,
# the status it must have, its wall time and its command.
PY=$1; RAW=$2; H=$3
run() {   # run <log name> <expected exit> <command...>
  local log=$1 want=$2; shift 2
  local t0=$(date +%s)
  nice -n 10 "$@" > $RAW/$log.log 2>&1
  local rc=$?
  echo "$log: exit $rc (must be $want), $(( $(date +%s) - t0 )) s: $*" | sed "s|$PY|python3|" >> $RAW/exits.txt
}
B=data/A_M2_box_M5_$H.json
run cert_M5_$H 0 $PY fixed_point_M_b_check.py cert --box=$B --second
run cert_M5_${H}_mut_sign 3 $PY fixed_point_M_b_check.py cert --box=$B --mutate=sign
run cert_M5_${H}_mut_radius 3 $PY fixed_point_M_b_check.py cert --box=$B --mutate=radius
