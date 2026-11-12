#!/usr/bin/env bash
# #562 main arm on win2, rule 2 (hp/held_homotopy.py at wip/i562-subagent 1161f49): a rung converges only when its
# correction is below tol AND its max|H| below 1e-6 h max|b|. Four jobs at 4 threads each, 6 h cap each.
# Before it: stop hh_real (if still running), hh_control07, hh_control07_neg and hh_planted_far of run_i562_main.sh
# (rule 1). Keep hh_planted and hh_planted_tsign running.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I562-win2
S=I562-win2/renode_0975_D242.3642.npz
J=I461-win2/crawlJ/anm_pin3_D242.3642.npz
RHO=$R/hh_real_setup.npz
export PYTHONFAULTHANDLER=1
cd /d/choptuik-i562-r2/hp || exit 9
log() { echo "$1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_rule2.txt; }
run() {
  local n=$1; shift
  log "$n start"
  ( "$PY" -u held_homotopy.py "$@" --rule 2 --threads 4 --hours 6 > $R/$n.log 2>&1; log "$n exit $?" ) &
}
run hh2_planted      $RAW $S $R/hh2_planted      --mode planted --eps 2.5e-17
run hh2_real         $RAW $S $R/hh2_real         --mode real
run hh2_control07    $RAW $J $R/hh2_control07    --mode control --rho $RHO --ladder 0:90:2
run hh2_control07_neg $RAW $J $R/hh2_control07_neg --mode control --rho $RHO --rho_scale -1 --ladder 0:90:2
wait
log "run_i562_rule2 done"
