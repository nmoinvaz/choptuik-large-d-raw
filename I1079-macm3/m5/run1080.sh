#!/bin/bash
# #1080 (macm3): do the two certified M = 3 excited zeros of #1079 persist at M = 5? Route of #1026 (run1026.sh.dh610): walk1026.py, the outer Newton over
# complete fixed-(A, w) solves of hier_nb.py 5 --fixA --schur. Stages: 1 the control at xi1 0.2 and its gate (stop if it fails); 2 x1 and x2 at xi1 0.2,
# side by side (2 procs each); 3 x1, x2 and the control at xi1 0.25, side by side (2 procs each, 6 threads); then the report.
# Started detached under caffeinate -is and nice -n 10 (launch.py). Exits and times go to exits_1080.txt.
RAW=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3/m5
WT=/Users/nathan/Source/choptuik-large-d
PY=/Users/nathan/Source/venv-macm3-i1080/bin/python
EX=$RAW/exits_1080.txt
stamp() { date -u '+%F %T'; }
log() { echo "1080 $* $(stamp) UTC" >> $EX; }
export W1026_PY=$PY W1026_WT=$WT
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_NUM_THREADS=1
W="$PY -u $RAW/walk1026.py"
CTRL="2.726475885672135 1.0156030949093042 0.1444194785 0.0110874259"
X1=$($PY $RAW/report1080.py args x1)
X2=$($PY $RAW/report1080.py args x2)
cd $WT/solver/inner_stokes || exit 1
mkdir -p $RAW/walks $RAW/logs
log "start, code $(git -C $WT rev-parse --short=8 HEAD) ($(git -C $WT status --porcelain --untracked-files=no | wc -l | tr -d ' ') tracked changes), load $(uptime | sed 's/.*load averages: //')"
log "x1 args: $X1"
log "x2 args: $X2"

$PY -u $RAW/memlog1080.py $$ >> $RAW/memlog_1080.log 2>&1 &
MEMPID=$!

fail() { log "STOP: $*"; kill $MEMPID 2>/dev/null; exit 1; }
# a Traceback in any solve's or walk's log is a code error, not a result
scan() {
  if grep -l Traceback $RAW/logs/fix_*.log $RAW/logs/walk_*.log 2>/dev/null >> $EX; then
    fail "$1: a Traceback in a log (files listed above)"
  fi
}
try() { local name=$1; shift; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc wall $(( $(date +%s) - s )) s"; return $rc; }
walk_job() { # NAME ARGS XI
  nice -n 10 bash -c "$W $1 $2 --xi1 $3 --procs 2 --maxit 25 > $RAW/logs/walk_$1_xi$3.log 2>&1"
}

$PY $RAW/report1080.py selftest > $RAW/logs/selftest_report.log 2>&1 || fail "report1080.py selftest (logs/selftest_report.log)"
$PY $RAW/eval1026.py --selftest > $RAW/logs/selftest_eval.log 2>&1 || fail "eval1026.py --selftest (logs/selftest_eval.log)"
log "selftests pass"

# 1. control at xi1 0.2, then its gate: PASS within 1e-5 of A 2.718579189, w 0.999228404 (eval1026.py exits 0), and --mutate=shift must exit 1
log "command: $W control $CTRL --xi1 0.2 --procs 2 --maxit 25"
try control_xi0.2 walk_job control "$CTRL" 0.2
scan "control xi1 0.2"
$PY $RAW/eval1026.py --dir $RAW/walks > $RAW/logs/eval_control.log 2>&1; rc=$?
log "gate_control exit $rc: $(head -1 $RAW/logs/eval_control.log | cut -c1-200)"
[ $rc = 0 ] || fail "the control did not reproduce the stored M = 5 zero (logs/eval_control.log)"
$PY $RAW/eval1026.py --dir $RAW/walks --mutate=shift > $RAW/logs/eval_control_mutate_shift.log 2>&1; rc=$?
log "gate_control --mutate=shift exit $rc (expected 1)"
[ $rc = 1 ] || fail "the control's mutation did not fail"

# 2. both zeros at xi1 0.2, side by side
log "command: $W x1 $X1 --xi1 0.2 --procs 2 --maxit 25"
log "command: $W x2 $X2 --xi1 0.2 --procs 2 --maxit 25"
walk_job x1 "$X1" 0.2 &
p1=$!
walk_job x2 "$X2" 0.2 &
p2=$!
wait $p1; log "x1_xi0.2 exit $?"
wait $p2; log "x2_xi0.2 exit $?"
scan "xi1 0.2"

# 3. both zeros and the control at xi1 0.25, side by side
log "command: $W x1 $X1 --xi1 0.25 --procs 2 --maxit 25"
log "command: $W x2 $X2 --xi1 0.25 --procs 2 --maxit 25"
log "command: $W control $CTRL --xi1 0.25 --procs 2 --maxit 25"
walk_job x1 "$X1" 0.25 &
p1=$!
walk_job x2 "$X2" 0.25 &
p2=$!
walk_job control "$CTRL" 0.25 &
p3=$!
wait $p1; log "x1_xi0.25 exit $?"
wait $p2; log "x2_xi0.25 exit $?"
wait $p3; log "control_xi0.25 exit $?"
scan "xi1 0.25"

$PY $RAW/eval1026.py --dir $RAW/walks > $RAW/logs/eval_all.log 2>&1
log "eval1026 (control rows only) exit $?"
$PY $RAW/report1080.py report > $RAW/logs/report.md 2>&1
log "report exit $?"
log "all steps done"
kill $MEMPID 2>/dev/null
