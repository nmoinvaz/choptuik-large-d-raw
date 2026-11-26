#!/bin/bash
# #1076 fu022mp_jump_width (dh610), the coordinator's order of 25 Nov (hc): "Run (a) now, the 32 two-seed solves for the width of the two-valued region, nice 19, registered first." width_jump.py: 18 locations (A = 3.7873456 + {-0.03125,
# -0.016, -0.004, -0.001, 0, +0.001, +0.004, +0.016, +0.03125} on the rows wf 0.23154321 and 0.24404321; the offset 0 is the repeat check), each solved from two forced seeds (the L and the R root that
# ../fu022mp_jump_map/ found at that row on A = 3.7873456): 36 solves, 32 of them at the 16 offsets other than 0; argcount.py at 20ad2589 imported unchanged from the worktree, the recount's options (m3fix, bounds, no extended precision), r1 0.249, 4 processes of 1 thread, nice 10
# raised to 19 by watch_i1088a_width.sh while an i1088a unit is active. Modes: dry (pins and selftests only), full. The reading (read_width.py): its repeat check FIRES (exit 1) if the offset-0 solves do not reproduce the map's two roots
# within 1e-4 or are not two roots: the lane stops and reports. Nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08). Logs in logs/.
{
set -u
MODE=${1:-full}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1021-dh610/fu022mp_jump_width; MAP=$RAW/I1021-dh610/fu022mp_jump_map; M=$F/m3; LG=$F/logs
CODE=/home/nathan/Source/choptuik-large-d-1076b; SI=$CODE/solver/inner_stokes; PY=/home/nathan/Source/venv-i1058/bin/python
L=$F/exits.txt; CAP=7200
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC fu022mp_jump_width: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
mkdir -p $LG $M
bad=0
while read bb f; do [ -f $F/$f ] && [ "$(blob $F/$f)" = "$bb" ] || { say "refuse: $F/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs.txt
while read bb f; do [ -f $f ] && [ "$(blob $f)" = "$bb" ] || { say "refuse: $f missing or not blob $bb"; bad=1; }; done < $F/in_blobs_src.txt
[ "$(git -C $CODE rev-parse --short=8 HEAD)" = 20ad2589 ] || { say "refuse: code is not at 20ad2589"; bad=1; }
[ -z "$(git -C $CODE status --short)" ] || { say "refuse: worktree $CODE has changes"; bad=1; }
if [ "$MODE" = full ]; then for f in $M/points_M3_r0.249_L.jsonl $M/points_M3_r0.249_R.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done; fi
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge 16777216 ] || { say "refuse: MemAvailable $av kB is below 16 GiB"; bad=1; }
[ $bad = 0 ] || exit 2
say "start (mode $MODE; pins checked: in_blobs.txt, in_blobs_src.txt, code 20ad2589 clean, MemAvailable $av kB, load $(cut -d' ' -f1-3 /proc/loadavg), $($PY -VV 2>&1 | head -1 | cut -c1-30), python-flint $($PY -c 'import flint; print(flint.__version__)'), mpmath $($PY -c 'import mpmath; print(mpmath.__version__)'))"
cd $SI
s=""
nice -n 19 $PY -u argcount.py --selftest > $LG/selftest_argcount.log 2>&1; s="$s $?"
nice -n 19 $PY -u argcount.py --selftest --mutate=starts > $LG/selftest_argcount_starts.log 2>&1; s="$s $?"
say "argcount selftest, --mutate=starts exits:$s (wanted 0 1)"
[ "$s" = " 0 1" ] || { say "STOP: the selftests did not behave"; exit 1; }
nice -n 19 $PY $F/width_jump.py selftest > $LG/selftest_width.log 2>&1; m0=$?
nice -n 19 $PY $F/width_jump.py selftest --mutate > $LG/selftest_width_mutate.log 2>&1; m1=$?
$PY -I $F/read_width.py selftest > $LG/selftest_read_width.log 2>&1; r0=$?
$PY -I $F/read_width.py selftest --mutate > $LG/selftest_read_width_mutate.log 2>&1; r1=$?
say "width_jump.py selftest exit $m0 (0 wanted), --mutate exit $m1 (1 wanted); read_width.py selftest exit $r0 (0 wanted), --mutate exit $r1 (1 wanted)"
[ "$m0 $m1 $r0 $r1" = "0 1 0 1" ] || { say "STOP: a check did not behave"; exit 1; }
[ "$(git -C $CODE status --short)" = "" ] || { say "STOP: the selftests changed the worktree"; exit 1; }
[ "$MODE" = full ] || { say "dry run: nothing started"; exit 0; }
t0=$(date +%s)
say "width map starts (cwd $SI, 2 passes of 18 locations, 4 processes of 1 thread, nice 10 raised to 19 by the watcher while an i1088a unit is active, timeout $CAP s): nice -n 10 timeout $CAP $PY -u $F/width_jump.py run $MAP $M"
nice -n 10 timeout $CAP $PY -u $F/width_jump.py run $MAP $M > $LG/width.log 2>&1; rc=$?
say "width map exit $rc (0 wanted; 124 is the cap), wall $(( $(date +%s) - t0 )) s, rows L $(wc -l < $M/points_M3_r0.249_L.jsonl), R $(wc -l < $M/points_M3_r0.249_R.jsonl)"
[ $rc = 0 ] || { say "STOP: width map exit $rc"; exit 1; }
while read bb f; do [ "$(blob $f)" = "$bb" ] || { say "STOP: source $f changed"; exit 1; }; done < $F/in_blobs_src.txt
$PY -I $F/read_width.py reading $M/points_M3_r0.249_L.jsonl $M/points_M3_r0.249_R.jsonl $MAP/m3/points_M3_r0.249_L.jsonl $MAP/m3/points_M3_r0.249_R.jsonl > $F/reading.txt 2>&1; rr=$?
say "reading: exit $rr (0 PASS, 1 the repeat check FIRES); $(grep -A2 '^two-valued width' $F/reading.txt | tr '\n' ' ')"
[ $rr = 0 ] || { say "STOP: the repeat check fires (the offset-0 solves do not reproduce the map's two roots); the work stops and is reported"; exit 1; }
say "width done"
exit 0
}
