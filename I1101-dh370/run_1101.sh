#!/bin/bash
# #1101 follow-up (t5's order, 27 Nov 01:57 UTC): does re-solving the accepted k_c 127 D 23.0 state at the same k_c and kappa move the root lambda_1 too?
# d18_secant.py scan (92b9bf53, blob eb1396ad; the worktree ~/Source/choptuik-large-d-1025v) on state A (winb's original) and state B (win2's re-solve R0), each at lambda 0.045 and 0.050:
# 4 evaluations, 2 processes (one per state), 1 thread each, nice 19, --pin per state. Then read_lower.py on each state's two points and results.py (the table). A systemd user unit (i1101a).
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1101-dh370
WTV=/home/nathan/Source/choptuik-large-d-1025v; WTVM=$WTV/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
D=23.0; LAMS=0.045,0.050
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP.txt; exit 1; }
cd $OUT || exit 9
declare -A SF=( [A]=inputs/A/sol_l1kc127wind23_D23.0000.npy [B]=inputs/B/sol_l1kc127k070w2_D23.0000.npy )
declare -A RF=( [A]=inputs/A/l1kc127wind23.jsonl [B]=inputs/B/l1kc127k070w2.jsonl )
declare -A SBW=( [A]=7a1b150c [B]=90d3e655 )
declare -A RBW=( [A]=eea03461 [B]=d1a3a641 )
for X in A B; do
  [ "$(blob ${SF[$X]})" = "${SBW[$X]}" ] && [ "$(blob ${RF[$X]})" = "${RBW[$X]}" ] || stop "state $X: ${SF[$X]} or ${RF[$X]} is not the pinned blob (${SBW[$X]}, ${RBW[$X]})"
done
[ "$(git -C $WTV rev-parse --short=8 HEAD)" = 92b9bf53 ] && [ "$(blob $WTVM/d18_secant.py)" = eb1396ad ] || stop "the worktree is not 92b9bf53 or d18_secant.py is not eb1396ad"
[ "$(blob in/read_lower.py)" = 89309d3c ] && [ "$(blob in/d185_scan_read.py)" = 7c9d400f ] || stop "the reader or its change finder is not the pinned blob"
step "pins ok: state A $(blob ${SF[A]}) record $(blob ${RF[A]}); state B $(blob ${SF[B]}) record $(blob ${RF[B]}); d18_secant.py eb1396ad at 92b9bf53; read_lower.py 89309d3c"
export P4_WT_MATTER=$WTVM OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
( cd $WTVM
  nice -n 19 $PY -I d18_secant.py selftest > $OUT/selftest_secant.txt 2>&1; echo $? > $OUT/.e0
  nice -n 19 $PY -I d18_secant.py selftest --mutate=half > $OUT/selftest_secant_half.txt 2>&1; echo $? > $OUT/.e1
  nice -n 19 $PY -I d18_secant.py selftest --mutate=norobust > $OUT/selftest_secant_norobust.txt 2>&1; echo $? > $OUT/.e2
  nice -n 19 $PY -I d18_secant.py selftest --mutate=nosigncheck > $OUT/selftest_secant_nosigncheck.txt 2>&1; echo $? > $OUT/.e3 )
e0=$(cat .e0); e1=$(cat .e1); e2=$(cat .e2); e3=$(cat .e3); rm -f .e0 .e1 .e2 .e3
step "d18_secant.py selftest exit $e0 (0 wanted); mutations half exit $e1, norobust exit $e2, nosigncheck exit $e3 (1 wanted each)"
[ $e0 = 0 ] && [ $e1 = 1 ] && [ $e2 = 1 ] && [ $e3 = 1 ] || stop "a selftest or a mutation of d18_secant.py did not read as written"
( cd in; nice -n 19 $PY -I read_lower.py selftest > $OUT/selftest_read_lower.txt 2>&1; echo $? > $OUT/.r0
  nice -n 19 $PY -I read_lower.py selftest --mutate=shift > $OUT/selftest_read_lower_shift.txt 2>&1; echo $? > $OUT/.r1
  nice -n 19 $PY -I read_lower.py selftest --mutate=round2 > $OUT/selftest_read_lower_round2.txt 2>&1; echo $? > $OUT/.r2 )
r0=$(cat .r0); r1=$(cat .r1); r2=$(cat .r2); rm -f .r0 .r1 .r2
step "read_lower selftest exit $r0 (0 wanted); mutations shift exit $r1, round2 exit $r2 (1 wanted each)"
[ $r0 = 0 ] && [ $r1 = 1 ] && [ $r2 = 1 ] || stop "a read_lower selftest or mutation did not read as written"
step "scan starts: D $D, lambda $LAMS on state A and on state B, 2 processes x 1 thread, nice 19"
t0=$(date +%s); pids=()
for X in A B; do
  mkdir -p scan_$X
  ( cd $WTVM && nice -n 19 /usr/bin/time -v $PY -u $WTVM/d18_secant.py scan $OUT/${RF[$X]} $OUT/${SF[$X]} $D $LAMS $OUT/scan_$X/scan_D23.0_p0.jsonl --pin=${SBW[$X]},${RBW[$X]} > $OUT/scan_$X.raw 2>&1
    rc=$?; echo "$(stamp) UTC state $X exit $rc" >> $OUT/steps.txt ) &
  pids+=($!)
done
wait "${pids[@]}"
step "scan done: $(( $(date +%s) - t0 )) s"
for X in A B; do grep -h 'the record system\|NOT the record system' scan_$X.raw >> steps.txt; grep -hE 'Elapsed|Maximum resident' scan_$X.raw >> steps.txt; done
cd in
for X in A B; do { echo "== state $X: read_lower.py scan_$X 0.045 0.050"; $PY -I read_lower.py $OUT/scan_$X 0.045 0.050; echo "(exit $?)"; } > $OUT/read_lower_$X.txt 2>&1; done
cd $OUT
python3 -I results.py > results.md 2> results.err; step "results.py exit $? (results.md)"
echo "1101 DONE $(stamp) UTC" > $OUT/DONE.txt
step "done"
exit 0
}
