#!/bin/bash
# #1025 kc79_leg (dh610), the coordinator's order of 23 Nov (hc, #1025 comment of "17:45"): lambda_1 on each point of win2's k_c 79 leg (I1025-win2/kc79_leap, tag l1kc79Lw1025d), one subfolder per D.
# usage: bash lane_leg.sh D CENTER PRED [dry]   (D the leg's D, CENTER the grid centre (the multiple of 0.005 nearest PRED), PRED the coordinator's prediction)
#  1. pins (in_blobs.txt of this folder's in/ and of D<D>/), worktrees, selftests (kc79_syscheck, read_lower and its two mutations, repeat_check, leg_read and its mutation: 0 0 1 1 0 0 1);
#  2. the source: kc79_syscheck_1025.py accepts the state and record at D (exit 0; --mutate=F and --mutate=steps exit 1);
#  3. d18_hybsign.py (e089207a, unmodified) at CENTER-0.015 to CENTER+0.015 by 0.005 (7 values) plus a repeat of CENTER (8 evaluations, 8 processes of 1 thread, nice 5; p0..p6 the grid, p7 the repeat) in
#     ~/Source/choptuik-large-d-1025f at 505d8399;
#  4. read_lower.py (89309d3c) on the window, repeat_check.py, leg_read.py read (against PRED, bar 0.01);
#  5. no robust change: widen once by 0.015 toward the window edge with the lower ln|det| (leg_read.py widen; three values, 3 processes), read the widened window, report. One or several changes: report as read.
# Each step stops the lane when it fails and nothing later runs. Memory: refuses to start the scan with less than 8 x 2.5 GB + 4 GB available; nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08):
# below 4 GiB the sampler only writes MEMALERT.txt.
{
set -u
D=$1; C=$2; PRED=$3
RAW=/home/nathan/Source/choptuik-large-d-raw; LEG=$RAW/I1025-dh610/kc79_leg; F=$LEG/D$D; IN=$LEG/in; DIN=$F/in; S=$F/scan; RG=$F/src
WT=/home/nathan/Source/choptuik-large-d-1025g; WTM=$WT/solver/matter; WTF=/home/nathan/Source/choptuik-large-d-1025f; WF=$WTF/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
TAG=$(cat $F/tag.txt 2>/dev/null || echo l1kc79Lw1025d)   # win2's leap tag of this point (D<D>/tag.txt; d when absent)
Df=$(printf '%.6f' $D); STATE=$DIN/sol_${TAG}_D$Df.npy; REC=$DIN/${TAG}.jsonl
L=$F/exits_leg.txt; MEMSTOP=4194304; PUSH=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/push_folder.sh
export PYTHONDONTWRITEBYTECODE=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc79_leg D $D: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
stop() { say "STOP: $*"; exit 1; }
mkdir -p $S $RG
bad=0
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$bb" ] || { say "refuse: $IN/$f missing or not blob $bb"; bad=1; }; done < $LEG/in_blobs.txt
while read bb f; do [ -f $DIN/$f ] && [ "$(blob $DIN/$f)" = "$bb" ] || { say "refuse: $DIN/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs.txt
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || { say "refuse: $WT is not at 48c36355"; bad=1; }
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || { say "refuse: $f.py differs from 505d8399"; bad=1; }; done
[ "$(git -C $WTF rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WTF status --short)" ] || { say "refuse: $WTF is not clean at 505d8399"; bad=1; }
[ -e $S/scan_D${D}_p0.jsonl ] && [ "${4:-}" != dry ] && { say "refuse: $S/scan_D${D}_p0.jsonl exists"; bad=1; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge $(( 8 * 2500000 + 4000000 )) ] || { say "refuse: MemAvailable $av kB is below 8 x 2.5 GB + 4 GB"; bad=1; }
[ $bad = 0 ] || exit 2
LAMS=$($PY -c "c = $C; print(','.join(f'{round(c + 0.005 * k, 3):.3f}' for k in range(-3, 4)))"); LO=$($PY -c "print(f'{round($C - 0.015, 3):.3f}')"); HI=$($PY -c "print(f'{round($C + 0.015, 3):.3f}')")
say "pins checked (in_blobs.txt of in/ and D$D/, worktrees 1025g 48c36355 and 1025f 505d8399, MemAvailable $av kB, load $(cut -d' ' -f1-3 /proc/loadavg), $($PY -V 2>&1)); window $LO to $HI, grid $LAMS and a repeat of $C; prediction $PRED"
export D18_DIR=$IN
( cd $IN
  $PY -I kc79_syscheck_1025.py --selftest > $F/selftest_kc79_syscheck.log 2>&1; a0=$?
  $PY -W ignore read_lower.py selftest > $F/selftest_read_lower.log 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $F/selftest_read_lower_mutate_shift.log 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $F/selftest_read_lower_mutate_round2.log 2>&1; r2=$?
  $PY repeat_check.py selftest > $F/selftest_repeat_check.log 2>&1; r3=$?
  $PY -I leg_read.py selftest > $F/selftest_leg_read.log 2>&1; g0=$?
  $PY -I leg_read.py selftest --mutate > $F/selftest_leg_read_mutate.log 2>&1; g1=$?
  echo "$a0 $r0 $r1 $r2 $r3 $g0 $g1" > $F/selftest_exits.txt )
read -r a0 r0 r1 r2 r3 g0 g1 < $F/selftest_exits.txt
[ "$a0 $r0 $r1 $r2 $r3 $g0 $g1" = "0 0 1 1 0 0 1" ] || stop "the selftests did not behave (kc79_syscheck $a0, read_lower $r0 $r1 $r2, repeat_check $r3, leg_read $g0 $g1; wanted 0 0 1 1 0 0 1)"
say "selftests as wanted (kc79_syscheck, read_lower, mutate shift, mutate round2, repeat_check, leg_read, mutate: 0 0 1 1 0 0 1)"
[ "${4:-}" = dry ] && { say "dry run: nothing started"; exit 0; }
# 2. the source
$PY -I $IN/kc79_syscheck_1025.py $REC $STATE $D $WTM > $RG/syscheck.txt 2>&1; s=$?
for m in F steps; do $PY -I $IN/kc79_syscheck_1025.py $REC $STATE $D $WTM --mutate=$m > $RG/syscheck_mutate_$m.txt 2>&1; eval "c$m=$?"; done
say "source check: kc79_syscheck_1025.py exit $s; controls --mutate=F exit $cF, --mutate=steps exit $csteps (1 wanted each): $(tail -n 3 $RG/syscheck.txt | cut -c1-330 | tr '\n' ' ')"
[ $s = 0 ] && [ $cF = 1 ] && [ $csteps = 1 ] || stop "the state is not accepted by the k_c 79 check on this build, or a control did not exit 1"
# 3. the scan
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WF
IFS=, read -ra LA <<< "$LAMS"
LISTS=("${LA[0]}" "${LA[1]}" "${LA[2]}" "${LA[3]}" "${LA[4]}" "${LA[5]}" "${LA[6]}" "$C")
say "scan: lambda $LO to $HI by 0.005 and a repeat of $C (8 evaluations), lists ${LISTS[*]}, 8 processes of 1 thread, nice 5, cap 28800 s each"
pids=()
for j in 0 1 2 3 4 5 6 7; do
  ( cd $WF && nice -n 5 /usr/bin/time -v timeout -s TERM 28800 $PY -u $IN/d18_hybsign.py $REC $STATE $D ${LISTS[$j]} $S/scan_D${D}_p$j.jsonl < /dev/null > $S/scan_p$j.raw 2>&1
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
merge() { cat $S/scan_D${D}_p*.jsonl | $PY -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$S/scan_D${D}_all.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $L; }
merge
# 4. the reading
reading() { # LO HI SUFFIX
  ( cd $IN; { echo "=== read_lower.py $S $1 $2"; $PY -W ignore read_lower.py $S $1 $2; echo "read_lower exit $?"; echo "=== repeat_check.py (merged scan file)"; $PY repeat_check.py $S/scan_D${D}_all.jsonl; echo "repeat_check exit $?"; } > $F/read_lower$3.txt 2>&1
    $PY -I leg_read.py read $F/read_lower$3.txt $PRED > $F/leg_read$3.txt 2>&1 ); }
reading $LO $HI ""
say "reading: $(grep -E '^hybrid signs|^robust changes|change \(|against the prediction' $F/leg_read.txt | tr '\n' ' ' | cut -c1-500)"
# 5. no robust change: widen once
nch=$(grep -c '   change (' $F/leg_read.txt)
if [ "$nch" = 0 ]; then
  W=$($PY -I $IN/leg_read.py widen $S/scan_D${D}_all.jsonl $LO $HI); wrc=$?
  say "no robust change in the window: widen once toward the lower ln|det| edge: leg_read widen exit $wrc: $W"
  [ $wrc = 0 ] || stop "no side to widen to (equal edge ln|det|)"
  SIDE=${W%% *}; WL=${W#* }; IFS=, read -ra WA <<< "$WL"
  pids=()
  for j in 0 1 2; do
    ( cd $WF && nice -n 5 /usr/bin/time -v timeout -s TERM 28800 $PY -u $IN/d18_hybsign.py $REC $STATE $D ${WA[$j]} $S/scan_D${D}_pw$j.jsonl < /dev/null > $S/scan_pw$j.raw 2>&1
      echo "$(date -u '+%F %T') UTC widen w$j (${WA[$j]}) exit $?" >> $L ) &
    pids+=($!)
  done
  wait "${pids[@]}"
  for j in 0 1 2; do grep -vE 'Warning|^  [a-z]+ = |slogdet' $S/scan_pw$j.raw > $S/scan_pw$j.log; say "w$j: $(grep -E 'record system' $S/scan_pw$j.log | head -1 | cut -c1-150)"; done
  merge
  if [ "$SIDE" = low ]; then WLO=$($PY -c "print(f'{round($LO - 0.015, 3):.3f}')"); WHI=$HI; else WLO=$LO; WHI=$($PY -c "print(f'{round($HI + 0.015, 3):.3f}')"); fi
  reading $WLO $WHI "_widened"
  say "reading of the widened window $WLO to $WHI: $(grep -E '^hybrid signs|^robust changes|change \(|against the prediction' $F/leg_read_widened.txt | tr '\n' ' ' | cut -c1-500)"
fi
bash $PUSH I1025-dh610/kc79_leg/D$D "I1025-dh610/kc79_leg/D$D: scan rows and reading" > $F/push_scan.txt 2>&1
say "scan done; readings in read_lower*.txt and leg_read*.txt; leg point done"
exit 0
}
