#!/bin/bash
# #1083 on dh370 (t5's order): the matched mode determinant checks of hp/mode_matched.py (wip/mode-horizon-1083 7c6177e1, blob 3dd81b39) on main's kernel, in the venv of the #1082 build, 6 threads, nice 10.
# Starts after ../I1082-dh370/1082_B_DONE.txt (build and bit-identity passed), beside the decisive test (4 threads) if the 1-minute load average is at most 12 three minutes after its selftest ran, else after it (1082_DONE.txt).
# Order: toy (+ its --mutate=shift control); four, four --match=out (must exit 1); root D 3.15 hmax 0.001 --both; planted, --mutate=shift (must exit 1), --mutate=outward (exit 0 = control fired); d315; identity hmax 0.001.
# Each command under timeout 14400 (4 h); an exception (a Traceback in its log), a control that does not fire or a timeout stops the run; a criterion that FAILS (exit 1 of a verdict subcommand) is recorded and the run goes on.
# PART 2 (unit i1083b): steps 2b to 5b after the decisive test ended (part 1, unit i1083a, ran toy, toy --mutate=shift and four, and was stopped after four: the load stayed above 12). Unit i1083b. Log: steps_1083.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1083-dh370
X=/home/nathan/Source/choptuik-large-d-raw-wt613/I1082-dh370
WT=/home/nathan/Source/choptuik-large-d-1083
PY=/home/nathan/Source/choptuik-large-d-1082/.venv/bin/python
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
S1=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
S2=$RAWIN/I1072-dh370/states2/tmap_tmap_lowDhm_x0.000625-0.9_D3.1500_M160_L0.7_M128_s1.8326_L0.7_M96_s1.8326.npz
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
unset HP_DENSE_M_MAX HP_MODE_EQUIL
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_1083.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_1083_$1.txt; step "STOP $1: $2"; echo "1083 CHAIN STOPPED at $1 $(stamp) UTC" > $OUT/1083_DONE.txt; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $OUT || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 7c6177e1 ] && [ "$(blob $WT/hp/mode_matched.py)" = 3dd81b39 ] && [ "$(blob $S1)" = 6a0f83d2 ] && [ "$(blob $S2)" = 9e683a14 ] || stop 0 "the worktree, mode_matched.py or a state not pinned (7c6177e1, 3dd81b39, 6a0f83d2, 9e683a14)"
step "part 2 (the first part, unit i1083a, was stopped after its step 2_four: load above 12 with the decisive test and the walk): waiting for $X/1082_DONE.txt, then steps 2b to 5b"
while [ ! -f $X/1082_DONE.txt ]; do sleep 60; done
step "the decisive test ended ($(cat $X/1082_DONE.txt | cut -c1-120)): starting step 2b with 6 threads"
cd $WT/hp
run() {   # name, expected exit codes (space separated), command words...
  local name=$1 want=$2; shift 2
  local t0=$(date +%s)
  timeout 14400 nice -n 10 $PY -u mode_matched.py "$@" > $OUT/$name.log 2>&1; local rc=$?
  step "$name: mode_matched.py $* : exit $rc (wanted: $want), $(( $(date +%s) - t0 )) s; $(tail -1 $OUT/$name.log | cut -c1-260)"
  echo "$name $rc" >> $OUT/exit_codes.txt
  [ $rc = 124 ] && stop $name "over 4 h"
  grep -q '^Traceback' $OUT/$name.log && stop $name "an exception (see $name.log)"
  case " $want " in *" $rc "*) ;; *) step "$name: exit $rc is not in the wanted set ($want)"; return 1;; esac
  return 0
}
ctl() { run "$@" || stop "${1}" "a control or a step did not read as written"; }
ctl 2b_four_match_out "1" four $OUT/four_out.jsonl $S1 --threads=6 --match=out
run 3_root_D3.15_h0.001 "0 1" root $OUT/root_D3.15_h0.001.jsonl $S2 --both --hmax=0.001 --lam0=4.3977863455 --threads=6 || true
run 4_planted "0 1" planted $OUT/planted.jsonl $S1 --threads=6 || true
ctl 4b_planted_mutate_shift "1" planted $OUT/planted_shift.jsonl $S1 --threads=6 --mutate=shift
ctl 4c_planted_mutate_outward "0" planted $OUT/planted_outward.jsonl $S1 --threads=6 --mutate=outward
run 5_d315 "0 1" d315 $OUT/d315.jsonl $S2 --threads=6 || true
run 5b_identity_h0.001 "0 1" identity $OUT/identity_h0.001.jsonl $S2 --hmax=0.001 --threads=6 || true
echo "1083 CHAIN DONE $(stamp) UTC (exit codes in exit_codes.txt)" > $OUT/1083_DONE.txt
step "chain done"
exit 0
}
