#!/bin/bash
# #1025 kc95_d22 / kc95_d225 on win2, the scan after the k_c 95 regrid (the coordinator's hc of 2026-11-24 ~17:25 UTC): "then d18_hybsign.py with 4 processes on lambda = (macm3's k_c 87 root at that D + 0.003) rounded to 0.005, +-0.01 by 0.005,
# plus a repeat of the centre (prediction: k_c 87 root + 0.003, bar 0.005)". usage: kc95_scan.sh D NEWTAG SUBFOLDER   (DRY=1: pins, selftests, the plan; no wait for the regrid)
# Waits for SUB/regrid_accepted.txt (exit 3 if regrid_refused.txt appears), for macm3's k_c 87 root at D in raw I1025-macm3/kc87_leg_lambda/roots87.txt (read with gh api; centre.py), for the scan memory (alert only elsewhere; a wait here)
# and for my other d18_hybsign scans to end. The six evaluations (centre-0.01, -0.005, centre, +0.005, +0.01, and the repeat of the centre) on FOUR processes of one thread: P1 centre, centre+0.01 | P2 centre (the repeat), centre-0.01 |
# P3 centre-0.005 | P4 centre+0.005. xfkappa's d18_hybsign.py (blob e089207a, unchanged; its first line is the record-system check, exit 3 if not). Caps 28800 s by the exact root pids. Then read_lower.py (89309d3c) on the folder
# at centre-0.01 .. centre+0.01, repeat_check.py (aaf598a9), pair2025.py on P1 and P2 (their first records are the same lambda), leg_read.py (5cae2639) against the prediction, bar 0.005.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw/I1025-win2
D=$1; NEWTAG=$2; SUB=$3
[ -n "$D" ] && [ -n "$NEWTAG" ] && [ -n "$SUB" ] || { echo "usage: kc95_scan.sh D NEWTAG SUBFOLDER"; exit 2; }
OUT=$BASE/$SUB; WOUT=D:/choptuik-i935-raw/I1025-win2/$SUB
EX=$OUT/exits_scan.txt; SUM=$OUT/summary_scan.txt
IN=$BASE/kc95_d22/inputs; WIN=D:/choptuik-i935-raw/I1025-win2/kc95_d22/inputs
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter
F4=$(printf "%.4f" $D); CAP=28800; NP=4
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1 D18_DIR=$WIN
mkdir -p $OUT
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc95 D $D scan refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $IN/d18_hybsign.py e089207a "d18_hybsign.py"
chk $IN/d185_scan_read.py 7c9d400f "d185_scan_read.py"
chk $IN/d18c_read.py 1383470f "d18c_read.py"
chk $IN/read_lower.py 89309d3c "read_lower.py"
chk $IN/repeat_check.py aaf598a9 "repeat_check.py"
chk $IN/leg_read.py 5cae2639 "leg_read.py"
chk $IN/pair2025.py e692c61d "pair2025.py"
for f in $OUT/scan_D${D}_p1.jsonl $OUT/scan.done $OUT/scan_refused.txt; do [ -e $f ] && { log "kc95 D $D scan refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
cd $OUT
"$PY" -I $IN/centre.py --selftest > selftest_centre.txt 2>&1; a0=$?
"$PY" -I $IN/centre.py --selftest --mutate > /dev/null 2>&1; a1=$?
"$PY" -I $IN/read_lower.py selftest > selftest_read_lower.txt 2>&1; r0=$?
"$PY" -I $IN/read_lower.py selftest --mutate=shift > /dev/null 2>&1; r1=$?
"$PY" -I $IN/read_lower.py selftest --mutate=round2 > /dev/null 2>&1; r2=$?
"$PY" -I $IN/repeat_check.py selftest > selftest_repeat_check.txt 2>&1; r3=$?
"$PY" -I $IN/leg_read.py selftest > selftest_leg_read.txt 2>&1; g0=$?
"$PY" -I $IN/leg_read.py selftest --mutate > /dev/null 2>&1; g1=$?
"$PY" -I $IN/pair2025.py --selftest > selftest_pair.txt 2>&1; p0=$?
"$PY" -I $IN/pair2025.py --selftest --break > /dev/null 2>&1; p1=$?
echo "$a0 $a1 $r0 $r1 $r2 $r3 $g0 $g1 $p0 $p1" > selftest_exits.txt
[ "$a0 $a1 $r0 $r1 $r2 $r3 $g0 $g1 $p0 $p1" = "0 1 0 1 1 0 0 1 0 1" ] || { log "kc95 D $D scan STOP: the selftests did not behave (centre $a0 $a1, read_lower $r0 $r1 $r2, repeat_check $r3, leg_read $g0 $g1, pair $p0 $p1; wanted 0 1 0 1 1 0 0 1 0 1)"; exit 1; }
log "kc95 D $D scan pins and selftests ok (centre, read_lower + shift + round2, repeat_check, leg_read, pair gate; each mutation exit 1)"
[ "$DRY" = 1 ] && { echo "DRY: waits for $OUT/regrid_accepted.txt and the k_c 87 root at D $D in roots87.txt"; exit 0; }
until [ -s $OUT/regrid_accepted.txt ]; do [ -e $OUT/regrid_refused.txt ] && { log "kc95 D $D scan: the regrid was refused: no scan"; exit 3; }; sleep 30; done
REC=$WOUT/rec_k95_D${F4}.jsonl; ST=$WOUT/sol_${NEWTAG}_D${F4}.npy
[ -s $OUT/rec_k95_D${F4}.jsonl ] && [ -s $OUT/sol_${NEWTAG}_D${F4}.npy ] || { log "kc95 D $D scan STOP: record or state missing"; exit 1; }
log "kc95 D $D scan: the regrid is accepted; waits for macm3's k_c 87 root at D $D (roots87.txt)"
tw=$(date +%s)
while :; do
  gh api -H "Accept: application/vnd.github.raw" repos/nmoinvaz/choptuik-large-d-raw/contents/I1025-macm3/kc87_leg_lambda/roots87.txt > $OUT/roots87.txt 2> $OUT/roots87.err
  out=$("$PY" -I $IN/centre.py $WOUT/roots87.txt $D); c=$?
  [ $c = 0 ] && break
  [ $c = 3 ] && { log "kc95 D $D scan STOP: roots87.txt has differing rows for D"; exit 1; }
  [ $(( $(date +%s) - tw )) -lt 43200 ] || { log "kc95 D $D scan STOP: no k_c 87 root for D $D after 12 h"; exit 1; }
  sleep 120
done
set -- $out; PRED=$1; C=$2; ROOT=$3
log "kc95 D $D scan: macm3's k_c 87 root at D $D is $ROOT; prediction $PRED, centre $C"
cp $OUT/roots87.txt $OUT/roots87_at_start.txt
V=($(awk -v c=$C 'BEGIN { printf "%.3f %.3f %.3f %.3f %.3f", c - 0.01, c - 0.005, c, c + 0.005, c + 0.01 }'))
LISTS=("${V[2]},${V[4]}" "${V[2]},${V[0]}" "${V[1]}" "${V[3]}")
echo "prediction $PRED centre $C root87 $ROOT lists: ${LISTS[*]}" > $OUT/scan_plan.txt
log "kc95 D $D scan lists: ${LISTS[*]}"
log "kc95 D $D scan waits for my other d18_hybsign scans to end and for memory (at least 4 x 3.6 GB + 4 GB free)"
tw=$(date +%s)
while :; do
  n=$(powershell -NoProfile -Command "@(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -match 'I1025-win2.*d18_hybsign.py' -and \$_.Name -match 'python' }).Count" | tr -d '\r')
  fm=$(powershell -NoProfile -Command "[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)" | tr -d '\r')
  [ "$n" = 0 ] && [ "$fm" -ge 18400 ] && break
  [ $(( $(date +%s) - tw )) -lt 21600 ] || { log "kc95 D $D scan STOP: the wait for threads and memory ended after 6 h ($n scans, $fm MB free)"; exit 1; }
  sleep 60
done
cd $WT/solver/matter || exit 1
scan() {  # N LAMS
  local N=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $WIN/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D${D}_p$N.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 1 thread)"; } > $OUT/scan_D${D}_p$N.log
  crun scan95_${F4}_p$N 0 $CAP d18_hybsign.py "$PY" -u $WIN/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D${D}_p$N.jsonl >> $OUT/scan_D${D}_p$N.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/scan_D${D}_p$N.log
  local n; n=$(grep -c '^{' $OUT/scan_D${D}_p$N.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_D${D}_p$N: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n points" >> $SUM
  log "scan95_${F4}_p$N exit $rc wall $w s capped $CAPPED"
}
for i in 1 2 3 4; do scan $i ${LISTS[$((i-1))]} & eval "q$i=\$!"; done
wait $q1 $q2 $q3 $q4
cd $OUT
for i in 1 2 3 4; do grep -E 'record system' scan_D${D}_p$i.log | head -1 | cut -c1-200 >> $SUM; done
cat scan_D${D}_p*.jsonl | "$PY" -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$WOUT/scan_D${D}_all.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $SUM
LO=$(awk -v c=$C 'BEGIN { printf "%.3f", c - 0.01 }'); HI=$(awk -v c=$C 'BEGIN { printf "%.3f", c + 0.01 }')
{ echo "=== read_lower.py $WOUT $LO $HI"; "$PY" -W ignore $IN/read_lower.py $WOUT $LO $HI; echo "read_lower exit $?"; echo "=== repeat_check.py (merged scan file)"; "$PY" -I $IN/repeat_check.py $OUT/scan_D${D}_all.jsonl; echo "repeat_check exit $?"; echo "=== pair2025.py (P1 and P2 first records)"; "$PY" -I $IN/pair2025.py scan_D${D}_p1.jsonl scan_D${D}_p2.jsonl; echo "pair exit $?"; } > read_lower.txt 2>&1
"$PY" -I $IN/leg_read.py read read_lower.txt $PRED 0.005 > leg_read.txt 2>&1
echo "kc95 D $D reading: $(grep -E '^hybrid signs|^robust changes|change \(|against the prediction' leg_read.txt | tr '\n' ' ' | cut -c1-500)" >> $SUM
log "kc95 D $D scan done: $(tail -n 2 $SUM | cut -c1-200 | tr '\n' ' ')"
touch $OUT/scan.done
exit 0
