#!/bin/bash
# #1072 amended step 1 (t5): step 0 selftests on ae96bcc6, 1a identity control, 1b M 160 source at L 0.9 and 0.7 with a fixed s0, 1c continuation
# in L at M' 128 and the M' 96 states. Each stage stops the run at its first failure (STOP_<stage>.txt). Log: steps_new.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1072-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960/I927-mac/inputs
WT=/home/nathan/Source/choptuik-large-d-1072b
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
S128=$RAWIN/lowDhm_x0.000625-0.9_D3.1500_M128.npz
S160=$RAWIN/lowDhm_x0.000625-0.9_D3.1500_M160.npz
ST=$OUT/states2; mkdir -p $ST
J=$OUT/solve_new.jsonl; LOG=$OUT/solve_new.log
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
cd $WT/hp || exit 9
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_new.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_$1.txt; step "STOP $1: $2"; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
step "start; worktree $(git -C $WT rev-parse --short=8 HEAD); load $(cut -d' ' -f1-3 /proc/loadavg)"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = ae96bcc6 ] || stop 0 "worktree not at ae96bcc6"
[ "$(blob $S128)" = df2ab378 ] || stop 0 "M 128 input is not blob df2ab378"
step "M 160 input blob $(blob $S160); M 128 input df2ab378; lowD_gamma.py $(blob lowD_gamma.py), tau_map_gain.py $(blob tau_map_gain.py), tau_map.py $(blob tau_map.py)"
# 0: the two step-0 selftest calls on ae96bcc6
nice -n 10 $PY lowD_gamma.py --selftest data/lowD_states/highm15_D3.7000_M96.npz --threads=6 > $OUT/selftest_lowD_gamma_ae96bcc6.txt 2>&1; a=$?
nice -n 10 $PY lowD_gamma.py --selftest data/lowD_states/highm15_D3.7000_M96.npz --threads=6 --break > $OUT/selftest_lowD_gamma_break_ae96bcc6.txt 2>&1; b=$?
step "step 0 on ae96bcc6: lowD_gamma.py --selftest exit $a (0 wanted); --selftest --break exit $b (1 wanted)"
[ $a = 0 ] && [ $b = 1 ] || stop 0 "the selftest exits are $a and $b, not 0 and 1"
echo "STEP0B PASS $(stamp) UTC" > $OUT/STEP0B_DONE.txt
# 1a: the identity control
t0=$(date +%s)
nice -n 10 timeout 21600 $PY -u tau_map_gain.py solve $S128 --pairs 1:128 --states $ST --out $OUT/solve_1a_identity.jsonl --threads 6 >> $LOG 2>&1; r=$?
step "1a identity solve (L 1 at M 128 from the M 128 state): exit $r, $(( $(date +%s) - t0 )) s"
nice -n 10 $PY tau_map_gain.py report $OUT/solve_1a_identity.jsonl --ref $S128 > $OUT/report_1a.txt 2>&1; rr=$?
step "1a report (the tool's identity check): exit $rr; $(grep 'identity:' $OUT/report_1a.txt | cut -c1-260)"
[ $r = 0 ] && [ $rr = 0 ] && grep -q 'identity: .*PASS' $OUT/report_1a.txt || stop 1a "identity solve exit $r, report exit $rr"
echo "STEP1A PASS $(stamp) UTC" > $OUT/STEP1A_DONE.txt
# 1b: the better source, s0 fixed from pick_s0 for L 0.5 on the M 160 state
S0=$($PY -c "
import sys; sys.path.insert(0, '.')
import tau_map_gain as g
print(repr(g.resolve_s0('$S160', 0.5, None)))" 2>/dev/null | tail -1)
[ -n "$S0" ] || stop 1b "pick_s0 gave nothing"
echo "$S0" > $OUT/s0_fixed.txt; step "1b: pick_s0 for L 0.5 on the M 160 state: s0 = $S0 (fixed for 1b and 1c)"
saved() { jq -r --argjson L $1 --argjson M $2 'select(.converged==true and .L==$L and .Mp==$M) | .saved' $J | tail -1; }
solve() {  # state L Mp
  t0=$(date +%s)
  nice -n 10 timeout 21600 $PY -u tau_map_gain.py solve $1 --pairs $2:$3 --s0 $S0 --states $ST --out $J --threads 6 >> $LOG 2>&1; rc=$?
  step "solve $(basename $1 .npz | cut -c1-60) -> L $2 M' $3: exit $rc, $(( $(date +%s) - t0 )) s"
  return $rc
}
solve $S160 0.9 128 || stop 1b "L 0.9 at M' 128 from the M 160 state did not converge (then the map, not the source, is the problem at D 3.15)"
echo "STEP1B_L09 PASS $(stamp) UTC" > $OUT/STEP1B_L09_DONE.txt
solve $S160 0.7 128 || stop 1b "L 0.7 at M' 128 from the M 160 state did not converge"
P07=$(saved 0.7 128); [ -f "$P07" ] || stop 1b "no saved state for L 0.7 M' 128"
echo "STEP1B PASS $(stamp) UTC" > $OUT/STEP1B_DONE.txt
# 1c: continuation in L at M' 128, then M' 96
solve $P07 0.5 128 || stop 1c "L 0.5 at M' 128 from the L 0.7 state did not converge"
P05=$(saved 0.5 128); [ -f "$P05" ] || stop 1c "no saved state for L 0.5 M' 128"
solve $P05 0.4 128 || stop 1c "L 0.4 at M' 128 from the L 0.5 state did not converge"
P04=$(saved 0.4 128); [ -f "$P04" ] || stop 1c "no saved state for L 0.4 M' 128"
solve $P05 0.5 96 || stop 1c "L 0.5 at M' 96 from the L 0.5 M' 128 state did not converge"
solve $P04 0.4 96 || stop 1c "L 0.4 at M' 96 from the L 0.4 M' 128 state did not converge"
echo "STEP1C PASS $(stamp) UTC" > $OUT/STEP1C_DONE.txt
step "1a, 1b and 1c done: converged states at L 0.5 and 0.4, M' 96 and 128 in $ST"
exit 0
}
