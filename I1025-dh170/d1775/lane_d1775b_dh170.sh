#!/bin/bash
# #1025 D 17.75, part 2 (the coordinator's hc, 21 Nov ~10:40 UTC): the same script and state as lane_d1775_dh170.sh, lambda 1.69 down to 1.40 at 0.01 (30 points, descending so that the first change below 1.70 shows first), after part 1 (pid 1082436) has ended.
# The controls of part 1 (ell_ddm selftest PASS / --mutate=slices FAIL; the three-point cross-check at D 18) stand: same code, state, python and threads; the pins are checked again.
{
# v2 (21 Nov 07:58 UTC): stage 2 replaced after the first cross-check failed its own 1e-6 ln|det| criterion (see README); v1 is lane_d1775_dh170_v1.sh.
# #1025 D 17.75 on dh170 (coordinator's hc, 21 Nov ~07:45 UTC): xfkappa's scan (A) of lane_d18b.sh (the hybrid sign scan, d18_hybsign.py with the noise test and the float64 sign beside each point) at D 17.75 on winb's
# state sol_l1kc63W1025_D17.750000.npy (k_c 63), lambda 1.70 to 1.95 at 0.01 (26 points), 4 threads, nice 10, an 8 h cap by exact pid. Stages: pins; 1 the planted control ell_ddm.py selftest (PASS) and --mutate=slices (FAIL);
# 2 the cross-check: the hybrid at D 18, lam 1.8 on xfkappa's inputs must give +1 with ln|det| -1925.0182289868 (his d18_hybsign.log) to 1e-6, noise-robust, float64 +1; 3 the scan; 4 the reading (d1775_read.py).
# xfkappa's command of (A) (lane_d18b.sh):  timeout 21600 nice -n 10 $PY -u $Q/d18_hybsign.py $STUB $ST 18 $L $SCAN   with L = 1.70,1.71,...,1.90. Here: STUB = winb's record file (the D 17.75 row), ST = winb's D 17.75 state, D 17.75.
set -u
D=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/d1775; I=/home/nathan/scratch1025d1775
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python; WT=/home/nathan/Source/choptuik-large-d-1025p4; W=$WT/solver/matter
ST=$I/sol_l1kc63W1025_D17.750000.npy; REC=$I/l1kc63W1025.jsonl; ST18=$I/sol_l1kc63W1025_D18.000000.npy; STUB18=$I/d18_stub_l1kc63W1025.jsonl
HS=$D/d18_hybsign.py; SCAN=$D/d1775b_scan_dh170.jsonl; XJ=$D/d18_crosscheck3_dh170.jsonl; L=$D/exits_d1775b.txt
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*" | tee -a $L; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$ST de9fc3e55aa46bafd4ef62536861f94aed9e3035" "$REC c33039dfa38b495486fb3ef7da77077d43db775a" "$ST18 45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21" "$STUB18 2cfdb8334ed6ba7013396190d8a4833b2b854c4b" "$HS e089207a61fbd98614716abd309571cbc4888db2" "$I/ell_d18_hybrid_1025.jsonl fbeaa7a1be52f6fe9c3c52bb2c243b28eb9b57ee"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
for f in $SCAN; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
$PY -c "import numpy, scipy, mpmath, multidouble; multidouble.dd_logdet" || { say "refuse: $PY lacks numpy/scipy/mpmath/multidouble.dd_logdet"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked: state de9fc3e5 (D 17.75), record c33039df, D 18 state 45e72c6a, D 18 stub 2cfdb833, d18_hybsign e089207a, worktree 505d8399 clean; $PY; 4 threads"
cd $W
say "part 2 waits for part 1's lane (pid 1082436) to end"
while kill -0 1082436 2>/dev/null; do sleep 30; done
say "part 1 ended; part 2 starts"
LAMS=$($PY -c 'print(",".join(f"{1.69 - 0.01 * i:.2f}" for i in range(30)))')
say "scan part 2 at D 17.75: lam $LAMS; 8 h cap (28800 s) by exact pid"
s0=$(date +%s)
nice -n 10 /usr/bin/time -v $PY -u $HS $REC $ST 17.75 $LAMS $SCAN < /dev/null > $D/d1775b_scan.raw 2>&1 &
tp=$!; echo $tp > $D/time_pid_scanb.txt; say "scan part 2 started under /usr/bin/time pid $tp"
while kill -0 $tp 2>/dev/null; do
  if [ $(( $(date +%s) - s0 )) -gt 28800 ]; then
    py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' '); say "8 h cap reached: TERM to python pid $py and time pid $tp"; kill -TERM $py $tp 2>/dev/null; break
  fi
  sleep 10
done
wait $tp; r=$?
grep -vE 'Warning|^  [a-z]+ = |slogdet' $D/d1775b_scan.raw > $D/d1775b_scan.log
say "scan part 2 exit $r, $(( $(date +%s) - s0 )) s wall"
$PY -I $D/d1775_read.py $SCAN > $D/d1775b_read.txt 2>&1; say "reading (part 2 alone): $(grep -E '^READING' $D/d1775b_read.txt)"
cat $D/d1775_scan_dh170.jsonl $SCAN > $D/d1775_all_dh170.jsonl; $PY -I $D/d1775_read.py $D/d1775_all_dh170.jsonl > $D/d1775_all_read.txt 2>&1; say "reading (both parts, lambda 1.40 to 1.95): $(grep -E '^READING' $D/d1775_all_read.txt)"
say "lane d1775b done"
exit
}
