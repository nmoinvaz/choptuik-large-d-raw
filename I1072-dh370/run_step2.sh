#!/bin/bash
# #1072 second amendment (t5, option C with one more solve), unit i1072d, 6 threads, nice 10, worktree 1072b at ae96bcc6:
# 1d  L 0.7 at M' 96 from the converged L 0.7 M' 128 state (same s0); if it fails, step 2 runs on the M' 128 states only
# 2a  gp selftest: lowD_gamma.py --selftest <uniform M 128 state> <L 0.7 M' 128 state> (exit 0)
# 2b  gamma on L 0.7 at M' 128, L 0.7 at M' 96 (if 1d converged), L 0.9 at M' 128 (--lam0=4.397784106690153 --xtol=1e-11), each followed by
#     accept_gamma.py on the records so far; the first failing acceptance stops the run (STOP_2*.txt). Log: steps_step2.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1072-dh370
S128=/home/nathan/Source/choptuik-large-d-raw-push960/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
WT=/home/nathan/Source/choptuik-large-d-1072b
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
ST=$OUT/states2; J=$OUT/solve_new.jsonl; G=$OUT/gamma_D3.15.jsonl
S0=$(cat $OUT/s0_fixed.txt)
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
cd $WT/hp || exit 9
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_step2.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_$1.txt; step "STOP $1: $2"; exit 1; }
saved() { jq -r --argjson L $1 --argjson M $2 'select(.converged==true and .L==$L and .Mp==$M) | .saved' $J | tail -1; }
step "start; worktree $(git -C $WT rev-parse --short=8 HEAD); s0 $S0; load $(cut -d' ' -f1-3 /proc/loadavg)"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = ae96bcc6 ] || stop 1d "worktree not at ae96bcc6"
P07=$(saved 0.7 128); P09=$(saved 0.9 128)
[ -f "$P07" ] && [ -f "$P09" ] || stop 1d "the converged L 0.7 or L 0.9 M' 128 state is missing"
# the checker's own selftest and controls
$PY -I $OUT/accept_gamma.py selftest > $OUT/selftest_accept_gamma.txt 2>&1; e0=$?
for m in shift sign F; do $PY -I $OUT/accept_gamma.py selftest --mutate=$m > /dev/null 2>&1; eval "e_$m=\$?"; done
step "accept_gamma.py selftest exit $e0 (0 wanted); mutations shift $e_shift, sign $e_sign, F $e_F (1 wanted each)"
[ $e0 = 0 ] && [ $e_shift = 1 ] && [ $e_sign = 1 ] && [ $e_F = 1 ] || stop 1d "the acceptance checker's selftest or a control is not as required"
# 1d
t0=$(date +%s)
nice -n 10 timeout 21600 $PY -u tau_map_gain.py solve $P07 --pairs 0.7:96 --s0 $S0 --states $ST --out $J --threads 6 >> $OUT/solve_new.log 2>&1; r=$?
step "1d: L 0.7 at M' 96 from the L 0.7 M' 128 state: exit $r, $(( $(date +%s) - t0 )) s"
P07_96=""; [ $r = 0 ] && P07_96=$(saved 0.7 96)
[ -n "$P07_96" ] && [ -f "$P07_96" ] && echo "1D PASS $(stamp) UTC" > $OUT/STEP1D_DONE.txt || { echo "1D FAIL (step 2 runs on the M' 128 states only) $(stamp) UTC" > $OUT/STEP1D_DONE.txt; step "1d did not converge: step 2 on the M' 128 states only"; P07_96=""; }
# 2a
nice -n 10 $PY lowD_gamma.py --selftest $S128 $P07 --threads=6 > $OUT/selftest_gp_L07_M128.txt 2>&1; g=$?
step "2a: lowD_gamma.py --selftest <uniform M 128> <L 0.7 M' 128>: exit $g (0 wanted); $(tail -2 $OUT/selftest_gp_L07_M128.txt | cut -c1-220 | tr '\n' '|')"
[ $g = 0 ] || stop 2a "the gp selftest on the L 0.7 M' 128 state exited $g"
echo "STEP2A PASS $(stamp) UTC" > $OUT/STEP2A_DONE.txt
# 2b
gamma() {  # state label
  t0=$(date +%s)
  nice -n 10 timeout 14400 $PY -u lowD_gamma.py $G $1 --threads=6 --lam0=4.397784106690153 --xtol=1e-11 > $OUT/gamma_$2.log 2>&1; rc=$?
  step "2b gamma $2: exit $rc, $(( $(date +%s) - t0 )) s; $(tail -1 $G | jq -c '{M,gamma,lam,F,n_signchanges,n_det,seconds}' | cut -c1-200)"
  $PY -I $OUT/accept_gamma.py $G --ref $OUT/in2/ref_uniform_M128.jsonl --ref96 $OUT/in2/ref_uniform_M96.jsonl > $OUT/accept_after_$2.txt 2>&1; ra=$?
  step "acceptance after $2: exit $ra; $(grep -E 'PASS|FAIL' $OUT/accept_after_$2.txt | tail -1)"
  return $(( rc + ra ))
}
gamma $P07 L07_M128 || stop 2b "gamma on L 0.7 at M' 128 (exit or acceptance)"
[ -n "$P07_96" ] && { gamma $P07_96 L07_M96 || stop 2b "gamma on L 0.7 at M' 96 (exit or acceptance)"; }
gamma $P09 L09_M128 || stop 2b "gamma on L 0.9 at M' 128 (exit or acceptance)"
echo "STEP2 DONE $(stamp) UTC" > $OUT/STEP2_DONE.txt
step "step 2 done"
exit 0
}
