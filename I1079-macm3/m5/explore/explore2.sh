#!/bin/bash
# #1080 EXPLORATORY, second order of the coordinator: two probes on x1's start solve at xi1 0.2 and 0.17, no walks.
#   hier_nb.py 5 A w --x=B3,C3 --fixA --schur --procs 2 --verbose=V --xi1=XI [--floor_max=1e-3]
# Batch 1: xi1 0.2, (--floor_max=1e-3 --verbose=2) beside (--verbose=3). Batch 2: the same at 0.17.
# The floor_max probes run at --verbose=2 so that the stop reasons print (the verbose level changes no number). Exits go to exits_explore2.txt.
RAW=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3/m5/explore
WT=/Users/nathan/Source/choptuik-large-d
PY=/Users/nathan/Source/venv-macm3-i1080/bin/python
EX=$RAW/exits_explore2.txt
stamp() { date -u '+%F %T'; }
log() { echo "explore2 $* $(stamp) UTC" >> $EX; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_NUM_THREADS=1
cd $WT/solver/inner_stokes || exit 1
mkdir -p $RAW/logs
log "start, code $(git -C $WT rev-parse --short=8 HEAD) ($(git -C $WT status --porcelain --untracked-files=no | wc -l | tr -d ' ') tracked changes), load $(uptime | sed 's/.*load averages: //')"

# job XI VERBOSE TAG EXTRA...: x1's start solve; a perl alarm ends a solve that runs past 30 min
job() {
  local xi=$1 v=$2 tag=$3
  shift 3
  local a=$($PY $RAW/explore_report.py args x1)
  set -- $a "$@"
  local out=$RAW/logs/start_x1_xi${xi}${tag}.log
  local cmd="$PY -u hier_nb.py 5 $1 $2 --x=$3,$4 --fixA --schur --procs 2 --verbose=$v --xi1=$xi ${@:5}"
  echo "# cd $WT/solver/inner_stokes && nice -n 10 $cmd" > $out
  log "command: nice -n 10 $cmd"
  nice -n 10 perl -e 'alarm 1800; exec @ARGV' $cmd >> $out 2>&1
}

for xi in 0.2 0.17
do
  job $xi 2 _fm --floor_max=1e-3 &
  p1=$!
  job $xi 3 _v3 &
  p2=$!
  wait $p1; log "x1 xi$xi floor_max exit $?"
  wait $p2; log "x1 xi$xi verbose3 exit $?"
done
if grep -l Traceback $RAW/logs/start_x1_xi*_fm.log $RAW/logs/start_x1_xi*_v3.log >> $EX 2>/dev/null; then log "Traceback in a log (files listed above)"; fi
log "all steps done"
