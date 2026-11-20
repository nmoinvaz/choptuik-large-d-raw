#!/bin/bash
# #1021 step (dh610): box 16 at xi1 0.15, M = 5 walk then M = 7, with #1026's M = 5 control and #1027's M = 7 control as gates (README.md).
# One walk at a time, --procs 2, nice 10; each walk's cap (3 x its estimate) is a timeout on its exact pid. If a control fails at 0.15 the driver stops after the
# controls (the result is then no verdict, with their residuals): the box 16 walks would not count.
. "$(dirname "$0")/../common_z16.sh"
X=$D/xi015
EX=$X/exits_z16_015.txt
log() { echo "z16xi015 $* $(stamp) UTC" >> $EX; }
cd $WT/solver/inner_stokes || exit 1
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = fc7dee4d ] || { echo "cl-995 is not at fc7dee4d"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { echo "cl-995 not clean"; exit 1; }
log "start, code $(git -C $WT rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)"
w26="$PY -u $D/walk1026.py"; w27="$PY -u $D/walk1027.py"
try() { local name=$1 want=$2 cap=$3; shift 3; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc (expected $want) wall $(( $(date +%s) - s )) s, cap $cap s"; return $rc; }
$PY $X/eval_z16_015.py --selftest > $X/logs/eval_selftest.log 2>&1; log "eval_z16_015 selftest exit $? (0)"
$PY $X/eval_z16_015.py --selftest --break > $X/logs/eval_selftest_break.log 2>&1; log "eval_z16_015 selftest --break exit $? (1)"
CTRL5="2.726475885672135 1.0156030949093042 0.1444194785 0.0110874259"
CTRL7="2.718579189229888 0.9992284031945021 0.1492035749173264 0.01471905249087869 0.008405346906375517 0.0014703451817031647"
Z3="3.553346604669 0.413172284516 0.7598443752 0.0120820005"
read -r IA IW IB3 IC3 IB5 IC5 < <($PY $D/z16_args.py input $D/inputs/z16_m7_inputs.json)
O="--procs 2 --out $X/walks --logs $X/logs"
try control5_xi0.15 "0 (gate)" 1800 bash -c "exec nice -n 10 timeout -s TERM 1800 $w26 control5 $CTRL5 --xi1 0.15 --maxit 25 $O > $X/logs/walk_control5_xi0.15.log 2>&1"
try control7_xi0.15 "0 (gate)" 1800 bash -c "exec nice -n 10 timeout -s TERM 1800 $w27 control7 $CTRL7 --xi1 0.15 $O > $X/logs/walk_control7_xi0.15.log 2>&1"
$PY $X/eval_z16_015.py > $X/logs/eval_gates.log 2>&1; g=$?
log "gates exit $g (0: both controls pass): $(grep -E '^gate' $X/logs/eval_gates.log | cut -c1-120 | tr '\n' ' ')"
if [ $g != 0 ]; then
  cp $X/logs/eval_gates.log $X/eval_z16_015.txt
  log "a gate failed: no box 16 walk is run (no verdict at M = 7); see eval_z16_015.txt"
  exit 0
fi
try z16m5_xi0.15 "0 (M = 5 zero found)" 3600 bash -c "exec nice -n 10 timeout -s TERM 3600 $w26 z16m5 $Z3 --xi1 0.15 --maxit 25 $O > $X/logs/walk_z16m5_xi0.15.log 2>&1"
if read -r ZA ZW ZB3 ZC3 ZB5 ZC5 < <($PY $D/z16_args.py $X/walks/walk_z16m5_xi0.15.json 2>> $X/logs/z16_args.log); then
  try z16_xi0.15 "0" 10800 bash -c "exec nice -n 10 timeout -s TERM 10800 $w27 z16 $ZA $ZW $ZB3 $ZC3 $ZB5 $ZC5 --xi1 0.15 $O > $X/logs/walk_z16_xi0.15.log 2>&1"
else
  log "z16_xi0.15 skipped: the M = 5 walk did not converge (logs/z16_args.log)"
fi
try z16in_xi0.15 "0 (information)" 7200 bash -c "exec nice -n 10 timeout -s TERM 7200 $w27 z16in $IA $IW $IB3 $IC3 $IB5 $IC5 --xi1 0.15 $O > $X/logs/walk_z16in_xi0.15.log 2>&1"
$PY $X/eval_z16_015.py > $X/logs/eval_z16_015.log 2>&1; log "eval_z16_015 exit $? (0 when both gates pass)"
cp $X/logs/eval_z16_015.log $X/eval_z16_015.txt
log "all steps done"
