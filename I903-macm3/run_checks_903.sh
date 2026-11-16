#!/bin/bash
# macm3b: the new-machine bit-identity checks of AGENTS.md, with the venv-macm3-main build, from hp/ of the 1f3cda09 worktree
RAW=$HOME/Source/choptuik-large-d-raw-903
R=$RAW/I903-macm3
PY=$HOME/Source/venv-macm3-main/bin/python
cd $HOME/Source/choptuik-large-d-903/hp
run() {
  name=$1; shift
  echo "903 $name start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/checks_times.txt
  caffeinate -is nice -n 10 $PY -u highm_check.py "$@" > $R/$name.log 2>&1
  rc=$?
  echo "exit $rc" >> $R/$name.log
  echo "903 $name exit $rc $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/checks_times.txt
}
run ref_compare ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80
run scaled_compare scaled --compare=$RAW/T81/scaled_main.json
run jets_compare jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json
run jets_mutate_kappa jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa
echo "903 run_checks_903.sh done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/checks_times.txt
