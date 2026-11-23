#!/bin/bash
# #1025 eval_dh170_d1975 (dh610), ordered by the coordinator: dh170's k_c 87 D 19.75 start state (blob 352107a8, record 6078a0b4) evaluated on this build with d18_hybsign.py (xfkappa's, blob e089207a, unmodified) at
# lambda 1.32 and 1.33: 2 processes of 1 thread, nice 10, each printing the record system first; plus one information process (freeze_compare.py, 1 thread, nice 10: the RK step counts of the four states, no det).
# Before the start (a failing one refuses, nothing is started): every input's blob from in_blobs.txt; the worktree 1025f clean at 505d8399; eval_compare.py selftest exit 0 and --mutate exit 1; MemAvailable at least 3 x 2.5 GB + 4 GB.
# Nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08): below 4 GiB the sampler only writes MEMALERT.txt. usage: bash lane_eval.sh [dry]
{
set -u
MODE=${1:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/eval_dh170_d1975; IN=$F/in; R=$F/run
WT=/home/nathan/Source/choptuik-large-d-1025f; W=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
D=19.75; L=$F/exits_eval.txt; MEMSTOP=4194304; CAP=28800
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC eval_dh170_d1975: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
bad=0
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$bb" ] || { say "refuse: $IN/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs.txt
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
for f in $R/eval_D19.75_p0.jsonl $R/eval_D19.75_p1.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
mkdir -p $R
( cd $IN && $PY -I eval_compare.py selftest > $F/selftest_eval_compare.log 2>&1; r0=$?; $PY -I eval_compare.py selftest --mutate > $F/selftest_eval_compare_mutate.log 2>&1; r1=$?; echo "$r0 $r1" > $F/selftest_exits_eval.txt )
read r0 r1 < $F/selftest_exits_eval.txt
[ $r0 = 0 ] && [ $r1 = 1 ] || { say "refuse: the selftests did not behave (eval_compare $r0, mutate $r1; wanted 0 1)"; bad=1; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge $(( 3 * 2500000 + 4000000 )) ] || { say "refuse: MemAvailable $av kB is below 3 x 2.5 GB + 4 GB"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked (in_blobs.txt, worktree 505d8399 clean, $PY), selftests as wanted (exits $r0 $r1); MemAvailable $av kB"
[ "$MODE" = dry ] && { say "dry run: nothing started"; exit 0; }
cd $W
say "evaluation: dh170's state on this build at 1.32 and 1.33, 2 processes of 1 thread, nice 10, cap $CAP s each; information: freeze_compare.py as a third process"
pids=()
j=0
for lam in 1.32 1.33; do
  ( nice -n 10 /usr/bin/time -v timeout -s TERM $CAP $PY -u $IN/d18_hybsign.py $IN/l1kc87dh170d1975.jsonl $IN/sol_l1kc87dh170d1975_D19.7500.npy $D $lam $R/eval_D19.75_p$j.jsonl < /dev/null > $R/eval_p$j.raw 2>&1
    echo "$(date -u '+%F %T') UTC eval $lam exit $?" >> $L ) &
  pids+=($!); j=$((j + 1))
done
( nice -n 10 /usr/bin/time -v timeout -s TERM 7200 $PY -u $IN/freeze_compare.py $IN < /dev/null > $R/freeze_compare.txt 2> $R/freeze_compare.err
  echo "$(date -u '+%F %T') UTC freeze_compare exit $?" >> $L ) &
pids+=($!)
( sleep 10; while pgrep -f 'd18_hybsign.py.*l1kc87dh170d1975|freeze_compare.py' > /dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    echo "$(date -u '+%F %T') UTC alive $(pgrep -f 'd18_hybsign.py.*l1kc87dh170d1975|freeze_compare.py' | wc -l) python-ish, RSS_kB $(ps -eo rss,cmd | awk '/(d18_hybsign.py.*l1kc87dh170d1975|freeze_compare.py)/ && !/awk|time|timeout/ {s+=$1} END {print s+0}'), MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg), points $(cat $R/eval_D19.75_p*.jsonl 2>/dev/null | wc -l)" >> $R/sampler_eval.log
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT_eval.txt
    sleep 30
  done ) &
wait "${pids[@]}"
for j in 0 1; do grep -vE 'Warning|^  [a-z]+ = |slogdet' $R/eval_p$j.raw > $R/eval_p$j.log; echo "p$j: $(grep -E 'record system' $R/eval_p$j.log | head -1 | cut -c1-140)" | tee -a $L; done
cd $IN && $PY -I eval_compare.py $R/eval_D19.75_p0.jsonl $R/eval_D19.75_p1.jsonl $IN/ref_dh170_scan_D19.75_1025.jsonl $IN/ref_linRe_D19.75_1.32.jsonl $IN/ref_linRe_D19.75_1.33.jsonl > $F/eval_compare.txt 2>&1
say "evaluation done; reading in eval_compare.txt, step counts in run/freeze_compare.txt; eval done"
exit 0
}
