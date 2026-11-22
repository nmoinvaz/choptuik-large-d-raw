#!/bin/bash
{
# #1025 kc79_d19low (dh610), the coordinator's order of 22 Nov (after the control's FAIL, 1.914e-6 against 1e-6): this machine's own spread of the k_c 79 control point: d18_hybsign.py at D 19.0, k_c 79,
# lambda 1.54 on winb's state and record, one process each at OMP, OPENBLAS, MKL = 2 and then = 4 (VECLIB and RAYON stay 1, as in the 1-thread control of control/), one after the other beside the D 19.25
# scan of ../kc71_d1925 (6 processes) and #1067 (10 threads), so that the threads in use stay at 20 or fewer (6 + 4 + 10). Then spread_read.py reads the three values against winb's row.
# d18_hybsign.py is xfkappa's, blob e089207a, unmodified. usage: bash lane_kc79_spread.sh [dry]
set -u
MODE=${1:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/kc79_d19low; IN=$F/in
WT=/home/nathan/Source/choptuik-large-d-1025f; W=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
CAP=10800
L=$F/exits_kc79_spread.txt
export PYTHONDONTWRITEBYTECODE=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc79_spread: $*" | tee -a $L; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$IN/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" \
          "$IN/sol_l1kc79W19m1025_D19.0000.npy 3a3b1999e1754c9c2e138ebf4d80f33a366abf3b" "$IN/l1kc79W19m1025.jsonl 3603895c432fc9b0319742c91a7158096a4e5053" \
          "$IN/ref_winb_scan_kc79_D19_1025.jsonl 321fb621c68f885708f6c995af1b2518e7cd2348"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
for f in $F/control_t2/scan_D19.0_p0.jsonl $F/control_t4/scan_D19.0_p0.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ -f $F/control/scan_D19.0_p0.jsonl ] && [ -f $F/control/control.log ] || { say "refuse: the 1-thread control files are missing"; bad=1; }
( cd $F && $PY spread_read.py selftest > $F/selftest_spread_read.log 2>&1; r0=$?
  $PY spread_read.py selftest --mutate > $F/selftest_spread_read_mutate.log 2>&1; r1=$?
  echo "$r0 $r1" > $F/selftest_spread_exits.txt )
read r0 r1 < $F/selftest_spread_exits.txt
[ $r0 = 0 ] && [ $r1 = 1 ] || { say "refuse: spread_read selftest did not behave ($r0, its mutate $r1; wanted 0 1)"; bad=1; }
MAXRSS=$(awk '/Maximum resident set size/ {print $NF}' $F/control/control.raw); av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ -n "$MAXRSS" ] && [ "$av" -ge $(( 2 * MAXRSS + 4000000 )) ] || { say "refuse: MemAvailable $av kB below 2 x the 1-thread control's max RSS (${MAXRSS:-?} kB) + 4 GB"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked, worktree 505d8399 clean, spread_read selftest as wanted ($r0 $r1), MemAvailable $av kB, 1-thread control max RSS $MAXRSS kB; runs: 2 threads, then 4 threads"
[ "$MODE" = dry ] && { say "dry run: nothing started"; exit 0; }
cd $W
for N in 2 4; do
  D=$F/control_t$N; mkdir -p $D
  export OMP_NUM_THREADS=$N OPENBLAS_NUM_THREADS=$N MKL_NUM_THREADS=$N
  say "control at OMP/OPENBLAS/MKL = $N: D 19.0, k_c 79, lambda 1.54, 1 process, cap $CAP s by exact pid"
  t0=$(date +%s)
  ( while sleep 30; do echo "$(date -u '+%F %T') UTC $(ps -eo pid,nlwp,rss,pcpu,args | awk '/d18_hybsign.py.*control_t'$N'/ && !/awk|time|timeout/ {print "pid " $1 " nlwp " $2 " rss_kB " $3 " pcpu " $4}')" >> $D/sampler.log; done ) &
  smp=$!
  nice -n 10 /usr/bin/time -v timeout -s TERM $CAP $PY -u $IN/d18_hybsign.py $IN/l1kc79W19m1025.jsonl $IN/sol_l1kc79W19m1025_D19.0000.npy 19.0 1.54 $D/scan_D19.0_p0.jsonl < /dev/null > $D/control.raw 2>&1
  rc=$?; kill $smp 2>/dev/null; wait $smp 2>/dev/null
  grep -vE 'Warning|^  [a-z]+ = |slogdet' $D/control.raw > $D/control.log
  say "control at $N threads: exit $rc, wall $(( $(date +%s) - t0 )) s, max RSS $(awk '/Maximum resident set size/ {print $NF}' $D/control.raw) kB, max nlwp $(awk '/nlwp/ {for (i=1;i<=NF;i++) if ($i=="nlwp" && $(i+1)>m) m=$(i+1)} END {print m+0}' $D/sampler.log)"
  [ $rc = 0 ] || { say "STOP: the $N-thread control did not end cleanly (exit $rc)"; exit 1; }
done
{ echo "=== spread_read.py (1, 2, 4 threads against winb's row)"; $PY $F/spread_read.py $F/control/scan_D19.0_p0.jsonl $F/control_t2/scan_D19.0_p0.jsonl $F/control_t4/scan_D19.0_p0.jsonl \
    $F/control/control.log $F/control_t2/control.log $F/control_t4/control.log $IN/ref_winb_scan_kc79_D19_1025.jsonl 1.54; echo "spread_read exit $?"; } > $F/spread_read.txt 2>&1
cat $F/spread_read.txt | tee -a $L
say "spread done; reading in spread_read.txt"
exit 0
}
