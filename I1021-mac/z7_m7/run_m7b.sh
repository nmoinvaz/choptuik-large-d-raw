#!/bin/bash
# #1021 rerun of box 7 or box 16 at M = 7 at xi1 0.15 under the criteria the coordinator fixed on #1048 (closing comment
# 7034798454; see the output folder's README). The z7_m7 route with walk1026b.py / walk1027b.py (the bars as options) and
# eval_m7b.py (the criteria and the gate). Both controls run first; when either fails its criteria the box walks do not run.
# One walk at a time, 1 process per solve. Usage: run_m7b.sh z7|z16 [REP]   (REP 0, default: z7 writes xi015b/, z16 ../z16_m7/;
# REP 3: the start solves of the M = 5 walks use #1027's three repeats (#1021 rule of 09:19 UTC), z7 writes xi015c/, z16
# ../z16_m7/rep3/; the 0 runs used run_m7b_v1.sh)
set -u
{ # read whole before it runs: an edit of this file cannot reach a running job
. "$(dirname "$0")/common_z7.sh"
BOX=$1; REP=${2:-0}
case $BOX:$REP in z7:0) O=$D/xi015b ;; z16:0) O=$(cd $D/.. && pwd)/z16_m7 ;; z7:3) O=$D/xi015c ;; z16:3) O=$(cd $D/.. && pwd)/z16_m7/rep3 ;; *) echo "BOX z7 or z16, REP 0 or 3"; exit 1 ;; esac
XI=0.15; R5=3.8e-2; R7=0.24; S5=1e-5; S7=3e-4; P5=1e-5; P7=3e-4
EX=$O/exits.txt
log() { echo "$BOX $* $(stamp) UTC" >> $EX; }
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = fc7dee4d ] || { echo "$WT is not at fc7dee4d"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { echo "$WT not clean"; exit 1; }
[ -e $O/README.md ] || { echo "$O/README.md (the criteria) missing"; exit 1; }
[ -e $O/walks ] && { echo "$O/walks exists"; exit 1; }
mkdir -p $O/logs $O/walks $NUMBA_CACHE_DIR
log "start, code $(git -C $WT rev-parse --short=8 HEAD), $($PY -c 'import sys,numpy,scipy,numba;print("python",sys.version.split()[0],"numpy",numpy.__version__,"scipy",scipy.__version__,"numba",numba.__version__)'), bars r1 $R5/$R7 step $S5/$S7 pos $P5/$P7, start repeats $REP"
try() { local name=$1 want=$2 cap=$3; shift 3; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc (expected $want) wall $(( $(date +%s) - s )) s, cap $cap s"; return $rc; }
E="$PY $D/eval_m7b.py"
$E --selftest > $O/logs/eval_selftest.log 2>&1; log "eval_m7b selftest exit $? (0)"
for m in shift pos7 nogate ratio; do $E --selftest --mutate=$m > $O/logs/eval_selftest_$m.log 2>&1; log "eval_m7b selftest --mutate=$m exit $? (1)"; done
$E --box $BOX --dir $O/walks > $O/logs/eval_stored_control.log 2>&1; log "eval_m7b on the stored control exit $? (0)"
$E --box $BOX --dir $O/walks --mutate=shift > $O/logs/eval_mutate_shift.log 2>&1; log "eval_m7b --mutate=shift exit $? (1)"
for w in walk1026b walk1027b; do
  $PY $D/$w.py --selftest > $O/logs/${w}_selftest.log 2>&1; log "$w selftest exit $? (0)"
  $PY $D/$w.py --selftest --mutate=noposbar > $O/logs/${w}_selftest_noposbar.log 2>&1; log "$w selftest --mutate=noposbar exit $? (1)"
  if [ $w = walk1026b ]; then $PY $D/$w.py --selftest --mutate=norepeat > $O/logs/${w}_selftest_norepeat.log 2>&1; log "$w selftest --mutate=norepeat exit $? (1)"; fi
done
cd $WT/solver/inner_stokes || exit 1
for c in "capcheck:0" "capcheck MAXFEV100:1" "check 1 3 5 7:0" "check 3 5 --mutate=sign:1"; do
  a=${c%:*}; want=${c##*:}; f=$(echo "$a" | tr ' =' '__' | tr -d -)
  if [ "$a" = "capcheck MAXFEV100" ]; then INNER_NB_MAXFEV=100 nice -n 10 $PY -u inner_nb.py capcheck > $O/logs/inner_nb_$f.log 2>&1
  else nice -n 10 $PY -u inner_nb.py $a > $O/logs/inner_nb_$f.log 2>&1; fi
  log "inner_nb.py $a exit $? ($want)"
done
nice -n 10 $PY -u hier_nb.py selftest > $O/logs/hier_nb_selftest.log 2>&1; log "hier_nb.py selftest exit $? (0)"
nice -n 10 $PY -u hier_nb.py selftest --mutate=radius > $O/logs/hier_nb_selftest_mutate.log 2>&1; log "hier_nb.py selftest --mutate=radius exit $? (1)"
w26="$PY -u $D/walk1026b.py"; w27="$PY -u $D/walk1027b.py"
CTRL5="2.726475885672135 1.0156030949093042 0.1444194785 0.0110874259"
CTRL="2.718579189229888 0.9992284031945021 0.1492035749173264 0.01471905249087869 0.008405346906375517 0.0014703451817031647"
read -r IA IW IB3 IC3 < $D/inputs/${BOX}_start.txt
try control5_xi$XI "0 (a gate)" 7200 bash -c "exec timeout -s TERM 7200 $w26 control5 $CTRL5 --xi1 $XI --procs 1 --maxit 25 --r1bar $R5 --stepbar $S5 --start_repeats $REP --out $O/walks --logs $O/logs > $O/logs/walk_control5_xi$XI.log 2>&1"
try control_xi$XI "0 (a gate)" 7200 bash -c "exec timeout -s TERM 7200 $w27 control $CTRL --xi1 $XI --procs 1 --r1bar $R7 --stepbar $S7 --out $O/walks --logs $O/logs > $O/logs/walk_control_xi$XI.log 2>&1"
$E --box $BOX --dir $O/walks > $O/logs/eval_gate.log 2>&1
if grep -q "M = 5 control (#1026's): PASS" $O/logs/eval_gate.log && grep -q "M = 7 control (#1027's): PASS" $O/logs/eval_gate.log; then
  log "gate: both controls pass"
  try ${BOX}m5_xi$XI "0 (M = 5 zero found)" 7200 bash -c "exec timeout -s TERM 7200 $w26 ${BOX}m5 $IA $IW $IB3 $IC3 --xi1 $XI --procs 1 --maxit 25 --r1bar $R5 --stepbar $S5 --posbar $P5 --start_repeats $REP --out $O/walks --logs $O/logs > $O/logs/walk_${BOX}m5_xi$XI.log 2>&1"
  if read -r ZA ZW ZB3 ZC3 ZB5 ZC5 < <($PY $D/z16_args.py $O/walks/walk_${BOX}m5_xi$XI.json 2>> $O/logs/z16_args.log); then
    try ${BOX}_xi$XI "0" 18000 bash -c "exec timeout -s TERM 18000 $w27 $BOX $ZA $ZW $ZB3 $ZC3 $ZB5 $ZC5 --xi1 $XI --procs 1 --r1bar $R7 --stepbar $S7 --posbar $P7 --out $O/walks --logs $O/logs > $O/logs/walk_${BOX}_xi$XI.log 2>&1"
  else
    log "${BOX}_xi$XI skipped: the M = 5 walk did not converge (logs/z16_args.log)"
  fi
else
  log "gate: a control failed (logs/eval_gate.log); the box walks do not run"
fi
$E --box $BOX --dir $O/walks > $O/logs/eval.log 2>&1; log "eval_m7b exit $? (0)"
cp $O/logs/eval.log $O/eval.txt
log "all steps done"
exit
}
