#!/bin/bash
# #1030: route 3's certificates on rpi5, one process at a time at nice 10 (commands of notes/P6_route3.md 10.6 and 11.6)
RAW=$(cd "$(dirname "$0")" && pwd); PY=$HOME/Source/venv-choptuik/bin/python
cd $HOME/Source/choptuik-large-d-964/solver/proof || exit 9
echo "$(date -u '+%F %T UTC') driver start, main $(git rev-parse --short HEAD)" >> $RAW/logs/driver.log
run() {  # NAME ARGS...
  name=$1; shift; t0=$(date +%s)
  nice -n 10 $PY -u "$@" > $RAW/logs/$name.log 2>&1; rc=$?
  echo "exit $rc" >> $RAW/logs/$name.log
  echo "$name $((`date +%s` - t0)) s exit $rc" >> $RAW/logs/times.txt
  echo "$(date -u '+%F %T UTC') $name exit $rc" >> $RAW/logs/driver.log
}
run route3_bound_lemmas route3_bound.py --lemmas
run route3_bound_constants route3_bound.py --constants
run route3_bound_constants_J0100 route3_bound.py --constants --J0=100
run route3_bound_check route3_bound.py --check
run route3_bound_check_plant route3_bound.py --check --mutate=plant
run route3_bound_check_psi route3_bound.py --check --mutate=psi
run route3_tuned_7_800 route3_tuned.py 7 800
run route3_tuned_7_800_demix route3_tuned.py 7 800 --mutate=demix
run route3_head_scope route3_head.py --scope
run route3_head_lemmas route3_head.py --lemmas
run route3_head_check route3_head.py --check
run route3_head_check_plant route3_head.py --check --mutate=plant
run route3_head_check_gsmall route3_head.py --check --mutate=gsmall
run route3_head_certify route3_head.py --certify
echo "$(date -u '+%F %T UTC') driver done" >> $RAW/logs/driver.log
