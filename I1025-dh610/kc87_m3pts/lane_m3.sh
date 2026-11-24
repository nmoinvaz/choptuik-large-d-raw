#!/bin/bash
# #1025 kc87_m3pts (dh610), the coordinator's order of 24 Nov (hc, read at 19:43 UTC): lambda_1 on four of macm3's k_c 87 leg states (raw I1025-macm3/kc87_leg2/b, tag l1kc87Lmacm3b): D 21.5625, 21.6875, 21.8125, 21.9375, one at a time; one subfolder per D.
# usage: bash lane_m3.sh D CENTER PRED [dry|check]   (D the state's D, CENTER the grid centre (the multiple of 0.005 nearest PRED), PRED = k_c 79's reading at D + 0.002; env FNAME names the folder when it is not D)
#  1. pins (in_blobs.txt of this folder's in/ and of <D>/), worktrees, selftests (kc79_syscheck, kc87_syscheck, read_lower and its two mutations, repeat_check, leg_read and its mutation: 0 0 0 1 1 0 0 1);
#  2. the source: kc87_syscheck_1025.py accepts the state and record at D (exit 0; --mutate=F and --mutate=steps exit 1) and kc79_syscheck_1025.py refuses it (exit 1);
#  3. d18_hybsign.py (e089207a, unmodified) at CENTER-0.015 to CENTER+0.015 by 0.005 (7 values) plus a repeat of CENTER (8 evaluations, 8 processes of 1 thread, nice 8; p0..p6 the grid, p7 the repeat) in
#     ~/Source/choptuik-large-d-1025f at 505d8399;
#  4. read_lower.py (89309d3c) on the window, repeat_check.py, leg_read.py read (against PRED, bar 0.005); the order has no widening: no robust change is reported as read.
# `check` stops after step 2 (a test of the lane on a state somebody else scans); `dry` stops after step 1. Each step stops the lane when it fails and nothing later runs. Memory: refuses to start the scan with less than
# 8 x 2.5 GB + 4 GB available; nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08): below 4 GiB the sampler only writes MEMALERT.txt.
{
set -u
D=$1; C=$2; PRED=$3; MODE=${4:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; LEG=$RAW/I1025-dh610/kc87_m3pts; F=$LEG/${FNAME:-$D}; IN=$LEG/in; DIN=$F/in; S=$F/scan; RG=$F/src
WT=/home/nathan/Source/choptuik-large-d-1025g; WTM=$WT/solver/matter; WTF=/home/nathan/Source/choptuik-large-d-1025f; WF=$WTF/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
TAG=l1kc87Lmacm3b
Df=$(printf '%.6f' $D); STATE=$DIN/sol_${TAG}_D$Df.npy; REC=$DIN/${TAG}.jsonl
L=$F/exits_k87l.txt; MEMSTOP=4194304; PUSH=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/push_folder.sh
export PYTHONDONTWRITEBYTECODE=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc87_m3pts D $D: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
stop() { say "STOP: $*"; exit 1; }
mkdir -p $S $RG
bad=0
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$bb" ] || { say "refuse: $IN/$f missing or not blob $bb"; bad=1; }; done < $LEG/in_blobs.txt
while read bb f; do [ -f $DIN/$f ] && [ "$(blob $DIN/$f)" = "$bb" ] || { say "refuse: $DIN/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs.txt
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || { say "refuse: $WT is not at 48c36355"; bad=1; }
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || { say "refuse: $f.py differs from 505d8399"; bad=1; }; done
[ "$(git -C $WTF rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WTF status --short)" ] || { say "refuse: $WTF is not clean at 505d8399"; bad=1; }
[ -e $S/scan_D${D}_p0.jsonl ] && [ -z "$MODE" ] && { say "refuse: $S/scan_D${D}_p0.jsonl exists"; bad=1; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ -n "$MODE" ] || [ "$av" -ge $(( 8 * 2500000 + 4000000 )) ] || { say "refuse: MemAvailable $av kB is below 8 x 2.5 GB + 4 GB"; bad=1; }
[ $bad = 0 ] || exit 2
LAMS=$($PY -c "c = $C; print(','.join(f'{round(c + 0.005 * k, 3):.3f}' for k in range(-3, 4)))"); LO=$($PY -c "print(f'{round($C - 0.015, 3):.3f}')"); HI=$($PY -c "print(f'{round($C + 0.015, 3):.3f}')")
say "pins checked (in_blobs.txt of in/ and $(basename $F)/, worktrees 1025g 48c36355 and 1025f 505d8399, MemAvailable $av kB, load $(cut -d' ' -f1-3 /proc/loadavg), $($PY -V 2>&1)); window $LO to $HI, grid $LAMS and a repeat of $C; prediction $PRED (bar 0.005); mode '${MODE:-run}'"
export D18_DIR=$IN
( cd $IN
  $PY -I kc79_syscheck_1025.py --selftest > $F/selftest_kc79_syscheck.log 2>&1; a0=$?
  $PY -I kc87_syscheck_1025.py --selftest > $F/selftest_kc87_syscheck.log 2>&1; a1=$?
  $PY -W ignore read_lower.py selftest > $F/selftest_read_lower.log 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $F/selftest_read_lower_mutate_shift.log 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $F/selftest_read_lower_mutate_round2.log 2>&1; r2=$?
  $PY repeat_check.py selftest > $F/selftest_repeat_check.log 2>&1; r3=$?
  $PY -I leg_read.py selftest > $F/selftest_leg_read.log 2>&1; g0=$?
  $PY -I leg_read.py selftest --mutate > $F/selftest_leg_read_mutate.log 2>&1; g1=$?
  echo "$a0 $a1 $r0 $r1 $r2 $r3 $g0 $g1" > $F/selftest_exits.txt )
read -r a0 a1 r0 r1 r2 r3 g0 g1 < $F/selftest_exits.txt
[ "$a0 $a1 $r0 $r1 $r2 $r3 $g0 $g1" = "0 0 0 1 1 0 0 1" ] || stop "the selftests did not behave (kc79_syscheck $a0, kc87_syscheck $a1, read_lower $r0 $r1 $r2, repeat_check $r3, leg_read $g0 $g1; wanted 0 0 0 1 1 0 0 1)"
say "selftests as wanted (kc79_syscheck, kc87_syscheck, read_lower, mutate shift, mutate round2, repeat_check, leg_read, mutate: 0 0 0 1 1 0 0 1)"
[ "$MODE" = dry ] && { say "dry run: nothing started"; exit 0; }
# 2. the source
$PY -I $IN/kc87_syscheck_1025.py $REC $STATE $D $WTM > $RG/syscheck.txt 2>&1; s=$?
for m in F steps; do $PY -I $IN/kc87_syscheck_1025.py $REC $STATE $D $WTM --mutate=$m > $RG/syscheck_mutate_$m.txt 2>&1; eval "c$m=$?"; done
$PY -I $IN/kc79_syscheck_1025.py $REC $STATE $D $WTM > $RG/syscheck_kc79_refuses.txt 2>&1; k=$?
say "source check: kc87_syscheck_1025.py exit $s; controls --mutate=F exit $cF, --mutate=steps exit $csteps (1 wanted each); kc79_syscheck_1025.py on it exit $k (1 wanted): $(tail -n 3 $RG/syscheck.txt | cut -c1-330 | tr '\n' ' ')"
[ $s = 0 ] && [ $cF = 1 ] && [ $csteps = 1 ] && [ $k = 1 ] || stop "the state is not accepted by the k_c 87 check on this build, a control did not exit 1, or the k_c 79 check did not refuse it"
cp $RG/syscheck.txt $RG/ACCEPTED.txt
[ "$MODE" = check ] && { say "check run: source accepted, nothing scanned"; exit 0; }
# 3. the scan
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WF
IFS=, read -ra LA <<< "$LAMS"
LISTS=("${LA[0]}" "${LA[1]}" "${LA[2]}" "${LA[3]}" "${LA[4]}" "${LA[5]}" "${LA[6]}" "$C")
say "scan: lambda $LO to $HI by 0.005 and a repeat of $C (8 evaluations), lists ${LISTS[*]}, 8 processes of 1 thread, nice 8, cap 28800 s each"
pids=()
for j in 0 1 2 3 4 5 6 7; do
  ( cd $WF && nice -n 8 /usr/bin/time -v timeout -s TERM 28800 $PY -u $IN/d18_hybsign.py $REC $STATE $D ${LISTS[$j]} $S/scan_D${D}_p$j.jsonl < /dev/null > $S/scan_p$j.raw 2>&1
    echo "$(date -u '+%F %T') UTC scan p$j (${LISTS[$j]}) exit $?" >> $L ) &
  pids+=($!)
done
( sleep 10; while pgrep -f "d18_hybsign.py.*sol_${TAG}_D$Df" > /dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    echo "$(date -u '+%F %T') UTC alive $(pgrep -f "d18_hybsign.py.*sol_${TAG}_D$Df" | wc -l), MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg), points $(cat $S/scan_D${D}_p*.jsonl 2>/dev/null | wc -l)" >> $S/sampler.log
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT_scan.txt
    sleep 30
  done ) &
wait "${pids[@]}"
for j in 0 1 2 3 4 5 6 7; do grep -vE 'Warning|^  [a-z]+ = |slogdet' $S/scan_p$j.raw > $S/scan_p$j.log; say "p$j: $(grep -E 'record system' $S/scan_p$j.log | head -1 | cut -c1-150)"; done
cat $S/scan_D${D}_p*.jsonl | $PY -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$S/scan_D${D}_all.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $L
# 4. the reading
( cd $IN; { echo "=== read_lower.py $S $LO $HI"; $PY -W ignore read_lower.py $S $LO $HI; echo "read_lower exit $?"; echo "=== repeat_check.py (merged scan file)"; $PY repeat_check.py $S/scan_D${D}_all.jsonl; echo "repeat_check exit $?"; } > $F/read_lower.txt 2>&1
  $PY -I leg_read.py read $F/read_lower.txt $PRED 0.005 > $F/leg_read.txt 2>&1 )
say "reading: $(grep -E '^hybrid signs|^robust changes|change \(|against the prediction' $F/leg_read.txt | tr '\n' ' ' | cut -c1-500)"
[ "$(grep -c '   change (' $F/leg_read.txt)" = 0 ] && say "no robust change in the window (the order has no widening): reported as read"
bash $PUSH I1025-dh610/kc87_m3pts/${FNAME:-$D} "I1025-dh610/kc87_m3pts/${FNAME:-$D}: scan rows and reading" > $F/push_scan.txt 2>&1
say "scan done; readings in read_lower.txt and leg_read.txt; k87l point done"
exit 0
}
