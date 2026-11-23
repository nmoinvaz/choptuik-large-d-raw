#!/bin/bash
# #1080 EXPLORATORY, third order of the coordinator: x1's start solve at xi1 0.2 with --floor_max=1e-3 (--verbose=2), once with INNER_NB_RTOL=1e-13 and once
# with 1e-11, side by side (2 procs each). The default integrator tolerance is rtol 1e-12, atol 1e-16 (inner_nb.py: integrate(..., rtol=1e-12, atol=1e-16), jumps(rtol=1e-12));
# INNER_NB_RTOL replaces rtol at every integrate call and leaves atol. The default's run is logs/start_x1_xi0.2_fm.log (same command, no override). Exits: exits_explore3.txt.
RAW=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3/m5/explore
WT=/Users/nathan/Source/choptuik-large-d
PY=/Users/nathan/Source/venv-macm3-i1080/bin/python
EX=$RAW/exits_explore3.txt
stamp() { date -u '+%F %T'; }
log() { echo "explore3 $* $(stamp) UTC" >> $EX; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_NUM_THREADS=1
cd $WT/solver/inner_stokes || exit 1
mkdir -p $RAW/logs
log "start, code $(git -C $WT rev-parse --short=8 HEAD) ($(git -C $WT status --porcelain --untracked-files=no | wc -l | tr -d ' ') tracked changes), load $(uptime | sed 's/.*load averages: //')"

# job RTOL: x1's start at xi1 0.2; a perl alarm ends a solve that runs past 30 min
job() {
  local rt=$1
  local a=$($PY $RAW/explore_report.py args x1)
  set -- $a
  local out=$RAW/logs/start_x1_xi0.2_fm_rtol$rt.log
  local cmd="$PY -u hier_nb.py 5 $1 $2 --x=$3,$4 --fixA --schur --procs 2 --verbose=2 --xi1=0.2 --floor_max=1e-3"
  echo "# cd $WT/solver/inner_stokes && INNER_NB_RTOL=$rt nice -n 10 $cmd" > $out
  log "command: INNER_NB_RTOL=$rt nice -n 10 $cmd"
  INNER_NB_RTOL=$rt nice -n 10 perl -e 'alarm 1800; exec @ARGV' $cmd >> $out 2>&1
}

job 1e-13 &
p1=$!
job 1e-11 &
p2=$!
wait $p1; log "rtol 1e-13 exit $?"
wait $p2; log "rtol 1e-11 exit $?"
if grep -l Traceback $RAW/logs/start_x1_xi0.2_fm_rtol*.log >> $EX 2>/dev/null; then log "Traceback in a log (files listed above)"; fi
log "all steps done"
