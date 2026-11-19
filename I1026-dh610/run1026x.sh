#!/bin/bash
# #1026 exploratory (not a reading; the verdicts of run1026.sh stand): the xi1 0.2 walks of minus, plus and newzero with the |r_3|, |r_5| bar at 1e-5 instead of 1e-6 (--bar), and the
# xi1 0.25 walk of minus rerun with the iteration cap at 80 instead of 25. Same code, flags and start values as run1026.sh. Output walks_explore/, logs_explore/.
. "$(dirname "$0")/common1026.sh"
EX=$RAW/exits_1026.txt
log() { echo "1026x $* $(stamp) UTC" >> $EX; }
cd $WT/solver/inner_stokes || exit 1
mkdir -p $RAW/walks_explore $RAW/logs_explore
log "start, load $(cut -d' ' -f1-3 /proc/loadavg)"
export W1026_PY=$PY W1026_WT=$WT
W="$PY -u $RAW/walk1026.py"
O="--out $RAW/walks_explore --logs $RAW/logs_explore --procs 2"
MINUS="2.59859992115029 0.22175721241675567 0.6931329470 0.0303267629"
PLUS="2.844769136217688 0.2179638045394524 0.7729710750 0.0207675674"
NEWZ="2.338793487291773 0.09623779643756343 0.8786980490 0.4250876107"
pids=()
nice -n 10 bash -c "$W minus $MINUS --xi1 0.2 --bar 1e-5 --maxit 40 $O > $RAW/logs_explore/walk_minus_xi0.2.log 2>&1" & pids+=($!)
nice -n 10 bash -c "$W plus $PLUS --xi1 0.2 --bar 1e-5 --maxit 40 $O > $RAW/logs_explore/walk_plus_xi0.2.log 2>&1" & pids+=($!)
nice -n 10 bash -c "$W newzero $NEWZ --xi1 0.2 --bar 1e-5 --maxit 40 $O > $RAW/logs_explore/walk_newzero_xi0.2.log 2>&1" & pids+=($!)
nice -n 10 bash -c "$W minus $MINUS --xi1 0.25 --maxit 80 $O > $RAW/logs_explore/walk_minus_xi0.25.log 2>&1" & pids+=($!)
for p in ${pids[@]}; do wait $p; log "walk pid $p exit $?"; done
bash -c "$PY $RAW/eval1026.py --dir $RAW/walks_explore > $RAW/logs_explore/eval_explore.log 2>&1"
log "all steps done"
