#!/usr/bin/env bash
# #595: held_homotopy rule 2 on cadcaf1 (exact projector): planted control at D 235.13, then the real traces at
# D 235.13 and D 240.03; one job at a time, 4 threads, nice 10, 1.5 h cap each
PY=/Users/nathan/venv-314/bin/python
RAW=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i562
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i562/c2pkgs
R=$RAW/I595-mac
mkdir -p $R
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a671334124392504b/hp || exit 9
log() { echo "$1 $(date -u '+%Y-%m-%d %H:%M:%S UTC') $(git rev-parse --short HEAD)" >> $R/exits.txt; }
run() {
  local n=$1; shift
  $PY -c "import hpkernel; print('hpkernel', hpkernel.__file__)" > $R/$n.log
  log "$n start"
  nice -n 10 $PY -u held_homotopy.py "$@" --rule 2 --threads 4 --hours 1.5 --ladder 0:90:2 >> $R/$n.log 2>&1
  log "$n exit $?"
}
run plantedrho235 $RAW I589-mac/s235.npz $R/plantedrho235 --mode control --rho $RAW/I589-mac/c2_probe_s235_setup.npz --rho_scale 1e-18 --h_max 1
run real235    $RAW I589-mac/s235.npz $R/real235    --mode real
run real240    $RAW I589-mac/s240.npz $R/real240    --mode real
