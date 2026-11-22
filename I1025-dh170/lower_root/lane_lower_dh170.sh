#!/bin/bash
{
# #1025 lower_root: the lower root's track at k_c 63 (the coordinator's hc, 22 Nov): the hybrid sign scan d18_hybsign.py (e089207a: the record system check first, the hybrid sign, p4_hybrid's 1e-15 noise test
# on blocks 0-11 with 2 seeds, the float64 sign beside) on one k_c 63 state at one D. usage: lane_lower_dh170.sh A|B [dry]   (the two lanes run side by side, 4 threads each, nice 10, systemd user units)
#   A: D 18.5, the Mac's k_c 63 state and record, lambda 1.20 to 1.54 at 0.02 (18 values) plus a repeat of 1.30 at the end (19 evaluations)
#   B: D 19.03125, dh370's k_c 63 state and record, lambda 1.47 to 1.55 at 0.005 (17 values) plus a repeat of 1.510 at the end (18 evaluations)
set -u
X=${1:?A or B}; MODE=${2:-}
F=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/lower_root
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python; WT=/home/nathan/Source/choptuik-large-d-1025p4; W=$WT/solver/matter
case $X in
  A) DD=18.5;     ST=$F/in/sol_l1kc63Wm1025_D18.5000.npy;   STH=33c1a58b82229d55661cbd5e79d2c1fce0c0717c; REC=$F/in/l1kc63Wm1025.jsonl; RECH=08f4dbf367edba55814e5cf989ccd32a9a5dbe67
     LAMS=$($PY -c 'print(",".join([f"{1.20 + 0.02 * i:.2f}" for i in range(18)] + ["1.30"]))'); NEV=19;;
  B) DD=19.03125; ST=$F/in/sol_l1kc63dh370_D19.031250.npy;  STH=53f3bd299d3162737003527309ba6a2eb78cc1c5; REC=$F/in/l1kc63dh370.jsonl;   RECH=168213b0e595b5f30a3376f479aa12157964141e
     LAMS=$($PY -c 'print(",".join([f"{1.47 + 0.005 * i:.3f}" for i in range(17)] + ["1.510"]))'); NEV=18;;
  *) echo "usage: $0 A|B [dry]"; exit 9;;
esac
LD=$F/lane$X; mkdir -p $LD
HS=$F/d18_hybsign.py; SCAN=$LD/scan_D${DD}_p0.jsonl; L=$LD/exits.txt; RAW=$LD/scan.raw
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC lane $X (D $DD): $*" | tee -a $L; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$ST $STH" "$REC $RECH" "$HS e089207a61fbd98614716abd309571cbc4888db2"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
for f in $SCAN $RAW; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
$PY -c "import numpy, scipy, mpmath, multidouble; multidouble.dd_logdet" || { say "refuse: $PY lacks numpy/scipy/mpmath/multidouble.dd_logdet"; bad=1; }
[ $bad = 0 ] || exit 2
[ "$MODE" = dry ] && L=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/5e14df5b-8f5b-49f8-ab79-88a302ef8042/scratchpad/dry_exits_lane$X.txt
say "pins checked: state $(basename $ST) $STH, record $(basename $REC) $RECH, d18_hybsign e089207a, worktree 505d8399 clean; $PY; 4 threads"
[ "$MODE" = dry ] && { say "dry run: pins ok, lambda list $LAMS ($NEV evaluations), nothing started"; exit 0; }
cd $W
say "1. planted control: ell_ddm.py selftest (must PASS), then --mutate=slices (must FAIL), 1800 s each"
timeout 1800 nice -n 10 $PY -u ell_ddm.py selftest < /dev/null > $LD/ell_ddm_selftest.log 2>&1; r1=$?
timeout 1800 nice -n 10 $PY -u ell_ddm.py selftest --mutate=slices < /dev/null >> $LD/ell_ddm_selftest.log 2>&1; r2=$?
grep -E '^selftest:' $LD/ell_ddm_selftest.log | tee -a $L
[ $r1 = 0 ] && [ $r2 = 1 ] || { say "STOP: the planted control did not behave (selftest exit $r1, --mutate=slices exit $r2)"; exit; }
say "2. the scan at D $DD: lam $LAMS ($NEV evaluations; the system check is the script's first line, exit 3 if it is not the record system); 8 h cap by exact pid"
s0=$(date +%s)
nice -n 10 /usr/bin/time -v $PY -u $HS $REC $ST $DD $LAMS $SCAN < /dev/null > $RAW 2>&1 &
tp=$!; echo $tp > $LD/time_pid.txt; say "scan started under /usr/bin/time pid $tp"
n=0
while kill -0 $tp 2>/dev/null; do
  if [ $(( $(date +%s) - s0 )) -gt 28800 ]; then
    py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' '); say "8 h cap reached: TERM to python pid $py and time pid $tp"; kill -TERM $py $tp 2>/dev/null; break
  fi
  if [ $((n % 3)) = 0 ]; then
    py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' ')
    av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
    if [ -n "$py" ] && [ -d /proc/$py ]; then rss=$(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status); ni=$(ps -o ni= -p $py | tr -d ' '); cpu=$(ps -o cputime= -p $py | tr -d ' '); else rss=0; ni=-; cpu=-; fi
    echo "$(date -u '+%T') lane $X MemAvailable $av MiB, python pid ${py:-none} RSS $rss MiB, cputime $cpu, nice $ni" >> $LD/memlog.log
    [ "$av" -lt 2048 ] && echo "ALERT $(date -u '+%F %T') UTC lane $X scan: MemAvailable $av MiB (alert only, nothing stopped)" >> $LD/alert.log
  fi
  n=$((n+1)); sleep 10
done
wait $tp; r=$?
grep -vE 'Warning|^  [a-z]+ = |slogdet' $RAW > $LD/scan.log
say "scan exit $r, $(( $(date -u +%s) - s0 )) s wall"
[ $r = 3 ] && say "STOP: not the record system (the system check failed)"
say "lane $X done"
exit
}
