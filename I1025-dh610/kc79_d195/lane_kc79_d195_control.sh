#!/bin/bash
{
# #1025 kc79_d195 (dh610), step 1 of the coordinator's order of 22 Nov: the control: d18_hybsign.py at D 19.125 on dh370's k_c 79 state and record (raw I1025-dh370/kc79_d19125/ at c58e5052), lambda 1.50,
# 1 process of 1 thread, nice 10. It must print the record system and dh370's hybrid sign and ln|det| of its lambda 1.50 row (-2537.823195774449) to 1e-9 relative (dh170 matched it to 1.1e-15).
# Stop and report if not. The scan of step 2 waits for dh370's D 19.5 state. d18_hybsign.py is xfkappa's, blob e089207a, unmodified. usage: bash lane_kc79_d195_control.sh [dry]
set -u
MODE=${1:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/kc79_d195; IN=$F/in
WT=/home/nathan/Source/choptuik-large-d-1025f; W=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
CAP_CONTROL=10800
L=$F/exits_kc79_d195.txt
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc79_d195: $*" | tee -a $L; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$IN/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" \
          "$IN/sol_l1kc79dh370_D19.1250.npy 3ff3fcb54b2684e9e6692a4508782e1d943d1b48" "$IN/l1kc79dh370.jsonl 15ac964fb37398094d4abcfd86453f0ba62175fe" \
          "$IN/ref_dh370_scan_kc79_D19.125_1025.jsonl 9a6ef23938a3684268a0246e46b9e643fe080da6"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
[ -e $F/control/scan_D19.125_p0.jsonl ] && { say "refuse: $F/control/scan_D19.125_p0.jsonl exists"; bad=1; }
# the pre-run checks of the control check: its selftest and its mutation
( cd $F && $PY control_check.py selftest > $F/selftest_control_check.log 2>&1; r0=$?
  $PY control_check.py selftest --mutate > $F/selftest_control_check_mutate.log 2>&1; r1=$?
  echo "$r0 $r1" > $F/selftest_control_exits.txt )
read r0 r1 < $F/selftest_control_exits.txt
[ $r0 = 0 ] && [ $r1 = 1 ] || { say "refuse: the control check's selftests did not behave (selftest $r0, mutate $r1; wanted 0 1)"; bad=1; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge 8000000 ] || { say "refuse: MemAvailable $av kB is below 8 GB"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked (inputs in in_blobs.txt, d18_hybsign e089207a, worktree 505d8399 clean, $PY), control_check selftests as wanted (exits $r0 $r1); MemAvailable $av kB"
[ "$MODE" = dry ] && { say "dry run: nothing started"; exit 0; }
cd $W
say "control: D 19.125, k_c 79, lambda 1.50, 1 process of 1 thread, nice 10, cap ${CAP_CONTROL} s by exact pid"
t0=$(date +%s)
nice -n 10 /usr/bin/time -v timeout -s TERM $CAP_CONTROL $PY -u $IN/d18_hybsign.py $IN/l1kc79dh370.jsonl $IN/sol_l1kc79dh370_D19.1250.npy 19.125 1.50 $F/control/scan_D19.125_p0.jsonl < /dev/null > $F/control/control.raw 2>&1
rc=$?; tc=$(( $(date +%s) - t0 ))
grep -vE 'Warning|^  [a-z]+ = |slogdet' $F/control/control.raw > $F/control/control.log
MAXRSS=$(awk '/Maximum resident set size/ {print $NF}' $F/control/control.raw); say "control exit $rc, wall $tc s, max RSS ${MAXRSS:-?} kB"
[ $rc = 0 ] || { say "STOP: the control did not end cleanly (exit $rc; 3 = not the record system, 124 = the cap): this machine's build or the state differs"; exit; }
$PY $F/control_check.py $F/control/control.log $F/control/scan_D19.125_p0.jsonl $IN/ref_dh370_scan_kc79_D19.125_1025.jsonl 1.50 | tee $F/control/control_check.txt | tee -a $L
if [ "${PIPESTATUS[0]}" = 0 ]; then say "control PASS: the scan of the order waits for dh370's D 19.5 state"; else say "STOP: the control does not match dh370's row to 1e-9: report, no scan"; fi
say "control done"
exit 0
}
