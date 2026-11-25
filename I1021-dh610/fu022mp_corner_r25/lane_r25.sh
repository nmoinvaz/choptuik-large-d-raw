#!/bin/bash
# #1076 fu022mp_corner_r25 (dh610), the coordinator's order of 25 Nov (hc): recount the two unresolved quarters SW and SE of the unresolved box at --r1=0.25 (the radius at which the continuation is accepted at the corner and at
# (3.787, 0.2315)), and, as the control for the assumption that the zero set does not depend on xi1, the NW quarter at r1 0.25 first (it must read resolved with winding 0 and no zero, as at 0.17); a control that fires stops the work.
# From level 1's cache (4228 lines at xi1 0.17, the r1b file; the 0.25 cache starts empty), argcount at 20ad2589 (worktree ~/Source/choptuik-large-d-1076b, detached, clean), the options of the recount without --retry, --r1=0.25
# --r1b=0.17, --procs=4, nice 10 raised to 19 by watch_i1088a_r25.sh while an i1088a unit is active. Modes: dry (pins and selftests only), full. Stage 1: NW; the control (read_r25.py control: 0 PASS, 1 FIRES, 2 INCONCLUSIVE; FIRES stops the
# lane, INCONCLUSIVE goes on and is reported); stage 2: SW and SE. Then the prefix checks (the r1b cache and the 0.2 file keep their first lines; a one-byte edit of a copy fails: 1) and read_r25.py (reading.txt). Nothing is stopped or
# terminated for memory (Nathan's rule of 2026-11-08). Logs in logs/.
{
set -u
MODE=${1:-full}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1021-dh610/fu022mp_corner_r25; E1=$RAW/I1021-dh610/fu022mp_corner_e1; IN=$F/in; M=$F/m3; LG=$F/logs
CODE=/home/nathan/Source/choptuik-large-d-1076b; SI=$CODE/solver/inner_stokes; PY=/home/nathan/Source/venv-i1058/bin/python
L=$F/exits.txt; C25=$M/points_M3_r0.25.jsonl; C17=$M/points_M3_r0.17.jsonl; N0=4228; CAP=43200
TAGN=M3_fu022mp_r25_nw_r0.25; TAGL=M3_fu022mp_r25_lower_r0.25
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC fu022mp_corner_r25: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
mkdir -p $LG $F/tmp $M
bad=0
while read bb f; do [ -f $F/$f ] && [ "$(blob $F/$f)" = "$bb" ] || { say "refuse: $F/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs.txt
while read bb f; do [ -f $f ] && [ "$(blob $f)" = "$bb" ] || { say "refuse: $f missing or not blob $bb"; bad=1; }; done < $F/in_blobs_src.txt
[ "$(git -C $CODE rev-parse --short=8 HEAD)" = 20ad2589 ] || { say "refuse: code is not at 20ad2589"; bad=1; }
[ -z "$(git -C $CODE status --short)" ] || { say "refuse: worktree $CODE has changes"; bad=1; }
[ "$(wc -l < $E1/m3/points_M3_r0.17.jsonl)" = $N0 ] || { say "refuse: the source cache is not $N0 lines"; bad=1; }
if [ "$MODE" = full ]; then for f in $M/count_$TAGN.json $M/count_$TAGL.json $C25 $C17 $M/points_M3_r0.2.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done; fi
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge 16777216 ] || { say "refuse: MemAvailable $av kB is below 16 GiB"; bad=1; }
[ $bad = 0 ] || exit 2
say "start (mode $MODE; pins checked: in_blobs.txt, in_blobs_src.txt, code 20ad2589 clean, source cache $N0 lines, MemAvailable $av kB, load $(cut -d' ' -f1-3 /proc/loadavg), $($PY -VV 2>&1 | head -1 | cut -c1-30), python-flint $($PY -c 'import flint; print(flint.__version__)'), mpmath $($PY -c 'import mpmath; print(mpmath.__version__)'))"
cd $SI
s=""
nice -n 19 $PY -u argcount.py --selftest > $LG/selftest_argcount.log 2>&1; s="$s $?"
for m in nosplit conj norecount; do nice -n 19 $PY -u argcount.py --selftest --mutate=$m > $LG/selftest_argcount_$m.log 2>&1; s="$s $?"; done
say "argcount selftest, nosplit, conj, norecount exits:$s (wanted 0 1 1 1)"
[ "$s" = " 0 1 1 1" ] || { say "STOP: the selftests did not behave"; exit 1; }
nice -n 19 $PY -u argcount_tie_check.py > $LG/tie_check.log 2>&1; t0r=$?
nice -n 19 $PY -u argcount_tie_check.py --mutate=pykey > $LG/tie_check_mutate_pykey.log 2>&1; t1r=$?
$PY -I $F/read_r25.py selftest > $LG/selftest_read_r25.log 2>&1; r0=$?
$PY -I $F/read_r25.py selftest --mutate > $LG/selftest_read_r25_mutate.log 2>&1; r1=$?
say "argcount_tie_check.py exit $t0r (0 wanted), --mutate=pykey exit $t1r (1 wanted); read_r25.py selftest exit $r0 (0 wanted), --mutate exit $r1 (1 wanted)"
[ "$t0r $t1r $r0 $r1" = "0 1 0 1" ] || { say "STOP: a check did not behave"; exit 1; }
[ "$MODE" = full ] || { say "dry run: nothing started"; exit 0; }
cp $E1/m3/points_M3_r0.17.jsonl $C17; cp $E1/m3/points_M3_r0.2.jsonl $M/points_M3_r0.2.jsonl
[ "$(blob $C17 | cut -c1-8)" = 6e9ffcf5 ] && [ "$(blob $M/points_M3_r0.2.jsonl | cut -c1-8)" = 86ffeb0e ] || { say "STOP: the copied caches are not the pinned blobs"; exit 1; }
OPT="--M=3 --r1=0.25 --r1b=0.17 --seed=$M/points_M3_r0.2.jsonl --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4 --m3mp --out=$M"
t0=$(date +%s)
( while sleep 60; do
    echo "$(date -u '+%F %T') UTC python $(ps -eo cmd | grep -c "[a]rgcount.py.*r25"), MemAvailable_kB $(awk '/MemAvailable/ {print $2}' /proc/meminfo), load $(cut -d' ' -f1 /proc/loadavg), cache25_lines $(wc -l < $C25 2>/dev/null || echo 0)" >> $LG/sampler.log
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    [ "$avs" -lt 4194304 ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT.txt
  done ) &
SAMP=$!
say "stage 1 (the control, NW at r1 0.25) starts (cwd $SI, 4 processes of 1 thread, nice 10 raised to 19 by the watcher while an i1088a unit is active, timeout $CAP s): nice -n 10 timeout $CAP $PY -u argcount.py --recount=$IN/cells_nw.jsonl $OPT --tag=$TAGN"
( cd $SI && nice -n 10 timeout $CAP $PY -u argcount.py --recount=$IN/cells_nw.jsonl $OPT --tag=$TAGN > $LG/recount_nw.log 2>&1 ); rc1=$?
say "stage 1 exit $rc1 (0 wanted; 124 is the cap), wall $(( $(date +%s) - t0 )) s, 0.25 cache $(wc -l < $C25 2>/dev/null || echo 0) lines"
[ $rc1 = 0 ] || { kill $SAMP 2>/dev/null; say "STOP: stage 1 exit $rc1"; exit 1; }
$PY -I $F/read_r25.py control $M/count_$TAGN.json > $LG/control.log 2>&1; cr=$?
say "control (NW at r1 0.25, winding 0 and no zero wanted): $(cat $LG/control.log) (exit $cr: 0 PASS, 1 FIRES, 2 INCONCLUSIVE)"
[ $cr != 1 ] || { kill $SAMP 2>/dev/null; say "STOP: the control fires (the NW quarter at r1 0.25 is resolved with a nonzero winding, leaf sum or zero); the work stops and is reported"; exit 1; }
t1=$(date +%s)
say "stage 2 (SW and SE at r1 0.25) starts: nice -n 10 timeout $CAP $PY -u argcount.py --recount=$IN/cells_sw_se.jsonl $OPT --tag=$TAGL"
( cd $SI && nice -n 10 timeout $CAP $PY -u argcount.py --recount=$IN/cells_sw_se.jsonl $OPT --tag=$TAGL > $LG/recount_lower.log 2>&1 ); rc2=$?
kill $SAMP 2>/dev/null
say "stage 2 exit $rc2 (0 wanted; 124 is the cap), wall $(( $(date +%s) - t1 )) s, 0.25 cache $(wc -l < $C25) lines"
head -n $N0 $C17 | cmp - $E1/m3/points_M3_r0.17.jsonl > $LG/prefix_cmp.log 2>&1; pk=$?
cmp $M/points_M3_r0.2.jsonl $E1/m3/points_M3_r0.2.jsonl > $LG/prefix_cmp_02.log 2>&1; p2=$?
cp $E1/m3/points_M3_r0.17.jsonl $F/tmp/edited.jsonl; printf 'X' | dd of=$F/tmp/edited.jsonl bs=1 seek=100 conv=notrunc 2>/dev/null
head -n $N0 $C17 | cmp - $F/tmp/edited.jsonl > $LG/prefix_cmp_mutate.log 2>&1; pm=$?
say "prefix check (the first $N0 lines of the r1b cache and the whole 0.2 file unchanged): cmp exits $pk $p2 (0 0 wanted); one-byte edit control exit $pm (1 wanted)"
[ $rc2 = 0 ] || { say "STOP: stage 2 exit $rc2"; exit 1; }
[ "$pk $p2 $pm" = "0 0 1" ] || { say "STOP: the prefix check did not behave"; exit 1; }
$PY -I $F/read_r25.py reading $M/count_$TAGN.json $M/count_$TAGL.json $C25 > $F/reading.txt 2>&1
say "reading: $(grep -m1 '^control' $F/reading.txt); lower quarters: $(grep -c ': resolved' $F/reading.txt) boxes resolved in total, $(grep -c ': UNRESOLVED' $F/reading.txt) unresolved; r25 done"
exit 0
}
