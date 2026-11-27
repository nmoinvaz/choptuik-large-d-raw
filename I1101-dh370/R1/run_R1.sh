#!/bin/bash
# #1101 R1 on dh370 (t5's order, 27 Nov 07:19 UTC, issue comment 7212257601): ell_refine.py at kappa 0.5 on winb's k_c 127 D 23.0 state, then bar 1, the push, and the root scan of R1's state with the Rust block 12.
# Unit i1101r1 under systemd-inhibit. Stops at the first failure (STOP.txt); R1's outputs are copied and pushed whatever the gate says, the scan runs only if bar 1 passes.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1101-dh370; R=$OUT/R1
WTV=/home/nathan/Source/choptuik-large-d-1025v; WTVM=$WTV/solver/matter
WTS=/home/nathan/Source/choptuik-large-d-1102; WTSM=$WTS/solver/matter; SITE=/home/nathan/Source/ellrs-site-1102
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
TAG=l1kc127k050dh370; SRC=l1kc127wind23; D=23.0; LAMS=(0.045 0.050 0.060 0.070)
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $R/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
push() { bash $OUT/push_1101.sh "$1" >> $R/push.txt 2>&1; step "push: $(tail -1 $R/push.txt)"; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $R/STOP.txt; push "R1 stopped: $*"; exit 1; }
cd $R || exit 9
[ "$(blob $R/inputs/sol_${SRC}_D23.0000.npy)" = 7a1b150c ] && [ "$(blob $R/inputs/$SRC.jsonl)" = eea03461 ] || stop "the inputs are not the pinned blobs 7a1b150c, eea03461"
[ "$(blob $WTVM/data/sol_${SRC}_D23.0000.npy)" = 7a1b150c ] && [ "$(blob $WTVM/data/$SRC.jsonl)" = eea03461 ] || stop "the worktree's data copies are not the pinned blobs"
[ ! -e $WTVM/data/$TAG.jsonl ] && [ ! -e $WTVM/data/sol_${TAG}_D23.0000.npy ] || stop "R1's output names already exist in the worktree's data/"
[ "$(git -C $WTV rev-parse --short=8 HEAD)" = 92b9bf53 ] && [ "$(blob $WTVM/ell_refine.py)" = 631e5801 ] && [ "$(blob $WTVM/dss_ell.py)" = 5d28c19e ] || stop "the scan worktree is not 92b9bf53 with ell_refine.py 631e5801, dss_ell.py 5d28c19e"
step "pins ok: state 7a1b150c, record eea03461 (the k_c 127 D 23.0 state of winb); worktree 92b9bf53, ell_refine.py 631e5801, dss_ell.py 5d28c19e"
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 RAYON_NUM_THREADS=6
cd $WTVM
step "R1 starts: nice 10, 6 threads, cap 57600 s on the python pid (timeout), no retry"
t0=$(date +%s)
nice -n 10 /usr/bin/time -v timeout -k 120 57600 $PY -u ell_refine.py $SRC 127 $TAG 127 1 $D 2.0992182200 --kappa 0.5 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma > $R/R1.log 2>&1
rc=$?; secs=$(( $(date +%s) - t0 ))
step "R1 exit $rc after $secs s"
grep -hE 'Elapsed|Maximum resident' $R/R1.log >> $R/steps.txt
for f in $TAG.jsonl sol_${TAG}_D23.0000.npy; do [ -e $WTVM/data/$f ] && cp -p $WTVM/data/$f $R/; done
if [ $rc -ne 0 ] || [ ! -e $R/$TAG.jsonl ] || [ ! -e $R/sol_${TAG}_D23.0000.npy ]; then stop "R1 exit $rc or its record or state is missing"; fi
SB=$(blob $R/sol_${TAG}_D23.0000.npy); RB=$(blob $R/$TAG.jsonl)
step "R1 state blob $SB, record blob $RB"
$PY -I $R/gate_R1.py $R/$TAG.jsonl > $R/gate.txt 2>&1; g=$?; step "bar 1 gate exit $g: $(cat $R/gate.txt)"
push "R1 (kappa 0.5, k_c 127, D 23.0) done: exit $rc, $secs s, gate $g"
[ $g = 0 ] || stop "bar 1 failed: $(cat $R/gate.txt)"
# ------------------------------------------------------------------------------------------------ the root scan (Rust block 12)
[ "$(git -C $WTS rev-parse --short=8 HEAD)" = d4b6b6ce ] && [ "$(blob $WTSM/d18_secant.py)" = 9706e506 ] && [ "$(blob $WTSM/ell_b12rs.py)" = a1fff74f ] && [ "$(blob $WTSM/ellrs/build.sh)" = e6254c9b ] || stop "the Rust worktree is not d4b6b6ce with d18_secant.py 9706e506, ell_b12rs.py a1fff74f, build.sh e6254c9b"
[ "$(blob $OUT/in/read_lower.py)" = 89309d3c ] && [ "$(blob $OUT/in/d185_scan_read.py)" = 7c9d400f ] || stop "the reader or its change finder is not the pinned blob"
export P4_WT_MATTER=$WTSM PYTHONPATH=$SITE OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
cd $WTSM
$PY -c "import ellrs; print('ellrs', ellrs.isa())" > $R/ellrs_isa.txt 2>&1; step "ellrs: $(cat $R/ellrs_isa.txt)"
st=""
for spec in "d18_secant.py selftest:0" "d18_secant.py selftest --mutate=half:1" "d18_secant.py selftest --mutate=norobust:1" "d18_secant.py selftest --mutate=nosigncheck:1" \
            "ell_b12rs.py selftest:0" "ell_b12rs.py selftest --mutate=nolam:1" "ell_b12rs.py selftest --mutate=harm:1"; do
  cmd=${spec%:*}; want=${spec##*:}
  nice -n 10 $PY $cmd > $R/pre/post_$(echo $cmd | tr ' =' '__').txt 2>&1; e=$?
  st="$st [$cmd exit $e, wanted $want]"; [ $e = $want ] || stop "selftest '$cmd' exit $e, wanted $want"
done
( cd $OUT/in
  for spec in "selftest:0" "selftest --mutate=shift:1" "selftest --mutate=round2:1"; do
    cmd=${spec%:*}; want=${spec##*:}; nice -n 10 $PY -I read_lower.py $cmd > $R/pre/post_read_lower_$(echo $cmd | tr ' =' '__').txt 2>&1; e=$?
    echo "[read_lower $cmd exit $e, wanted $want]" >> $R/pre/post_read_lower_exits.txt; [ $e = $want ] || exit 1
  done ) || stop "a read_lower selftest or mutation did not read as written"
step "selftests before the scan:$st; read_lower 0 1 1"
step "scan starts: D $D, lambda ${LAMS[*]} on R1's state, 4 processes x 1 thread, --b12=rust --b12_threads=1, nice 10, pins $SB,$RB"
t1=$(date +%s); pids=()
for i in 0 1 2 3; do
  ( nice -n 10 /usr/bin/time -v $PY -u $WTSM/d18_secant.py scan $R/$TAG.jsonl $R/sol_${TAG}_D23.0000.npy $D ${LAMS[$i]} $R/scan/scan_D23.0_p$i.jsonl --b12=rust --b12_threads=1 --pin=$SB,$RB > $R/scan_p$i.raw 2>&1
    echo "$(stamp) UTC scan p$i (lambda ${LAMS[$i]}) exit $?" >> $R/steps.txt ) &
  pids+=($!)
done
wait "${pids[@]}"
step "scan done: $(( $(date +%s) - t1 )) s"
for i in 0 1 2 3; do grep -h 'the record system\|NOT the record system' $R/scan_p$i.raw >> $R/steps.txt; grep -hE 'Elapsed|Maximum resident' $R/scan_p$i.raw >> $R/steps.txt; done
{ echo "== read_lower.py scan 0.045 0.070"; cd $OUT/in; $PY -I read_lower.py $R/scan 0.045 0.070; echo "(exit $?)"; } > $R/read_lower_R1.txt 2>&1
$PY -I $R/results_R1.py > $R/results_R1.md 2> $R/results_R1.err; step "results_R1.py exit $? (results_R1.md)"
echo "1101 R1 DONE $(stamp) UTC" > $R/DONE.txt
push "R1 root scan done"
step "done"
exit 0
}
