#!/usr/bin/env bash
# #562 main arm on win2: the held-offset homotopy (hp/held_homotopy.py), six jobs at 3 threads each, 6 h cap each.
# Needs the code at wip/i562-subagent 6dcadb8 (or later) and the raw clone pulled to at least 3d4615b0 (I562-mac/probe_real_setup.npz).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I562-win2
S=I562-win2/renode_0975_D242.3642.npz
J=I461-win2/crawlJ/anm_pin3_D242.3642.npz
RHO=$RAW/I562-mac/probe_real_setup.npz
export PYTHONFAULTHANDLER=1
cd /d/choptuik-i562/hp || exit 9
[ -f $RHO ] || { echo "pull the raw clone first ($RHO)" >&2; exit 9; }
log() { echo "$1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_main.txt; }
run() {   # name, then the arguments
  local n=$1; shift
  log "$n start"
  ( "$PY" -u held_homotopy.py "$@" --threads 3 --hours 6 > $R/$n.log 2>&1; log "$n exit $?" ) &
}
# planted (pass: exit 0) and its control tsign (must not exit 0)
run hh_planted        $RAW $S $R/hh_planted        --mode planted --eps 2.5e-17
run hh_planted_tsign  $RAW $S $R/hh_planted_tsign  --mode planted --eps 2.5e-17 --mutate tsign
# the real trace (exit 0: reached t = 1; exit 3: stopped, at a fold or a limit)
run hh_real           $RAW $S $R/hh_real           --mode real
# the 0.7 control: crawlJ's state, its target moved by -rho (as the real one) and by +rho (toward the exact projector)
run hh_control07      $RAW $J $R/hh_control07      --mode control --rho $RHO --ladder 0:90:2
run hh_control07_neg  $RAW $J $R/hh_control07_neg  --mode control --rho $RHO --rho_scale -1 --ladder 0:90:2
# planted beyond the one-mode fold (eps 2.5e-16): a demonstration of the stop rule, no pass rule
run hh_planted_far    $RAW $S $R/hh_planted_far    --mode planted --eps 2.5e-16
wait
log "run_i562_main done"
