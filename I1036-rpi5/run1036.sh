#!/bin/bash
# #1036: the commands of notes/L2_MODE.md section 10, in order, one at a time at nice 10 (from solver/inner_pert/ of the worktree)
RAW=$(cd "$(dirname "$0")" && pwd); PY=$HOME/Source/venv-choptuik/bin/python
cd $HOME/Source/cl-1036/solver/inner_pert || exit 9
echo "$(date -u '+%F %T UTC') driver start, main $(git rev-parse --short HEAD)" >> $RAW/logs/driver.log
run() {  # NAME ARGS...
  name=$1; shift; t0=$(date +%s)
  nice -n 10 $PY -u "$@" > $RAW/logs/$name.log 2>&1; rc=$?
  echo "exit $rc" >> $RAW/logs/$name.log
  echo "$name $((`date +%s` - t0)) s exit $rc" >> $RAW/logs/times.txt
  echo "$(date -u '+%F %T UTC') $name exit $rc" >> $RAW/logs/driver.log
}
run l2_mode_flat l2_mode.py --flat
run l2_mode_check l2_mode.py --check
run l2_mode_check_curv l2_mode.py --check --mutate=curv
run l2_mode_first_order l2_mode.py --first-order
run l2_mode_first_order_print l2_mode.py --first-order --print
run l2_c2_forcing l2_c2_forcing.py
run l2_c2_forcing_p1 l2_c2_forcing.py --p1
run l2_c2_checks_main l2_c2.py --checks
run l2_c2_checks_ident l2_c2.py --checks --mutate=ident
run l2_c2_checks_series l2_c2.py --checks --mutate=series
run l2_c2_checks_force l2_c2.py --checks --mutate=force
run l2_c2_M1_planted l2_c2.py 1 --planted-lam
for M in 1 3 5; do run l2_c2_M$M l2_c2.py $M --forcing=l2,l2_ctrl,l0,sym --lamcheck; done
for M in 1 3 5; do run l2_c2_M${M}_G l2_c2.py $M --forcing=l2,l0,G,sym --lamcheck; done
run l2_c2_M5_mutate_gsign l2_c2.py 5 --forcing=l0,sym --mutate=gsign
run l2_c2_summary l2_c2_summary.py
echo "$(date -u '+%F %T UTC') driver done" >> $RAW/logs/driver.log
