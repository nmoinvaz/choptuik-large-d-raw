#!/bin/bash
# #1076 fu022mp_m3mp (dh610), the coordinator's order of 23 Nov (the #1076 comment 7096737456): the --m3mp recount of #1021's 17 unresolved leaves on fu022mp pass 3's cache, argcount at feat/inner-mp 58108b67 (worktree
# ~/Source/choptuik-large-d-1076, detached). Steps (a failing one stops the lane and nothing later runs): pins (in_blobs.txt, code, clean worktree, fu021's sha256, outputs absent, free memory); argcount --selftest (exit 0) and its three
# mutations (exit 1 each); the preflight m3mp_check.py on the pass 2 cache of raw efed06f1 with --procs=2 (exit 0 and "m3mp check: PASS"); the recount, as ordered:
#   nice -n 10 timeout 24h argcount.py --M=3 --recount=<cells> --r1=0.17 --r1b=0.2 --seed=<OUT>/m3/points_M3_r0.2.jsonl --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=12 --retry --m3mp --out=<OUT>/m3 --tag=M3_fu022mp_m3mp_r0.17
# with OMP/OPENBLAS/MKL = 1; then prefix_keys.py fu021's cache -> this cache (exit 0 wanted; its --mutate=edit exit 1 wanted); then summarize_m3mp.py. Memory: refuses to start with less than 16 GiB available; nothing is stopped or terminated for
# memory (Nathan's rule of 2026-11-08): below 4 GiB the sampler only writes MEMALERT.txt. usage: bash lane_m3mp.sh
{
set -u
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1021-dh610/fu022mp_m3mp; IN=$F/in; M=$F/m3; LG=$F/logs
CODE=/home/nathan/Source/choptuik-large-d-1076; SI=$CODE/solver/inner_stokes; PY=/home/nathan/Source/venv-i1058/bin/python
L=$LG/exits.txt; TAG=M3_fu022mp_m3mp_r0.17; MEMSTOP=4194304
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC fu022mp_m3mp: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
mkdir -p $LG $F/tmp
bad=0
while read bb f; do [ -f $F/$f ] && [ "$(blob $F/$f)" = "$bb" ] || { say "refuse: $F/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs.txt
[ "$(sha256sum $IN/fu021_points_M3_r0.17.jsonl | cut -d' ' -f1)" = 981f49fcef392e0e0a3a90d3863cfb8825e0e1ffbc691f0befce797401065e1d ] || { say "refuse: fu021's cache is not the SHA256SUMS_fu021 file"; bad=1; }
[ "$(git -C $CODE rev-parse HEAD)" = 58108b67 ] || [ "$(git -C $CODE rev-parse --short=8 HEAD)" = 58108b67 ] || { say "refuse: code is not at 58108b67"; bad=1; }
[ -z "$(git -C $CODE status --short)" ] || { say "refuse: worktree $CODE has changes"; bad=1; }
[ "$(wc -l < $M/points_M3_r0.17.jsonl)" = 3605 ] || { say "refuse: the cache is not the 3605-line pass 3 cache"; bad=1; }
for f in $M/count_$TAG.json $M/leaves_$TAG.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge 16777216 ] || { say "refuse: MemAvailable $av kB is below 16 GiB"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked (in_blobs.txt, fu021's sha256, code 58108b67 clean, cache 3605 lines, outputs absent, MemAvailable $av kB, load $(cut -d' ' -f1-3 /proc/loadavg), $($PY -VV 2>&1 | head -1 | cut -c1-30), python-flint $($PY -c 'import flint; print(flint.__version__)'), mpmath $($PY -c 'import mpmath; print(mpmath.__version__)'))"
cd $SI
s=""
nice -n 10 $PY -u argcount.py --selftest > $LG/selftest_argcount.log 2>&1; s="$s $?"
for m in nosplit conj norecount; do nice -n 10 $PY -u argcount.py --selftest --mutate=$m > $LG/selftest_argcount_$m.log 2>&1; s="$s $?"; done
say "argcount selftest, nosplit, conj, norecount exits:$s (wanted 0 1 1 1)"
[ "$s" = " 0 1 1 1" ] || { say "STOP: the selftests did not behave"; exit 1; }
say "preflight: m3mp_check.py on the pass 2 cache (raw efed06f1, blob $(blob $IN/points_M3_r0.17_efed06f1.jsonl | cut -c1-8)) with --procs=2"
TMPDIR=$F/tmp nice -n 10 $PY -u m3mp_check.py $IN/points_M3_r0.17_efed06f1.jsonl --procs=2 > $LG/m3mp_check.log 2>&1; rc=$?
say "preflight exit $rc: $(grep -E 'm3mp check' $LG/m3mp_check.log | cut -c1-120)"
if [ $rc != 0 ] || ! grep -q 'm3mp check: PASS' $LG/m3mp_check.log; then say "STOP: the preflight did not exit 0 with PASS; the recount is not started"; exit 1; fi
CMD="nice -n 10 timeout 24h $PY -u argcount.py --M=3 --recount=$IN/cells_unresolved11.jsonl --r1=0.17 --r1b=0.2 --seed=$M/points_M3_r0.2.jsonl --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=12 --retry --m3mp --out=$M --tag=$TAG"
say "recount starts (cwd $SI, 12 processes of 1 thread, nice 10, timeout 24h): $CMD"
( while sleep 60; do
    echo "$(date -u '+%F %T') UTC python $(pgrep -f "argcount.py.*$TAG" | wc -l), RSS_kB $(ps -eo rss,cmd | awk -v t="$TAG" '$0 ~ t && !/awk|timeout|nice/ {s+=$1} END {print s+0}'), MemAvailable_kB $(awk '/MemAvailable/ {print $2}' /proc/meminfo), load $(cut -d' ' -f1 /proc/loadavg), cache_lines $(wc -l < $M/points_M3_r0.17.jsonl), mp_points_logged $(grep -c 'extended precision' $LG/recount.log)" >> $LG/sampler.log
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT.txt
  done ) &
SAMP=$!
t0=$(date +%s)
( cd $SI && $CMD > $LG/recount.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
say "recount exit $rc (0 wanted; 124 is the 24 h cap), wall $(( $(date +%s) - t0 )) s, cache $(wc -l < $M/points_M3_r0.17.jsonl) lines"
[ $rc = 0 ] || { say "STOP: the recount exit $rc"; exit 1; }
$PY -I $IN/prefix_keys.py $IN/fu021_points_M3_r0.17.jsonl $M/points_M3_r0.17.jsonl > $LG/prefix_keys.log 2>&1; pk=$?
$PY -I $IN/prefix_keys.py $IN/fu021_points_M3_r0.17.jsonl $M/points_M3_r0.17.jsonl --mutate=edit > $LG/prefix_keys_mutate_edit.log 2>&1; pm=$?
say "prefix_keys fu021 -> this cache exit $pk (0 wanted); its --mutate=edit control exit $pm (1 wanted): $(tail -n 1 $LG/prefix_keys.log | cut -c1-100)"
$PY -I $F/summarize_m3mp.py $M/count_$TAG.json $M/leaves_$TAG.jsonl $M/points_M3_r0.17.jsonl $LG/recount.log > $F/summary_m3mp.txt 2>&1
say "summary in summary_m3mp.txt; m3mp done"
exit 0
}
