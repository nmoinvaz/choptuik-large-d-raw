#!/bin/bash
# Every run of I866-mac, from solver/proof/ of the checkout (branch wip/sa-866).
# Usage: run_i866.sh <python> <this folder>. Each line of exits.txt has the run, its exit status, the status it must
# have, its wall time and its command.
PY=$1; RAW=$2
: > $RAW/exits.txt
run() {   # run <log name> <expected exit> <command...>
  local log=$1 want=$2; shift 2
  local t0=$(date +%s)
  nice -n 10 "$@" > $RAW/$log.log 2>&1
  local rc=$?
  echo "$log: exit $rc (must be $want), $(( $(date +%s) - t0 )) s: $*" | sed "s|$PY|python3|" >> $RAW/exits.txt
}
M3=data/A_M_box_M3_1e-10.json
M5=data/A_M2_box_M5_1e-10.json
run cert_M3 0 $PY fixed_point_M_b_check.py cert --box=$M3
run cert_M3_mut_sign 3 $PY fixed_point_M_b_check.py cert --box=$M3 --mutate=sign
run cert_M3_mut_radius 3 $PY fixed_point_M_b_check.py cert --box=$M3 --mutate=radius
run cert_M5 0 $PY fixed_point_M_b_check.py cert --box=$M5 --second
run cert_M5_mut_sign 3 $PY fixed_point_M_b_check.py cert --box=$M5 --mutate=sign
run cert_M5_mut_radius 3 $PY fixed_point_M_b_check.py cert --box=$M5 --mutate=radius
