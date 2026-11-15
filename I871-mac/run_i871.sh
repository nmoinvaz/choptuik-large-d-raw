#!/bin/bash
# Every run of I871-mac, from solver/proof/ of the checkout (branch wip/sa-871).
# Usage: run_i871.sh <python> <root of the raw-data clone>. Each line of exits.txt has the run, its exit status, the
# status it must have, its wall time and its command.
PY=$1; ROOT=$2
RAW=$ROOT/I871-mac
: > $RAW/exits.txt
run() {   # run <log name> <expected exit> <command...>
  local log=$1 want=$2; shift 2
  local t0=$(date +%s)
  nice -n 10 "$@" > $RAW/$log.log 2>&1
  local rc=$?
  echo "$log: exit $rc (must be $want), $(( $(date +%s) - t0 )) s: $*" | sed "s|$PY|python3|; s|$ROOT|RAW|g" >> $RAW/exits.txt
}
run sets_M5 0 $PY theorem_A_sets_M.py --M=5 --raw=$ROOT
for m in decimal centre kbox; do run sets_M5_mut_$m 1 $PY theorem_A_sets_M.py --M=5 --raw=$ROOT --mutate=$m; done
run selftest_M5 0 $PY theorem_A_sets_M.py --M=5 --raw=$ROOT --selftest
run sets_M3 0 $PY theorem_A_sets_M.py --M=3
run sets_M3_mut_centre 1 $PY theorem_A_sets_M.py --M=3 --mutate=centre
run selftest_M3 0 $PY theorem_A_sets_M.py --M=3 --selftest
