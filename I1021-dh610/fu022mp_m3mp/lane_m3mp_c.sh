#!/bin/bash
# #1076 fu022mp_m3mp attempt 3 (dh610), the coordinator's order of 24 Nov (hc): rerun the --m3mp recount from the cache attempt 2 left (3845 lines, blob d4e4a1cc), the same command and code (argcount at f860d30e, worktree
# ~/Source/choptuik-large-d-1076b, detached), timeout 172800 s (48 h), unit i1076c, nice 10 (below the #1025 lanes). Steps (a failing one stops the lane): pins (in_blobs_c.txt, fu021's sha256, code, clean worktree, outputs absent,
# free memory >= 16 GiB); argcount --selftest (exit 0) and its three mutations (exit 1 each); no preflight (the code and python are those of attempt 2's preflight PASS and run); the recount
#   nice -n 10 timeout 172800 argcount.py --M=3 --recount=<cells> --r1=0.17 --r1b=0.2 --seed=<OUT>/m3/points_M3_r0.2.jsonl --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=12 --retry --m3mp --out=<OUT>/m3 --tag=M3_fu022mp_m3mp_r0.17
# with OMP/OPENBLAS/MKL = 1; an alert-only hourly progress line appended to README.md (cache lines, fu mp rows, the cache's last write time); after the recount (any exit) prefix_keys.py fu021's cache -> this cache (exit 0 wanted) and its
# --mutate=edit control (exit 1 wanted); on exit 0 summarize_m3mp.py. Nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08): below 4 GiB the sampler only writes MEMALERT.txt. Logs in logs/attempt3/.
{
set -u
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1021-dh610/fu022mp_m3mp; IN=$F/in; M=$F/m3; LG=$F/logs/attempt3
CODE=/home/nathan/Source/choptuik-large-d-1076b; SI=$CODE/solver/inner_stokes; PY=/home/nathan/Source/venv-i1058/bin/python
L=$LG/exits.txt; TAG=M3_fu022mp_m3mp_r0.17; MEMSTOP=4194304; CACHE=$M/points_M3_r0.17.jsonl
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC fu022mp_m3mp attempt 3: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
mkdir -p $LG $F/tmp
bad=0
while read bb f; do [ -f $F/$f ] && [ "$(blob $F/$f)" = "$bb" ] || { say "refuse: $F/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs_c.txt
[ "$(sha256sum $IN/fu021_points_M3_r0.17.jsonl | cut -d' ' -f1)" = 981f49fcef392e0e0a3a90d3863cfb8825e0e1ffbc691f0befce797401065e1d ] || { say "refuse: fu021's cache is not the SHA256SUMS_fu021 file"; bad=1; }
[ "$(git -C $CODE rev-parse --short=8 HEAD)" = f860d30e ] || { say "refuse: code is not at f860d30e"; bad=1; }
[ -z "$(git -C $CODE status --short)" ] || { say "refuse: worktree $CODE has changes"; bad=1; }
[ "$(wc -l < $CACHE)" = 3845 ] || { say "refuse: the cache is not the 3845-line cache of attempt 2's end"; bad=1; }
for f in $M/count_$TAG.json $M/leaves_$TAG.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge 16777216 ] || { say "refuse: MemAvailable $av kB is below 16 GiB"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked (in_blobs_c.txt, fu021's sha256, code f860d30e clean, cache 3845 lines blob $(blob $CACHE | cut -c1-8), outputs absent, MemAvailable $av kB, load $(cut -d' ' -f1-3 /proc/loadavg), $($PY -VV 2>&1 | head -1 | cut -c1-30), python-flint $($PY -c 'import flint; print(flint.__version__)'), mpmath $($PY -c 'import mpmath; print(mpmath.__version__)'))"
cd $SI
s=""
nice -n 10 $PY -u argcount.py --selftest > $LG/selftest_argcount.log 2>&1; s="$s $?"
for m in nosplit conj norecount; do nice -n 10 $PY -u argcount.py --selftest --mutate=$m > $LG/selftest_argcount_$m.log 2>&1; s="$s $?"; done
say "argcount selftest, nosplit, conj, norecount exits:$s (wanted 0 1 1 1)"
[ "$s" = " 0 1 1 1" ] || { say "STOP: the selftests did not behave"; exit 1; }
CMD="nice -n 10 timeout 172800 $PY -u argcount.py --M=3 --recount=$IN/cells_unresolved11.jsonl --r1=0.17 --r1b=0.2 --seed=$M/points_M3_r0.2.jsonl --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=12 --retry --m3mp --out=$M --tag=$TAG"
say "recount starts (cwd $SI, 12 processes of 1 thread, nice 10, timeout 172800 s): $CMD"
mp0=$(grep -c '"fu": "mp"' $CACHE); n0=$(wc -l < $CACHE); t0=$(date +%s)
( while sleep 60; do
    echo "$(date -u '+%F %T') UTC python $(pgrep -f "argcount.py.*$TAG" | wc -l), RSS_kB $(ps -eo rss,cmd | awk -v t="$TAG" '$0 ~ t && !/awk|timeout|nice/ {s+=$1} END {print s+0}'), MemAvailable_kB $(awk '/MemAvailable/ {print $2}' /proc/meminfo), load $(cut -d' ' -f1 /proc/loadavg), cache_lines $(wc -l < $CACHE), mp_points_logged $(grep -c 'extended precision' $LG/recount.log)" >> $LG/sampler.log
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT.txt
  done ) &
SAMP=$!
( while sleep 3600; do
    nm=$(grep -c '"fu": "mp"' $CACHE); el=$(( $(date +%s) - t0 ))
    echo "- $(date -u '+%F %H:%M') UTC (hour $(( el / 3600 )) of attempt 3, unit i1076c): cache lines $(wc -l < $CACHE) (+$(( $(wc -l < $CACHE) - n0 )) since the start), extended-precision rows (fu mp) $nm (+$(( nm - mp0 )) since the start; $(python3 -c "print(f'{($nm - $mp0) * 3600 / $el:.2f}')") per hour), newest row written $(date -u -r $CACHE '+%F %H:%M:%S') UTC, argcount processes alive $(pgrep -f "argcount.py.*$TAG" | wc -l), MemAvailable $(awk '/MemAvailable/ {print $2}' /proc/meminfo) kB (alert only)" >> $F/README.md
  done ) &
HOUR=$!
( cd $SI && $CMD > $LG/recount.log 2>&1 ); rc=$?
kill $SAMP $HOUR 2>/dev/null
say "recount exit $rc (0 wanted; 124 is the 48 h cap), wall $(( $(date +%s) - t0 )) s, cache $(wc -l < $CACHE) lines, fu mp rows $(grep -c '"fu": "mp"' $CACHE)"
$PY -I $IN/prefix_keys.py $IN/fu021_points_M3_r0.17.jsonl $CACHE > $LG/prefix_keys.log 2>&1; pk=$?
$PY -I $IN/prefix_keys.py $IN/fu021_points_M3_r0.17.jsonl $CACHE --mutate=edit > $LG/prefix_keys_mutate_edit.log 2>&1; pm=$?
say "prefix_keys fu021 -> this cache exit $pk (0 wanted); its --mutate=edit control exit $pm (1 wanted): $(tail -n 1 $LG/prefix_keys.log | cut -c1-100)"
[ $rc = 0 ] || { say "STOP: the recount exit $rc"; exit 1; }
cat $F/logs/attempt2/recount.log $LG/recount.log > $LG/recount_attempts2_3.log
$PY -I $F/summarize_m3mp.py $M/count_$TAG.json $M/leaves_$TAG.jsonl $CACHE $LG/recount_attempts2_3.log > $F/summary_m3mp.txt 2>&1
say "summary in summary_m3mp.txt; m3mp done"
exit 0
}
