#!/bin/bash
# #1076 fu022mp_jump_map (dh610), the coordinator's order of 25 Nov (hc): "the float64 map of F_3 around (3.7873456, 0.239871): about 25 points, 4 procs, nice 19 under the yield watcher, registered first (a branch-switch line
# of the inner solve, crossing the edge, vs an isolated jump). Report where the line runs through the lower half; post on #1076." map_jump.py: 27 locations (a 5 x 5 grid of the lower half and the gap's two points) in three passes
# (STD = the recount's seed rule from a copy of its cache, L and R = the seed forced to the F_3 of the gap's lower and upper point), argcount.py at 20ad2589 imported unchanged from the worktree, the recount's options (m3fix, bounds,
# no extended precision), r1 0.249, 4 processes of 1 thread, nice 10 raised to 19 by watch_i1088a_map.sh while an i1088a unit is active. Modes: dry (pins and selftests only), full. Then the pin check again, the reading (read_map.py:
# its repeat check FIRES (exit 1) if the gap's own-branch seeds do not reproduce the recount's F_3: the lane stops and reports). Nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08). Logs in logs/.
{
set -u
MODE=${1:-full}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1021-dh610/fu022mp_jump_map; R249=$RAW/I1021-dh610/fu022mp_corner_r249; M=$F/m3; LG=$F/logs
CODE=/home/nathan/Source/choptuik-large-d-1076b; SI=$CODE/solver/inner_stokes; PY=/home/nathan/Source/venv-i1058/bin/python
L=$F/exits.txt; SRC=$R249/m3/points_M3_r0.249.jsonl; S02=$R249/m3/points_M3_r0.2.jsonl; NSRC=231; CAP=14400
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC fu022mp_jump_map: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
mkdir -p $LG $M
bad=0
while read bb f; do [ -f $F/$f ] && [ "$(blob $F/$f)" = "$bb" ] || { say "refuse: $F/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs.txt
while read bb f; do [ -f $f ] && [ "$(blob $f)" = "$bb" ] || { say "refuse: $f missing or not blob $bb"; bad=1; }; done < $F/in_blobs_src.txt
[ "$(git -C $CODE rev-parse --short=8 HEAD)" = 20ad2589 ] || { say "refuse: code is not at 20ad2589"; bad=1; }
[ -z "$(git -C $CODE status --short)" ] || { say "refuse: worktree $CODE has changes"; bad=1; }
[ "$(wc -l < $SRC)" = $NSRC ] || { say "refuse: the source cache is not $NSRC lines"; bad=1; }
if [ "$MODE" = full ]; then for f in $M/points_M3_r0.249_std.jsonl $M/points_M3_r0.249_L.jsonl $M/points_M3_r0.249_R.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done; fi
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge 16777216 ] || { say "refuse: MemAvailable $av kB is below 16 GiB"; bad=1; }
[ $bad = 0 ] || exit 2
say "start (mode $MODE; pins checked: in_blobs.txt, in_blobs_src.txt, code 20ad2589 clean, source cache $NSRC lines, MemAvailable $av kB, load $(cut -d' ' -f1-3 /proc/loadavg), $($PY -VV 2>&1 | head -1 | cut -c1-30), python-flint $($PY -c 'import flint; print(flint.__version__)'), mpmath $($PY -c 'import mpmath; print(mpmath.__version__)'))"
cd $SI
s=""
nice -n 19 $PY -u argcount.py --selftest > $LG/selftest_argcount.log 2>&1; s="$s $?"
nice -n 19 $PY -u argcount.py --selftest --mutate=starts > $LG/selftest_argcount_starts.log 2>&1; s="$s $?"
say "argcount selftest, --mutate=starts exits:$s (wanted 0 1)"
[ "$s" = " 0 1" ] || { say "STOP: the selftests did not behave"; exit 1; }
nice -n 19 $PY $F/map_jump.py selftest > $LG/selftest_map.log 2>&1; m0=$?
nice -n 19 $PY $F/map_jump.py selftest --mutate > $LG/selftest_map_mutate.log 2>&1; m1=$?
$PY -I $F/read_map.py selftest > $LG/selftest_read_map.log 2>&1; r0=$?
$PY -I $F/read_map.py selftest --mutate > $LG/selftest_read_map_mutate.log 2>&1; r1=$?
say "map_jump.py selftest exit $m0 (0 wanted), --mutate exit $m1 (1 wanted); read_map.py selftest exit $r0 (0 wanted), --mutate exit $r1 (1 wanted)"
[ "$m0 $m1 $r0 $r1" = "0 1 0 1" ] || { say "STOP: a check did not behave"; exit 1; }
[ "$(git -C $CODE status --short)" = "" ] || { say "STOP: the selftests changed the worktree"; exit 1; }
[ "$MODE" = full ] || { say "dry run: nothing started"; exit 0; }
t0=$(date +%s)
say "map starts (cwd $SI, 3 passes of 27 locations, 4 processes of 1 thread, nice 10 raised to 19 by the watcher while an i1088a unit is active, timeout $CAP s): nice -n 10 timeout $CAP $PY -u $F/map_jump.py run $SRC $S02 $M"
nice -n 10 timeout $CAP $PY -u $F/map_jump.py run $SRC $S02 $M > $LG/map.log 2>&1; rc=$?
say "map exit $rc (0 wanted; 124 is the cap), wall $(( $(date +%s) - t0 )) s, rows std $(wc -l < $M/points_M3_r0.249_std.jsonl), L $(wc -l < $M/points_M3_r0.249_L.jsonl), R $(wc -l < $M/points_M3_r0.249_R.jsonl)"
[ $rc = 0 ] || { say "STOP: map exit $rc"; exit 1; }
for f in $SRC $S02; do :; done
[ "$(wc -l < $SRC)" = $NSRC ] && [ "$(blob $SRC | cut -c1-8)" = "$(awk -v f=$SRC '$2==f {print substr($1,1,8)}' $F/in_blobs_src.txt)" ] || { say "STOP: the source cache changed"; exit 1; }
head -n $NSRC $M/points_M3_r0.249_std.jsonl | cmp - $SRC > $LG/prefix_cmp.log 2>&1; pk=$?
cp $SRC $F/tmp_edited.jsonl; printf 'X' | dd of=$F/tmp_edited.jsonl bs=1 seek=100 conv=notrunc 2>/dev/null
head -n $NSRC $M/points_M3_r0.249_std.jsonl | cmp - $F/tmp_edited.jsonl > $LG/prefix_cmp_mutate.log 2>&1; pm=$?
say "prefix check (the first $NSRC lines of the STD cache are the recount's): cmp exit $pk (0 wanted); one-byte edit control exit $pm (1 wanted)"
[ "$pk $pm" = "0 1" ] || { say "STOP: the prefix check did not behave"; exit 1; }
$PY -I $F/read_map.py reading $SRC $M/points_M3_r0.249_std.jsonl $M/points_M3_r0.249_L.jsonl $M/points_M3_r0.249_R.jsonl > $F/reading.txt 2>&1; rr=$?
say "reading: exit $rr (0 PASS, 1 the repeat check FIRES); $(grep -m1 '^repeat check' $F/reading.txt); $(grep -m1 '^classes of' $F/reading.txt)"
[ $rr = 0 ] || { say "STOP: the repeat check fires (a gap point's own-branch seed does not reproduce the recount's F_3); the work stops and is reported"; exit 1; }
say "map done"
exit 0
}
