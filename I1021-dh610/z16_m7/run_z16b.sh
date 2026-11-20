#!/bin/bash
# #1021 step (dh610): box 16's zero at M = 7 by #1027's protocol and rule, at xi1 0.25 and 0.2, with the known zero's control
# (see README.md). One walk at a time, 2 processes (--procs 2), nice 10; a walk's own cap by timeout on its exact pid.
#   run_z16b.sh (second driver, started after the 0.25 control failed): the 0.2 radius only (Z16_XIS="0.25 0.2" restores both)
. "$(dirname "$0")/common_z16.sh"
EX=$D/exits_z16.txt
log() { echo "z16 $* $(stamp) UTC" >> $EX; }
cd $WT/solver/inner_stokes || exit 1
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = fc7dee4d ] || { echo "cl-995 is not at fc7dee4d"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { echo "cl-995 not clean"; exit 1; }
log "start (run_z16b.sh, radii ${Z16_XIS:-0.2}), code $(git -C $WT rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)"
w26="$PY -u $D/walk1026.py"; w27="$PY -u $D/walk1027.py"
try() { local name=$1 want=$2 cap=$3; shift 3; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc (expected $want) wall $(( $(date +%s) - s )) s, cap $cap s"; return $rc; }
$PY $D/eval_z16.py --selftest > $D/logs/eval_selftest.log 2>&1; log "eval_z16 selftest exit $? (0)"
$PY $D/eval_z16.py --selftest --break > $D/logs/eval_selftest_break.log 2>&1; log "eval_z16 selftest --break exit $? (1)"
CTRL="2.718579189229888 0.9992284031945021 0.1492035749173264 0.01471905249087869 0.008405346906375517 0.0014703451817031647"
read -r IA IW IB3 IC3 IB5 IC5 < <($PY $D/z16_args.py input $D/inputs/z16_m7_inputs.json)
for xi in ${Z16_XIS:-0.2}; do
  try control_xi$xi "0 or 1, not validated" 3600 bash -c "exec nice -n 10 timeout -s TERM 3600 $w27 control $CTRL --xi1 $xi --procs 2 --out $D/walks --logs $D/logs > $D/logs/walk_control_xi$xi.log 2>&1"
  try z16m5_xi$xi "0 (M = 5 zero found)" 3600 bash -c "exec nice -n 10 timeout -s TERM 3600 $w26 z16m5 $IA $IW $IB3 $IC3 --xi1 $xi --procs 2 --maxit 25 --out $D/walks --logs $D/logs > $D/logs/walk_z16m5_xi$xi.log 2>&1"
  if read -r ZA ZW ZB3 ZC3 ZB5 ZC5 < <($PY $D/z16_args.py $D/walks/walk_z16m5_xi$xi.json 2>> $D/logs/z16_args.log); then
    try z16_xi$xi "0" 9000 bash -c "exec nice -n 10 timeout -s TERM 9000 $w27 z16 $ZA $ZW $ZB3 $ZC3 $ZB5 $ZC5 --xi1 $xi --procs 2 --out $D/walks --logs $D/logs > $D/logs/walk_z16_xi$xi.log 2>&1"
  else
    log "z16_xi$xi skipped: the M = 5 walk did not converge (logs/z16_args.log)"
  fi
  try z16in_xi$xi "0 (information)" 9000 bash -c "exec nice -n 10 timeout -s TERM 9000 $w27 z16in $IA $IW $IB3 $IC3 $IB5 $IC5 --xi1 $xi --procs 2 --out $D/walks --logs $D/logs > $D/logs/walk_z16in_xi$xi.log 2>&1"
done
$PY $D/eval_z16.py > $D/logs/eval_z16.log 2>&1; log "eval_z16 exit $? (0 when the control passes at a validated radius)"
cp $D/logs/eval_z16.log $D/eval_z16.txt
log "all steps done"
