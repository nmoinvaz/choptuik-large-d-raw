#!/bin/bash
# #1076 fu022mp_corner_e1 (dh610), the coordinator's order of 25 Nov (hc), option (e) level 1: the unresolved box A 3.6623456 to 3.9123456, wf 0.20654321 to 0.30654321 (its corner (3.9123456, 0.20654321) has no value, also
# not from the 0.2 start, raw 86a70082) tiled into its four quarters (in/cells_e1.jsonl from tile_cells.py), each counted as its own box by the recount code, from attempt 4's final cache (4159 lines, blob fdfc811a), argcount at 20ad2589
# (worktree ~/Source/choptuik-large-d-1076b, detached, clean), the options of the recount without --retry (the corner's rows are already in the cache and are not computed again), --procs=4, nice 10 raised to 19 by
# watch_i1088a_tiles.sh while an i1088a unit is active. Modes: dry (pins and selftests only), full. Steps (a failing one stops the lane): pins, selftests (argcount --selftest 0, nosplit, conj, norecount 1 each; tie check 0 and
# --mutate=pykey 1; tile_cells.py selftest 0 and its drop and shift mutations 1 each; read_tiles.py selftest 0 and --mutate 1), the tiling check (tile_cells.py on the parent reproduces in/cells_e1.jsonl byte for byte), the
# recount, the prefix check of the cache (the first 4159 lines unchanged: head | cmp 0; a one-byte edit of a copy: 1), read_tiles.py (reading.txt). Nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08). Logs in logs/.
{
set -u
MODE=${1:-full}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1021-dh610/fu022mp_corner_e1; MAIN=$RAW/I1021-dh610/fu022mp_m3mp; IN=$F/in; M=$F/m3; LG=$F/logs
CODE=/home/nathan/Source/choptuik-large-d-1076b; SI=$CODE/solver/inner_stokes; PY=/home/nathan/Source/venv-i1058/bin/python
L=$F/exits.txt; TAG=M3_fu022mp_corner_e1_r0.17; CACHE=$M/points_M3_r0.17.jsonl; N0=4159; CAP=43200
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC fu022mp_corner_e1: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
mkdir -p $LG $F/tmp $M
bad=0
while read bb f; do [ -f $F/$f ] && [ "$(blob $F/$f)" = "$bb" ] || { say "refuse: $F/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs.txt
while read bb f; do [ -f $f ] && [ "$(blob $f)" = "$bb" ] || { say "refuse: $f missing or not blob $bb"; bad=1; }; done < $F/in_blobs_src.txt
[ "$(git -C $CODE rev-parse --short=8 HEAD)" = 20ad2589 ] || { say "refuse: code is not at 20ad2589"; bad=1; }
[ -z "$(git -C $CODE status --short)" ] || { say "refuse: worktree $CODE has changes"; bad=1; }
[ "$(wc -l < $MAIN/m3/points_M3_r0.17.jsonl)" = $N0 ] || { say "refuse: the source cache is not $N0 lines"; bad=1; }
if [ "$MODE" = full ]; then for f in $M/count_$TAG.json $M/leaves_$TAG.jsonl $CACHE $M/points_M3_r0.2.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done; fi
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
q=""
$PY -I $F/tile_cells.py selftest > $LG/selftest_tile.log 2>&1; q="$q $?"
for m in drop shift; do $PY -I $F/tile_cells.py selftest --mutate=$m > $LG/selftest_tile_$m.log 2>&1; q="$q $?"; done
$PY -I $F/read_tiles.py selftest > $LG/selftest_read_tiles.log 2>&1; q="$q $?"
$PY -I $F/read_tiles.py selftest --mutate > $LG/selftest_read_tiles_mutate.log 2>&1; q="$q $?"
$PY -I $F/tile_cells.py $IN/cells_parent.jsonl $F/tmp/cells_e1_check.jsonl 3.9123456,0.20654321 > $LG/tile_check.log 2>&1; q="$q $?"
cmp $F/tmp/cells_e1_check.jsonl $IN/cells_e1.jsonl > $LG/tile_cmp.log 2>&1; q="$q $?"
say "argcount_tie_check.py exit $t0r (0 wanted), --mutate=pykey exit $t1r (1 wanted); tile_cells selftest, drop, shift, read_tiles selftest, --mutate, tiling check, cmp with in/cells_e1.jsonl exits:$q (wanted 0 1 1 0 1 0 0)"
[ "$t0r $t1r$q" = "0 1 0 1 1 0 1 0 0" ] || { say "STOP: a check did not behave"; exit 1; }
[ "$MODE" = full ] || { say "dry run: nothing started"; exit 0; }
cp $MAIN/m3/points_M3_r0.17.jsonl $CACHE; cp $MAIN/m3/points_M3_r0.2.jsonl $M/points_M3_r0.2.jsonl
[ "$(blob $CACHE | cut -c1-8)" = fdfc811a ] && [ "$(blob $M/points_M3_r0.2.jsonl | cut -c1-8)" = 86ffeb0e ] || { say "STOP: the copied caches are not the pinned blobs"; exit 1; }
CMD="nice -n 10 timeout $CAP $PY -u argcount.py --M=3 --recount=$IN/cells_e1.jsonl --r1=0.17 --r1b=0.2 --seed=$M/points_M3_r0.2.jsonl --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4 --m3mp --out=$M --tag=$TAG"
say "recount starts (cwd $SI, 4 processes of 1 thread, nice 10 raised to 19 by the watcher while an i1088a unit is active, timeout $CAP s): $CMD"
t0=$(date +%s)
( while sleep 60; do
    echo "$(date -u '+%F %T') UTC python $(ps -eo cmd | grep -c "[a]rgcount.py.*$TAG"), MemAvailable_kB $(awk '/MemAvailable/ {print $2}' /proc/meminfo), load $(cut -d' ' -f1 /proc/loadavg), cache_lines $(wc -l < $CACHE), mp_points_logged $(grep -c 'extended precision' $LG/recount.log)" >> $LG/sampler.log
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    [ "$avs" -lt 4194304 ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT.txt
  done ) &
SAMP=$!
( cd $SI && $CMD > $LG/recount.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
say "recount exit $rc (0 wanted; 124 is the cap), wall $(( $(date +%s) - t0 )) s, cache $(wc -l < $CACHE) lines"
head -c $(stat -c %s $MAIN/m3/points_M3_r0.17.jsonl) $CACHE | cmp - $MAIN/m3/points_M3_r0.17.jsonl > $LG/prefix_cmp.log 2>&1; pk=$?
cp $MAIN/m3/points_M3_r0.17.jsonl $F/tmp/edited.jsonl; printf 'X' | dd of=$F/tmp/edited.jsonl bs=1 seek=100 conv=notrunc 2>/dev/null
head -c $(stat -c %s $MAIN/m3/points_M3_r0.17.jsonl) $CACHE | cmp - $F/tmp/edited.jsonl > $LG/prefix_cmp_mutate.log 2>&1; pm=$?
say "prefix check (the first $N0 lines of the cache unchanged): cmp exit $pk (0 wanted); one-byte edit control exit $pm (1 wanted)"
[ $rc = 0 ] || { say "STOP: the recount exit $rc"; exit 1; }
[ "$pk $pm" = "0 1" ] || { say "STOP: the prefix check did not behave"; exit 1; }
$PY -I $F/read_tiles.py $CACHE $N0 $M/count_$TAG.json > $F/reading.txt 2>&1
say "reading: $(grep -c ': resolved' $F/reading.txt) quarters resolved, $(grep -c ': UNRESOLVED' $F/reading.txt) unresolved; $(grep '^count:' $F/reading.txt | cut -c1-200); tiles done"
exit 0
}
