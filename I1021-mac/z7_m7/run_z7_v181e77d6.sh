#!/bin/bash
# #1021 (Mac): box 7's zero at M = 7 by #1027's protocol and rule at xi1 0.2 only, the route of I1021-dh610/z16_m7 (raw
# 5b72af8c, run_z16.sh) with the known zero's M = 5 (#1026) and M = 7 (#1027) controls at 0.2 (see README.md). One walk at
# a time, 1 process (--procs 1; dh610: 2), each walk's cap twice dh610's. Steps: the evaluator's checks, the compiled
# backend's checks (inner_nb_checks.sh's lines, logs here), control5, control, z7m5, z7 (when z7m5 converges), eval_z7.
set -u
{ # read whole before it runs: an edit of this file cannot reach a running job
. "$(dirname "$0")/common_z7.sh"
EX=$D/exits_z7.txt
log() { echo "z7 $* $(stamp) UTC" >> $EX; }
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = fc7dee4d ] || { echo "$WT is not at fc7dee4d"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { echo "$WT not clean"; exit 1; }
[ -e $D/walks/walk_z7m5_xi0.2.json ] && { echo "walks exist"; exit 1; }
mkdir -p $D/logs $D/walks $NUMBA_CACHE_DIR
log "start, code $(git -C $WT rev-parse --short=8 HEAD), $($PY -c 'import sys,numpy,scipy,numba;print("python",sys.version.split()[0],"numpy",numpy.__version__,"scipy",scipy.__version__,"numba",numba.__version__)')"
try() { local name=$1 want=$2 cap=$3; shift 3; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc (expected $want) wall $(( $(date +%s) - s )) s, cap $cap s"; return $rc; }
w26="$PY -u $D/walk1026.py"; w27="$PY -u $D/walk1027.py"
$PY $D/eval_z7.py --selftest > $D/logs/eval_selftest.log 2>&1; log "eval_z7 selftest exit $? (0)"
$PY $D/eval_z7.py --selftest --break > $D/logs/eval_selftest_break.log 2>&1; log "eval_z7 selftest --break exit $? (1)"
$PY $D/eval_z7.py > $D/logs/eval_stored_control.log 2>&1; log "eval_z7 on the stored control exit $? (0)"
$PY $D/eval_z7.py --mutate=shift > $D/logs/eval_mutate_shift.log 2>&1; log "eval_z7 --mutate=shift exit $? (1)"
$PY $D/eval1026.py --selftest > $D/logs/eval1026_selftest.log 2>&1; log "eval1026 selftest exit $? (0)"
cd $WT/solver/inner_stokes || exit 1
for c in "capcheck:0" "capcheck MAXFEV100:1" "check 1 3 5 7:0" "check 3 5 --mutate=sign:1"; do
  a=${c%:*}; want=${c##*:}; f=$(echo "$a" | tr ' =' '__' | tr -d -); 
  if [ "$a" = "capcheck MAXFEV100" ]; then INNER_NB_MAXFEV=100 nice -n 10 $PY -u inner_nb.py capcheck > $D/logs/inner_nb_$f.log 2>&1
  else nice -n 10 $PY -u inner_nb.py $a > $D/logs/inner_nb_$f.log 2>&1; fi
  log "inner_nb.py $a exit $? ($want)"
done
nice -n 10 $PY -u hier_nb.py selftest > $D/logs/hier_nb_selftest.log 2>&1; log "hier_nb.py selftest exit $? (0)"
nice -n 10 $PY -u hier_nb.py selftest --mutate=radius > $D/logs/hier_nb_selftest_mutate.log 2>&1; log "hier_nb.py selftest --mutate=radius exit $? (1)"
CTRL5="2.726475885672135 1.0156030949093042 0.1444194785 0.0110874259"
CTRL="2.718579189229888 0.9992284031945021 0.1492035749173264 0.01471905249087869 0.008405346906375517 0.0014703451817031647"
read -r IA IW IB3 IC3 < $D/inputs/z7_start.txt
xi=0.2
try control5_xi$xi "0 (#1026's M = 5 control)" 7200 bash -c "exec timeout -s TERM 7200 $w26 control5 $CTRL5 --xi1 $xi --procs 1 --maxit 25 --out $D/walks --logs $D/logs > $D/logs/walk_control5_xi$xi.log 2>&1"
try control_xi$xi "0 or 1, not validated at 0.2" 7200 bash -c "exec timeout -s TERM 7200 $w27 control $CTRL --xi1 $xi --procs 1 --out $D/walks --logs $D/logs > $D/logs/walk_control_xi$xi.log 2>&1"
try z7m5_xi$xi "0 (M = 5 zero found)" 7200 bash -c "exec timeout -s TERM 7200 $w26 z7m5 $IA $IW $IB3 $IC3 --xi1 $xi --procs 1 --maxit 25 --out $D/walks --logs $D/logs > $D/logs/walk_z7m5_xi$xi.log 2>&1"
if read -r ZA ZW ZB3 ZC3 ZB5 ZC5 < <($PY $D/z16_args.py $D/walks/walk_z7m5_xi$xi.json 2>> $D/logs/z16_args.log); then
  try z7_xi$xi "0" 18000 bash -c "exec timeout -s TERM 18000 $w27 z7 $ZA $ZW $ZB3 $ZC3 $ZB5 $ZC5 --xi1 $xi --procs 1 --out $D/walks --logs $D/logs > $D/logs/walk_z7_xi$xi.log 2>&1"
else
  log "z7_xi$xi skipped: the M = 5 walk did not converge (logs/z16_args.log)"
fi
$PY $D/eval_z7.py > $D/logs/eval_z7.log 2>&1; log "eval_z7 exit $? (0 when the stored control passes)"
cp $D/logs/eval_z7.log $D/eval_z7.txt
log "all steps done"
exit
}
