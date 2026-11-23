#!/bin/bash
# #1080 EXPLORATORY, the coordinator's order after raw 83d797ad: x2's float64 start solve at xi1 0.2 with --floor_max=1e-3, as x1's (explore2.sh).
#   hier_nb.py 5 A w --x=B3,C3 --fixA --schur --procs 2 --verbose=2 --xi1=0.2 --floor_max=1e-3
# No value_mp, no walk. Exits go to exits_explore4.txt.
RAW=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3/m5/explore
WT=/Users/nathan/Source/choptuik-large-d
PY=/Users/nathan/Source/venv-macm3-i1080/bin/python
EX=$RAW/exits_explore4.txt
stamp() { date -u '+%F %T'; }
log() { echo "explore4 $* $(stamp) UTC" >> $EX; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_NUM_THREADS=1
cd $WT/solver/inner_stokes || exit 1
log "start, code $(git -C $WT rev-parse --short=8 HEAD) ($(git -C $WT status --porcelain --untracked-files=no | wc -l | tr -d ' ') tracked changes), load $(uptime | sed 's/.*load averages: //')"
read -r A W B3 C3 <<< "$($PY $RAW/explore_report.py args x2)"
out=$RAW/logs/start_x2_xi0.2_fm.log
cmd="$PY -u hier_nb.py 5 $A $W --x=$B3,$C3 --fixA --schur --procs 2 --verbose=2 --xi1=0.2 --floor_max=1e-3"
echo "# cd $WT/solver/inner_stokes && nice -n 10 $cmd" > $out
log "command: nice -n 10 $cmd"
nice -n 10 perl -e 'alarm 1800; exec @ARGV' $cmd >> $out 2>&1
log "x2 xi0.2 floor_max exit $?"
if grep -q Traceback $out; then log "Traceback in $out"; fi
log "all steps done"
