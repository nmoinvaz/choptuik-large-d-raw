#!/bin/bash
{
# #1025 k_c break bisection, step 2, scan at D 18.46875 on dh170 (the coordinator's hc, 22 Nov): the hybrid sign scan d18_hybsign.py (e089207a: the record system check first, the hybrid sign, p4_hybrid's 1e-15 noise test on
# blocks 0-11 with 2 seeds, the float64 sign beside) over lambda 1.62 to 1.80 at 0.01 on one k_c's state at D 18.46875; usage: lane_kcbreak_dh170.sh 63|55 (the two lanes run side by side, 4 threads each, nice 10).
# lambda list: 1.71 first and last (a repeat check: the reader's merge compares repeated points), then 1.62 ... 1.80.
set -u
KC=${1:?63 or 55}
D=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc_break_D18.46875
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python; WT=/home/nathan/Source/choptuik-large-d-1025p4; W=$WT/solver/matter
case $KC in
  63) TAG=l1kc63dh1025;;
  55) TAG=l1kc55dh1025;;
  *) echo "usage: $0 63|55"; exit 9;;
esac
ST=$D/sol_${TAG}_D18.468750.npy; REC=$D/$TAG.jsonl
read -r PK STH RECH < $D/pins_kc$KC.txt || { echo "no accepted state: $D/pins_kc$KC.txt"; exit 2; }
[ "$PK" = "$KC" ] || { echo "pins_kc$KC.txt is for k_c $PK"; exit 2; }
HS=$D/d18_hybsign.py; SCAN=$D/kc${KC}_D18.46875_scan_dh170.jsonl; L=$D/exits_kc$KC.txt; RAW=$D/kc${KC}_scan.raw
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC k_c $KC: $*" | tee -a $L; }
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
[ -n "${DRYRUN:-}" ] && L=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/026ace6b-8e85-4de1-9fd2-85ec04d52786/scratchpad/dry_exits_kc$KC.txt
say "pins checked: state $(basename $ST) $STH, record $(basename $REC) $RECH, d18_hybsign e089207a, worktree 505d8399 clean; $PY; 4 threads"
[ -n "${DRYRUN:-}" ] && { say "dry run: pins ok, nothing started"; exit 0; }
cd $W
say "1. planted control: ell_ddm.py selftest (must PASS), then --mutate=slices (must FAIL), 1800 s each"
timeout 1800 nice -n 10 $PY -u ell_ddm.py selftest < /dev/null > $D/ell_ddm_selftest_kc$KC.log 2>&1; r1=$?
timeout 1800 nice -n 10 $PY -u ell_ddm.py selftest --mutate=slices < /dev/null >> $D/ell_ddm_selftest_kc$KC.log 2>&1; r2=$?
grep -E '^selftest:' $D/ell_ddm_selftest_kc$KC.log | tee -a $L
[ $r1 = 0 ] && [ $r2 = 1 ] || { say "STOP: the planted control did not behave (selftest exit $r1, --mutate=slices exit $r2)"; exit; }
LAMS=$($PY -c 'print(",".join(["1.71"] + [f"{1.62 + 0.01 * i:.2f}" for i in range(19)] + ["1.71"]))')
say "2. the scan at D 18.46875: lam $LAMS (21 evaluations; the system check is the script's first line, exit 3 if it is not the record system); 8 h cap by exact pid"
s0=$(date +%s)
nice -n 10 /usr/bin/time -v $PY -u $HS $REC $ST 18.46875 $LAMS $SCAN < /dev/null > $RAW 2>&1 &
tp=$!; echo $tp > $D/time_pid_kc$KC.txt; say "scan started under /usr/bin/time pid $tp"
n=0
while kill -0 $tp 2>/dev/null; do
  if [ $(( $(date +%s) - s0 )) -gt 28800 ]; then
    py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' '); say "8 h cap reached: TERM to python pid $py and time pid $tp"; kill -TERM $py $tp 2>/dev/null; break
  fi
  if [ $((n % 3)) = 0 ]; then
    py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' ')
    av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
    if [ -n "$py" ] && [ -d /proc/$py ]; then rss=$(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status); ni=$(ps -o ni= -p $py | tr -d ' '); cpu=$(ps -o cputime= -p $py | tr -d ' '); else rss=0; ni=-; cpu=-; fi
    echo "$(date -u '+%T') k_c $KC MemAvailable $av MiB, python pid ${py:-none} RSS $rss MiB, cputime $cpu, nice $ni" >> $D/memlog_kc$KC.log
    [ "$av" -lt 2048 ] && echo "ALERT $(date -u '+%F %T') UTC k_c $KC scan: MemAvailable $av MiB (alert only, nothing stopped)" >> $D/alert_kc.log
  fi
  n=$((n+1)); sleep 10
done
wait $tp; r=$?
grep -vE 'Warning|^  [a-z]+ = |slogdet' $RAW > $D/kc${KC}_scan.log
say "scan exit $r, $(( $(date -u +%s) - s0 )) s wall"
[ $r = 3 ] && say "STOP: not the record system (the system check failed)"
say "lane kc$KC done"
exit
}
