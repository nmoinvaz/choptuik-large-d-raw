#!/bin/bash
# #1026 (dh610): do the three radius-stable M = 3 zeros of #1020 persist at M = 5? Control first: the known zero's M = 5 solve from its M = 3 zero must reproduce the stored zero (A 2.718579189, w/w_inf 0.999228404, inputs/hier_M5_full_schur.log).
# Route: walk1026.py (the outer Newton over complete fixed-(A, w) solves of hier_nb.py 5 --fixA --schur), because hier_nb.py 5's own level-1 Newton stops without a step from the M = 3 zero (logs/probe_*). Same code as run1020.sh (cl-995 fc7dee4d).
# Stages: 0 the M = 3 harmonics at the four zeros (f3probe1026.py); 1 the control at xi1 0.2 and its gate (eval1026.py exits 0); 2 the three candidates at xi1 0.2, side by side (2 procs each); 3 all four at xi1 0.25, side by side.
. "$(dirname "$0")/common1026.sh"
EX=$RAW/exits_1026.txt
log() { echo "1026 $* $(stamp) UTC" >> $EX; }
cd $WT/solver/inner_stokes || exit 1
mkdir -p $RAW/walks $RAW/logs
log "start, code $(git -C $WT rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)"
try() { local name=$1 want=$2; shift 2; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc (expected $want) wall $(( $(date +%s) - s )) s"; return $rc; }
step() { try "$@" || { log "stopped at $1"; exit 1; }; }
W="$PY -u $RAW/walk1026.py"
export W1026_PY=$PY W1026_WT=$WT
# M = 3 harmonics (-2 Im F_3, 2 Re F_3) at the zeros, from step 0's probe (the tuned values at xi1 0.2 and 0.25 agree to 1e-9)
CTRL="2.726475885672135 1.0156030949093042 0.1444194785 0.0110874259"
MINUS="2.59859992115029 0.22175721241675567 0.6931329470 0.0303267629"
PLUS="2.844769136217688 0.2179638045394524 0.7729710750 0.0207675674"
NEWZ="2.338793487291773 0.09623779643756343 0.8786980490 0.4250876107"
step f3probe 0 bash -c "nice -n 10 $PY -u $RAW/f3probe1026.py > $RAW/logs/f3probe.log 2>&1"
step control_xi0.2 0 bash -c "nice -n 10 $W control $CTRL --xi1 0.2 --procs 2 --maxit 25 > $RAW/logs/walk_control_xi0.2.log 2>&1"
step gate_control 0 bash -c "$PY $RAW/eval1026.py > $RAW/logs/eval_control.log 2>&1"
pids=()
for n in minus plus newzero; do
  v=$(echo $n | tr a-z A-Z); [ $n = newzero ] && v=NEWZ; a=${!v}
  nice -n 10 bash -c "$W $n $a --xi1 0.2 --procs 2 --maxit 25 > $RAW/logs/walk_${n}_xi0.2.log 2>&1" &
  pids+=($!)
done
for p in ${pids[@]}; do wait $p; log "walk pid $p exit $?"; done
pids=()
for n in control minus plus newzero; do
  v=$(echo $n | tr a-z A-Z); [ $n = newzero ] && v=NEWZ; [ $n = control ] && v=CTRL; a=${!v}
  nice -n 10 bash -c "$W $n $a --xi1 0.25 --procs 2 --maxit 25 > $RAW/logs/walk_${n}_xi0.25.log 2>&1" &
  pids+=($!)
done
for p in ${pids[@]}; do wait $p; log "walk pid $p exit $?"; done
try eval 0 bash -c "$PY $RAW/eval1026.py > $RAW/logs/eval_all.log 2>&1"
log "all steps done"
