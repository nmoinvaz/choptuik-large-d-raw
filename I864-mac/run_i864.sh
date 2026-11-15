#!/bin/bash
# Every run of I864-mac, from solver/proof/ of the checkout (branch wip/sa-864).
# Usage: run_i864.sh <python> <root of the raw-data clone>. Each line of exits.txt has the run, its exit status, the
# status it must have, its wall time and its command.
PY=$1; ROOT=$2
RAW=$ROOT/I864-mac
: > $RAW/exits.txt
run() {   # run <log name> <expected exit> <command...>
  local log=$1 want=$2; shift 2
  local t0=$(date +%s)
  nice -n 10 "$@" > $RAW/$log.log 2>&1
  local rc=$?
  echo "$log: exit $rc (must be $want), $(( $(date +%s) - t0 )) s: $*" | sed "s|$PY|python3|; s|$ROOT|RAW|g" >> $RAW/exits.txt
}
for M in 3 5; do
  run cover_M$M 0 $PY start_cover_lemmas_M.py --M=$M --raw=$ROOT --rerun
  run cover_M${M}_edge0 0 $PY start_cover_lemmas_M.py --M=$M --raw=$ROOT --mutate=edge0
  for m in widen edge centre g0 rho0; do run cover_M${M}_mut_$m 1 $PY start_cover_lemmas_M.py --M=$M --raw=$ROOT --mutate=$m; done
  run selftest_M$M 0 $PY start_cover_lemmas_M.py --M=$M --raw=$ROOT --selftest
done
