#!/bin/bash
{
# #1025 kc71_meet (t5's order): the hybrid sign scan d18_hybsign.py (e089207a, unmodified: the record system check first, the hybrid sign, the 1e-15 noise test on blocks 0-11 with 2 seeds, the float64 sign beside)
# on win2's k_c 71 state at D 19.1875 (lane 1) or D 19.25 (lane 2): lambda 1.42 to 1.58 at 0.01 (17 values) plus a repeat of 1.50 at the end (18 evaluations). Starts only if control/control_check.txt says PASS.
# usage: lane_kc71.sh 1|2 [dry]   (4 threads, nice 10, 8 h cap by exact pid; a systemd user unit)
set -u
N=${1:?1 or 2}; MODE=${2:-}
F=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc71_meet
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python; WT=/home/nathan/Source/choptuik-large-d-1025p4; W=$WT/solver/matter
case $N in
  1) DD=19.1875; ST=$F/in/sol_l1kc71Lw1025_D19.187500.npy;;
  2) DD=19.25;   ST=$F/in/sol_l1kc71Lw1025_D19.250000.npy;;
  *) echo "usage: $0 1|2 [dry]"; exit 9;;
esac
REC=$F/in/l1kc71Lw1025.jsonl; LD=$F/lane$N; mkdir -p $LD
LAMS=$($PY -c 'print(",".join([f"{1.42 + 0.01 * i:.2f}" for i in range(17)] + ["1.50"]))'); NEV=18
HS=$F/in/d18_hybsign.py; SCAN=$LD/scan_D${DD}_p0.jsonl; L=$LD/exits.txt; RAW=$LD/scan.raw
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC lane $N (D $DD): $*" | tee -a $L; }
bad=0
while read -r h f; do [ -f $F/in/$f ] && [ "$(git hash-object --no-filters $F/in/$f)" = "$h" ] || { say "refuse: in/$f missing or not blob $h"; bad=1; }; done < $F/in_blobs.txt
head -c 4 $F/control/control_check.txt 2>/dev/null | grep -q '^PASS' || { say "refuse: control/control_check.txt does not say PASS"; bad=1; }
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
for f in $SCAN $RAW; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
$PY -c "import numpy, scipy, mpmath, multidouble; multidouble.dd_logdet" || { say "refuse: $PY lacks numpy/scipy/mpmath/multidouble.dd_logdet"; bad=1; }
[ $bad = 0 ] || exit 2
[ "$MODE" = dry ] && L=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/5e14df5b-8f5b-49f8-ab79-88a302ef8042/scratchpad/dry_exits_lane$N.txt
say "pins checked (in_blobs.txt), control PASS, worktree 505d8399 clean; $PY; 4 threads"
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
    echo "$(date -u '+%T') lane $N MemAvailable $av MiB, python pid ${py:-none} RSS $rss MiB, cputime $cpu, nice $ni" >> $LD/memlog.log
    [ "$av" -lt 2048 ] && echo "ALERT $(date -u '+%F %T') UTC lane $N scan: MemAvailable $av MiB (alert only, nothing stopped)" >> $LD/alert.log
  fi
  n=$((n+1)); sleep 10
done
wait $tp; r=$?
grep -vE 'Warning|^  [a-z]+ = |slogdet' $RAW > $LD/scan.log
say "scan exit $r, $(( $(date +%s) - s0 )) s wall"
[ $r = 3 ] && say "STOP: not the record system (the system check failed)"
say "lane $N done"
exit
}
