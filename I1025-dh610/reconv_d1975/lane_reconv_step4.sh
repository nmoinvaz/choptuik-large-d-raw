#!/bin/bash
# #1025 reconv_d1975 (dh610) step 4, ordered by the coordinator after the re-convergence result: d18_hybsign.py (xfkappa's, blob e089207a, unmodified) on both re-converged states, linRe and macRe, at
# lambda 1.32, 1.33, 1.34 (D 19.75): 6 processes of 1 thread, nice 10, each printing the record system; then the reader (dh170's read_lower.py, as in ../kc95_d1975) on scan/lin and scan/mac, and step4_roots.py.
# Before the scan (a failing one stops the lane, nothing is started): every input's blob from in_blobs_step4.txt; the worktree 1025f clean at 505d8399; the reader's selftests exit 0 1 1 0; step4_roots.py selftest exits 0
# and its --mutate exits 1; the reader on the reference rows gives dh170's 1.325410 and macm3's 1.338993 (step4_roots.py check). Free memory: refuses a start with less than 6 x 2.5 GB + 4 GB available; nothing is
# stopped or terminated for memory (Nathan's rule of 2026-11-08): below 4 GiB the sampler only writes MEMALERT_step4.txt. usage: bash lane_reconv_step4.sh [dry]
{
set -u
MODE=${1:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/reconv_d1975; IN=$F/in; S=$F/scan
WT=/home/nathan/Source/choptuik-large-d-1025f; W=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
D=19.75; L=$F/exits_step4.txt; MEMSTOP=4194304; CAP=28800
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC reconv_d1975 step 4: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
bad=0
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$bb" ] || { say "refuse: $IN/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs_step4.txt
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
for f in $S/lin/scan_D19.75_p0.jsonl $S/mac/scan_D19.75_p0.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
mkdir -p $S/lin $S/mac $F/refcheck/dh $F/refcheck/mac
export D18_DIR=$IN
( cd $IN && $PY -W ignore read_lower.py selftest > $F/selftest_read_lower.log 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $F/selftest_read_lower_mutate_shift.log 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $F/selftest_read_lower_mutate_round2.log 2>&1; r2=$?
  $PY repeat_check.py selftest > $F/selftest_repeat_check.log 2>&1; r3=$?
  $PY -I step4_roots.py selftest > $F/selftest_step4_roots.log 2>&1; r4=$?
  $PY -I step4_roots.py selftest --mutate > $F/selftest_step4_roots_mutate.log 2>&1; r5=$?
  echo "$r0 $r1 $r2 $r3 $r4 $r5" > $F/selftest_exits_step4.txt )
read r0 r1 r2 r3 r4 r5 < $F/selftest_exits_step4.txt
[ $r0 = 0 ] && [ $r1 = 1 ] && [ $r2 = 1 ] && [ $r3 = 0 ] && [ $r4 = 0 ] && [ $r5 = 1 ] || { say "refuse: the selftests did not behave (read_lower $r0, mutate shift $r1, mutate round2 $r2, repeat_check $r3, step4_roots $r4, step4_roots mutate $r5; wanted 0 1 1 0 0 1)"; bad=1; }
# the reader on the reference rows
cp $IN/ref_dh170_scan_D19.75_1025.jsonl $F/refcheck/dh/scan_ref_p0.jsonl; cp $IN/ref_macm3_scan_D19.75_1025.jsonl $F/refcheck/mac/scan_ref_p0.jsonl
( cd $IN && $PY -W ignore read_lower.py $F/refcheck/dh 1.32 1.34 > $F/refcheck/read_dh.txt 2>&1; $PY -W ignore read_lower.py $F/refcheck/mac 1.32 1.34 > $F/refcheck/read_mac.txt 2>&1
  $PY -I step4_roots.py check $F/refcheck/read_dh.txt $F/refcheck/read_mac.txt > $F/refcheck/check.txt 2>&1; echo $? > $F/refcheck/check_exit.txt )
rc=$(cat $F/refcheck/check_exit.txt); [ "$rc" = 0 ] || { say "refuse: the reader on the reference rows did not give 1.325410 and 1.338993 ($(cut -c1-200 $F/refcheck/check.txt))"; bad=1; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge $(( 6 * 2500000 + 4000000 )) ] || { say "refuse: MemAvailable $av kB is below 6 x 2.5 GB + 4 GB"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked (in_blobs_step4.txt, worktree 505d8399 clean, $PY), selftests as wanted (exits $r0 $r1 $r2 $r3 $r4 $r5), the reader on the reference rows: $(cut -c1-60 $F/refcheck/check.txt); MemAvailable $av kB"
[ "$MODE" = dry ] && { say "dry run: nothing started"; exit 0; }
cd $W
say "scan: linRe and macRe at 1.32, 1.33, 1.34, 6 processes of 1 thread, nice 10, cap $CAP s each by exact pid"
pids=()
for t in lin mac; do
  case $t in lin) TG=l1kc87linRe;; mac) TG=l1kc87macRe;; esac
  j=0
  for lam in 1.32 1.33 1.34; do
    ( nice -n 10 /usr/bin/time -v timeout -s TERM $CAP $PY -u $IN/d18_hybsign.py $IN/$TG.jsonl $IN/sol_${TG}_D19.7500.npy $D $lam $S/$t/scan_D19.75_p$j.jsonl < /dev/null > $S/$t/scan_p$j.raw 2>&1
      echo "$(date -u '+%F %T') UTC step 4 $t $lam exit $?" >> $L ) &
    pids+=($!); j=$((j + 1))
  done
done
( sleep 10; while pgrep -f 'd18_hybsign.py.*l1kc87(lin|mac)Re' > /dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    echo "$(date -u '+%F %T') UTC alive $(pgrep -f 'd18_hybsign.py.*l1kc87(lin|mac)Re' | wc -l) python, RSS_kB $(ps -eo rss,cmd | awk '/d18_hybsign.py.*l1kc87(lin|mac)Re/ && !/awk|time|timeout/ {s+=$1} END {print s+0}'), MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg), points $(cat $S/lin/scan_D19.75_p*.jsonl $S/mac/scan_D19.75_p*.jsonl 2>/dev/null | wc -l)" >> $S/sampler_step4.log
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT_step4.txt
    sleep 30
  done ) &
wait "${pids[@]}"
for t in lin mac; do for j in 0 1 2; do
  grep -vE 'Warning|^  [a-z]+ = |slogdet' $S/$t/scan_p$j.raw > $S/$t/scan_p$j.log
  echo "$t p$j: $(grep -E 'record system' $S/$t/scan_p$j.log | head -1 | cut -c1-120)" | tee -a $L
done; done
cat $S/lin/scan_D19.75_p*.jsonl $S/mac/scan_D19.75_p*.jsonl > $S/rc_all_rows.jsonl
cd $IN
for t in lin mac; do { echo "=== read_lower.py $S/$t 1.32 1.34"; $PY -W ignore read_lower.py $S/$t 1.32 1.34; echo "read_lower exit $?"; } > $F/read_lower_$t.txt 2>&1; done
DZ=$($PY -I -c "import json; print(json.load(open('$F/cond/f_lin_mac.json'))['dz'])")
$PY -I step4_roots.py result $F/read_lower_lin.txt $F/read_lower_mac.txt $DZ > $F/step4_roots.txt 2>&1
say "scan done; readings in read_lower_lin.txt, read_lower_mac.txt, step4_roots.txt; step 4 done"
exit 0
}
