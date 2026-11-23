#!/bin/bash
# #1080 EXPLORATORY (the coordinator's order after the result): start solves only, no walks. Each is the first solve of walk1026.py,
#   hier_nb.py 5 A w --x=B3,C3 --fixA --schur --procs 2 --verbose=V --xi1=XI
# Batch 1: x1, x2 and the control at xi1 0.15 (2 procs each, 6 threads). Batch 2: the same at 0.17. Batch 3: x1 at xi1 0.2 with --verbose=2.
# Started detached under caffeinate -is and nice -n 10 (../launch.py). Exits go to exits_explore.txt.
RAW=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3/m5/explore
WT=/Users/nathan/Source/choptuik-large-d
PY=/Users/nathan/Source/venv-macm3-i1080/bin/python
EX=$RAW/exits_explore.txt
stamp() { date -u '+%F %T'; }
log() { echo "explore $* $(stamp) UTC" >> $EX; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_NUM_THREADS=1
cd $WT/solver/inner_stokes || exit 1
mkdir -p $RAW/logs
log "start, code $(git -C $WT rev-parse --short=8 HEAD) ($(git -C $WT status --porcelain --untracked-files=no | wc -l | tr -d ' ') tracked changes), load $(uptime | sed 's/.*load averages: //')"
$PY $RAW/explore_report.py selftest > $RAW/logs/selftest_explore.log 2>&1 || { log "STOP: explore_report.py selftest"; exit 1; }

# job NAME XI VERBOSE TAG: one start solve; a perl alarm ends a solve that runs past 30 min
job() {
  local name=$1 xi=$2 v=$3 tag=$4
  local a=$($PY $RAW/explore_report.py args $name)
  set -- $a
  local out=$RAW/logs/start_${name}_xi${xi}${tag}.log
  local cmd="$PY -u hier_nb.py 5 $1 $2 --x=$3,$4 --fixA --schur --procs 2 --verbose=$v --xi1=$xi"
  echo "# cd $WT/solver/inner_stokes && nice -n 10 $cmd" > $out
  log "command: nice -n 10 $cmd"
  nice -n 10 perl -e 'alarm 1800; exec @ARGV' $cmd >> $out 2>&1
}

batch() { # XI: x1, x2, control side by side
  job x1 $1 1 "" &
  p1=$!
  job x2 $1 1 "" &
  p2=$!
  job control $1 1 "" &
  p3=$!
  wait $p1; log "x1 xi$1 exit $?"
  wait $p2; log "x2 xi$1 exit $?"
  wait $p3; log "control xi$1 exit $?"
}
batch 0.15
batch 0.17
job x1 0.2 2 _v2
log "x1 xi0.2 verbose2 exit $?"
if grep -l Traceback $RAW/logs/start_*.log >> $EX 2>/dev/null; then log "Traceback in a log (files listed above)"; fi
$PY $RAW/explore_report.py report > $RAW/logs/report.md 2>&1
log "report exit $?"
log "all steps done"
