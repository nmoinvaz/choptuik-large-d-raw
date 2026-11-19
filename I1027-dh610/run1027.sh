#!/bin/bash
# #1027 (dh610): M = 7 at the two low-omega M = 5 zeros of #1026, by walk1027.py (#1026's outer Newton over complete fixed-(A, w) solves, here of hier_nb.py 7 with the M = 7 flags of proof/B_tail_M7.md).
# Control first: the known zero from its M = 5 zero (F_7 = 0) must reproduce (2.71924, 1.000025) (eval1027.py exits 0). Then z2275 and z2584 at xi1 0.15 (the control's radius), then both at xi1 0.2 and 0.25 as exploration.
. "$(dirname "$0")/common1027.sh"
EX=$RAW/exits_1027.txt
log() { echo "1027 $* $(stamp) UTC" >> $EX; }
cd $WT/solver/inner_stokes || exit 1
mkdir -p $RAW/walks $RAW/logs
log "start, code $(git -C $WT rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)"
try() { local name=$1 want=$2; shift 2; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc (expected $want) wall $(( $(date +%s) - s )) s"; return $rc; }
step() { try "$@" || { log "stopped at $1"; exit 1; }; }
export W1027_PY=$PY W1027_WT=$WT
W="$PY -u $RAW/walk1027.py"
CTRL="2.718579189229888 0.9992284031945021 0.1492035749173264 0.01471905249087869 0.008405346906375517 0.0014703451817031647"
Z2275="2.227529226538137 0.09257370253498763 0.727370 0.006983 0.398120 0.038676"
Z2584="2.5838875556175958 0.14135765185307603 0.82177 0.006896 0.40790 0.033645"
step control_xi0.15 0 bash -c "nice -n 10 $W control $CTRL --xi1 0.15 --procs 2 > $RAW/logs/walk_control_xi0.15.log 2>&1"
step gate_control 0 bash -c "$PY $RAW/eval1027.py > $RAW/logs/eval_control.log 2>&1"
pids=()
for n in z2275 z2584; do
  v=$(echo $n | tr a-z A-Z)
  nice -n 10 bash -c "$W $n ${!v} --xi1 0.15 --procs 2 > $RAW/logs/walk_${n}_xi0.15.log 2>&1" &
  pids+=($!)
done
for p in ${pids[@]}; do wait $p; log "walk pid $p exit $?"; done
pids=()
for xi in 0.2 0.25; do for n in z2275 z2584; do
  v=$(echo $n | tr a-z A-Z)
  nice -n 10 bash -c "$W $n ${!v} --xi1 $xi --procs 2 > $RAW/logs/walk_${n}_xi$xi.log 2>&1" &
  pids+=($!)
done; done
for p in ${pids[@]}; do wait $p; log "walk pid $p exit $?"; done
try eval 0 bash -c "$PY $RAW/eval1027.py > $RAW/logs/eval_all.log 2>&1"
log "all steps done"
