#!/bin/bash
{
# #1025 kc79_d19125low (t5's order): the hybrid sign scan d18_hybsign.py (e089207a, unmodified; the record system check first, the hybrid sign, the 1e-15 noise test on blocks 0-11 with 2 seeds, the float64 sign beside)
# on dh370's k_c 79 D 19.125 state: lambda 1.10 to 1.44 at 0.02 (18 values) plus a repeat of 1.30 (19 evaluations), split in two processes of 4 threads: p0 the even-index values (1.10, 1.14, ..., 1.42), p1 the odd-index
# ones (1.12, ..., 1.44) and the repeat of 1.30 at its end, so the repeat is on another process than the first 1.30. Starts only if control/control_check.txt says PASS. usage: scan_k79.sh 0|1 [dry]
set -u
P=${1:?0 or 1}; MODE=${2:-}
F=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc79_d19125low
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python; WT=/home/nathan/Source/choptuik-large-d-1025p4; W=$WT/solver/matter
case $P in
  0) LAMS=1.10,1.14,1.18,1.22,1.26,1.30,1.34,1.38,1.42; NEV=9;;
  1) LAMS=1.12,1.16,1.20,1.24,1.28,1.32,1.36,1.40,1.44,1.30; NEV=10;;
  *) echo "usage: $0 0|1 [dry]"; exit 9;;
esac
ST=$F/in/sol_l1kc79dh370_D19.1250.npy; REC=$F/in/l1kc79dh370.jsonl; LD=$F/scan; mkdir -p $LD
HS=$F/in/d18_hybsign.py; SCAN=$LD/scan_D19.125_p$P.jsonl; L=$LD/exits_p$P.txt; RAW=$LD/scan_p$P.raw
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC process $P: $*" | tee -a $L; }
bad=0
while read -r h f; do [ -f $F/in/$f ] && [ "$(git hash-object --no-filters $F/in/$f)" = "$h" ] || { say "refuse: in/$f missing or not blob $h"; bad=1; }; done < $F/in_blobs.txt
head -c 4 $F/control/control_check.txt 2>/dev/null | grep -q '^PASS' || { say "refuse: control/control_check.txt does not say PASS"; bad=1; }
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
for f in $SCAN $RAW; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
$PY -c "import numpy, scipy, mpmath, multidouble; multidouble.dd_logdet" || { say "refuse: $PY lacks numpy/scipy/mpmath/multidouble.dd_logdet"; bad=1; }
[ $bad = 0 ] || exit 2
[ "$MODE" = dry ] && L=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/5e14df5b-8f5b-49f8-ab79-88a302ef8042/scratchpad/dry_exits_k79p$P.txt
say "pins checked (in_blobs.txt), control PASS, worktree 505d8399 clean; $PY; 4 threads"
[ "$MODE" = dry ] && { say "dry run: pins ok, lambda list $LAMS ($NEV evaluations), nothing started"; exit 0; }
cd $W
say "1. planted control: ell_ddm.py selftest (must PASS), then --mutate=slices (must FAIL), 1800 s each"
timeout 1800 nice -n 10 $PY -u ell_ddm.py selftest < /dev/null > $LD/ell_ddm_selftest_p$P.log 2>&1; r1=$?
timeout 1800 nice -n 10 $PY -u ell_ddm.py selftest --mutate=slices < /dev/null >> $LD/ell_ddm_selftest_p$P.log 2>&1; r2=$?
grep -E '^selftest:' $LD/ell_ddm_selftest_p$P.log | tee -a $L
[ $r1 = 0 ] && [ $r2 = 1 ] || { say "STOP: the planted control did not behave (selftest exit $r1, --mutate=slices exit $r2)"; exit; }
say "2. the scan at D 19.125: lam $LAMS ($NEV evaluations; the system check is the script's first line, exit 3 if it is not the record system); 8 h cap by exact pid"
s0=$(date +%s)
nice -n 10 /usr/bin/time -v $PY -u $HS $REC $ST 19.125 $LAMS $SCAN < /dev/null > $RAW 2>&1 &
tp=$!; echo $tp > $LD/time_pid_p$P.txt; say "scan started under /usr/bin/time pid $tp"
n=0
while kill -0 $tp 2>/dev/null; do
  if [ $(( $(date +%s) - s0 )) -gt 28800 ]; then
    py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' '); say "8 h cap reached: TERM to python pid $py and time pid $tp"; kill -TERM $py $tp 2>/dev/null; break
  fi
  if [ $((n % 6)) = 0 ]; then
    py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' ')
    av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
    if [ -n "$py" ] && [ -d /proc/$py ]; then rss=$(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status); ni=$(ps -o ni= -p $py | tr -d ' '); cpu=$(ps -o cputime= -p $py | tr -d ' '); else rss=0; ni=-; cpu=-; fi
    echo "$(date -u '+%T') process $P MemAvailable $av MiB, python pid ${py:-none} RSS $rss MiB, cputime $cpu, nice $ni" >> $LD/memlog_p$P.log
    [ "$av" -lt 2048 ] && echo "ALERT $(date -u '+%F %T') UTC process $P scan: MemAvailable $av MiB (alert only, nothing stopped)" >> $LD/alert.log
  fi
  n=$((n+1)); sleep 10
done
wait $tp; r=$?
grep -vE 'Warning|^  [a-z]+ = |slogdet' $RAW > $LD/scan_p$P.log
say "scan exit $r, $(( $(date +%s) - s0 )) s wall"
[ $r = 3 ] && say "STOP: not the record system (the system check failed)"
say "process $P done"
exit
}
