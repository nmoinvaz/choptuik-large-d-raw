#!/bin/bash
{
# #1025 kc79_d19125low, the control (t5's order): d18_hybsign.py (e089207a, unmodified) on dh370's k_c 79 D 19.125 state and record, lambda 1.50, one process of 4 threads at nice 10, 3 h cap by exact pid; it must print the record
# system and dh370's hybrid sign and ln|det| at 1.50 (their scan file) to 1e-9 relative (control_check_k79.py). usage: control_k79.sh [dry]
set -u
MODE=${1:-}
F=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc79_d19125low
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python; WT=/home/nathan/Source/choptuik-large-d-1025p4; W=$WT/solver/matter
L=$F/control/exits.txt; OUT=$F/control/scan_D19.125_p0.jsonl; RAW=$F/control/control.raw
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC control: $*" | tee -a $L; }
bad=0
while read -r h f; do [ -f $F/in/$f ] && [ "$(git hash-object --no-filters $F/in/$f)" = "$h" ] || { say "refuse: in/$f missing or not blob $h"; bad=1; }; done < $F/in_blobs.txt
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
for f in $OUT $RAW; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
$PY -c "import numpy, scipy, mpmath, multidouble; multidouble.dd_logdet" || { say "refuse: $PY lacks numpy/scipy/mpmath/multidouble.dd_logdet"; bad=1; }
[ $bad = 0 ] || exit 2
[ "$MODE" = dry ] && L=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/5e14df5b-8f5b-49f8-ab79-88a302ef8042/scratchpad/dry_exits_k79control.txt
say "pins checked: in_blobs.txt, worktree 505d8399 clean; $PY; 4 threads"
[ "$MODE" = dry ] && { say "dry run: pins ok, nothing started"; exit 0; }
s0=$(date +%s)
nice -n 10 /usr/bin/time -v $PY -u $F/in/d18_hybsign.py $F/in/l1kc79dh370.jsonl $F/in/sol_l1kc79dh370_D19.1250.npy 19.125 1.50 $OUT < /dev/null > $RAW 2>&1 &
tp=$!; echo $tp > $F/control/time_pid.txt; say "control started under /usr/bin/time pid $tp (lambda 1.50 at D 19.125, k_c 79)"
while kill -0 $tp 2>/dev/null; do
  if [ $(( $(date +%s) - s0 )) -gt 10800 ]; then py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' '); say "3 h cap reached: TERM to python pid $py and time pid $tp"; kill -TERM $py $tp 2>/dev/null; break; fi
  py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' ')
  [ -n "$py" ] && [ -d /proc/$py ] && echo "$(date -u '+%T') MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo) MiB, python pid $py RSS $(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status) MiB, cputime $(ps -o cputime= -p $py | tr -d ' ')" >> $F/control/memlog.log
  sleep 30
done
wait $tp; r=$?
grep -vE 'Warning|^  [a-z]+ = |slogdet' $RAW > $F/control/control.log
say "control scan exit $r, $(( $(date +%s) - s0 )) s wall"
$PY $F/in/control_check_k79.py $F/control/control.log $OUT $F/in/ref_dh370_row_lam1.50.jsonl 1.50 > $F/control/control_check.txt 2>&1; c=$?
cat $F/control/control_check.txt | cut -c1-420 | tee -a $L
[ $c = 0 ] && say "CONTROL PASS" || say "STOP: CONTROL FAIL (control_check exit $c, scan exit $r); no scan"
exit
}
