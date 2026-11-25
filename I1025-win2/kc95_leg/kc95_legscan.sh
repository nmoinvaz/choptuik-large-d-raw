#!/bin/bash
# #1025 kc95_leg on win2, the scan at one new point of the k_c 95 leg (the coordinator's hc of 2026-11-25 ~20:00 UTC): "Then scan lambda -0.10 to 0.06 by 0.02 plus a repeat at D 23.0625 and D 23.125."
# usage: kc95_legscan.sh D   (DRY=1: pins, selftests and the plan; no waiting)   e.g. kc95_legscan.sh 23.0625
# Waits for the leap's record row of D and its state (copied into states/ by the leap driver), accepts them with kc95_syscheck_1025.py (selftest 0, accepts, --mutate=F and --mutate=steps exit 1, the k_c 87 check refuses), then runs
# d18_hybsign.py (e089207a, unchanged; its first line is the record-system check, exit 3 if not): 10 evaluations (lambda -0.10 to 0.06 by 0.02, nine values, and the repeat of -0.04 on its own process) on FOUR processes of one thread:
# P1 -0.04 -0.06 0.02 | P2 -0.04 (the repeat) -0.08 0.04 | P3 -0.02 -0.10 | P4 0.00 0.06; caps 28800 s by the exact root pids; waits for 18.4 GB free memory only. Then read_lower.py (89309d3c) over -0.10 to 0.06, repeat_check.py, pair2025.py (P1 and P2 first records)
# and a ln|det| table to four decimals. SRC_NOTE (below) is the quality note for every table of this leg.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw/I1025-win2
D=$1
[ -n "$D" ] || { echo "usage: kc95_legscan.sh D"; exit 2; }
LEG=$BASE/kc95_leg; WLEG=D:/choptuik-i935-raw/I1025-win2/kc95_leg
OUT=$LEG/scan_D$D; WOUT=$WLEG/scan_D$D
EX=$OUT/exits_legscan.txt; SUM=$OUT/summary_legscan.txt
IN=$BASE/kc95_d22/inputs; WIN=D:/choptuik-i935-raw/I1025-win2/kc95_d22/inputs
CK=$LEG/inputs; WCK=$WLEG/inputs
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k95leg; WTM=D:/choptuik-i1025k95leg/solver/matter
TAG=l1kc95Lw1025m; CAP=28800
NOTE="descends from the REDUCED QUALITY D 23.0 source (part c2, constraint 1.0496e-2 at the k_c 87 source); rows above 1e-2 flagged"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1 D18_DIR=$WIN
mkdir -p $OUT
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "legscan D $D refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $IN/d18_hybsign.py e089207a "d18_hybsign.py"
chk $IN/d185_scan_read.py 7c9d400f "d185_scan_read.py"
chk $IN/d18c_read.py 1383470f "d18c_read.py"
chk $IN/read_lower.py 89309d3c "read_lower.py"
chk $IN/repeat_check.py aaf598a9 "repeat_check.py"
chk $IN/pair2025.py e692c61d "pair2025.py"
chk $CK/kc95_syscheck_1025.py d487e628 "kc95_syscheck_1025.py"
chk $CK/kc87_syscheck_1025.py 6df5d960 "kc87_syscheck_1025.py"
chk $WT/solver/matter/ell_leap.py 5816d7b3 "ell_leap.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = edf49057 ] || { log "legscan D $D refuse: the worktree is not at edf49057"; bad=1; }
for f in $OUT/scan_D${D}_p1.jsonl $OUT/scan.done $OUT/scan_refused.txt $OUT/accepted.txt; do [ -e $f ] && { log "legscan D $D refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
refuse() { log "legscan D $D STOP: $*"; echo "legscan D $D STOP: $*" >> $SUM; echo "$*" > $OUT/scan_refused.txt; exit ${2:-1}; }
cd $OUT
"$PY" -I $IN/read_lower.py selftest > selftest_read_lower.txt 2>&1; r0=$?
"$PY" -I $IN/read_lower.py selftest --mutate=shift > /dev/null 2>&1; r1=$?
"$PY" -I $IN/read_lower.py selftest --mutate=round2 > /dev/null 2>&1; r2=$?
"$PY" -I $IN/repeat_check.py selftest > selftest_repeat_check.txt 2>&1; r3=$?
"$PY" -I $IN/pair2025.py --selftest > selftest_pair.txt 2>&1; p0=$?
"$PY" -I $IN/pair2025.py --selftest --break > /dev/null 2>&1; p1=$?
"$PY" -I $CK/kc95_syscheck_1025.py --selftest > selftest_kc95_syscheck.txt 2>&1; k0=$?
"$PY" -I $CK/kc87_syscheck_1025.py --selftest > selftest_kc87_syscheck.txt 2>&1; k1=$?
echo "$r0 $r1 $r2 $r3 $p0 $p1 $k0 $k1" > selftest_exits.txt
[ "$r0 $r1 $r2 $r3 $p0 $p1 $k0 $k1" = "0 1 1 0 0 1 0 0" ] || refuse "the selftests did not behave (read_lower $r0 $r1 $r2, repeat_check $r3, pair $p0 $p1, kc95 check $k0, kc87 check $k1; wanted 0 1 1 0 0 1 0 0)"
LISTS=("-0.04,-0.06,0.02" "-0.04,-0.08,0.04" "-0.02,-0.10" "0.00,0.06")
echo "lists: ${LISTS[*]}" > $OUT/scan_plan.txt
log "legscan D $D pins and selftests ok (read_lower + shift + round2, repeat_check, pair gate, kc95 and kc87 checks; each mutation exit 1); lists ${LISTS[*]}"
[ "$DRY" = 1 ] && { echo "DRY: D $D lists ${LISTS[*]}"; exit 0; }
log "legscan D $D waits for the leap's row and state of D $D (states/ of the leg folder)"
REC=$WLEG/states/$TAG.jsonl
ST=""
until [ -n "$ST" ]; do
  for n in $LEG/states/sol_${TAG}_D$(printf "%.6f" $D).npy $LEG/states/sol_${TAG}_D$(printf "%.4f" $D).npy; do
    [ -e $n ] && "$PY" -I -c "
import json, sys
rows = [json.loads(l) for l in open('$LEG/states/$TAG.jsonl') if l.strip()]
sys.exit(0 if any(abs(r['D'] - $D) < 1e-9 for r in rows) else 1)" 2>/dev/null && { ST=$WLEG/states/$(basename $n); break; }
  done
  [ -e $LEG/STOP_scans.txt ] && refuse "STOP_scans.txt exists"
  [ -n "$ST" ] || sleep 60
done
sleep 30   # the copier copies a state once it is 30 s old; the record row and the state are both in states/ now
log "legscan D $D: the leap's row and state are there ($(basename $ST), blob $(git hash-object --no-filters $LEG/states/$(basename $ST) | cut -c1-8))"
"$PY" -I $WCK/kc95_syscheck_1025.py $REC $ST $D $WTM > source_kc95_syscheck.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' source_kc95_syscheck.txt >> $SUM
[ $s = 0 ] || refuse "kc95_syscheck_1025.py does not accept the leap's state (exit $s)"
for m in F steps; do "$PY" -I $WCK/kc95_syscheck_1025.py $REC $ST $D $WTM --mutate=$m > source_kc95_syscheck_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the control --mutate=$m did not exit 1"; done
"$PY" -I $WCK/kc87_syscheck_1025.py $REC $ST $D $WTM > source_kc87_syscheck_refuses.txt 2>&1; [ $? = 1 ] || refuse "kc87_syscheck_1025.py did not refuse the k_c 95 state"
echo "accepted $(date -u '+%F %T') UTC: state $(basename $ST) blob $(git hash-object --no-filters $LEG/states/$(basename $ST) | cut -c1-8)" > $OUT/accepted.txt
log "legscan D $D: the leap's state is accepted by kc95_syscheck_1025.py (controls 1 1; the k_c 87 check refuses); the scan waits for memory"
echo "quality note: $NOTE" >> $SUM
tw=$(date +%s)
while :; do
  fm=$(powershell -NoProfile -Command "[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)" | tr -d '\r')
  [ "$fm" -ge 18400 ] && break
  [ $(( $(date +%s) - tw )) -lt 21600 ] || refuse "the wait for memory ended after 6 h ($fm MB free)"
  sleep 60
done
cd $WT/solver/matter || exit 1
scan() {  # N LAMS
  local N=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $WIN/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D${D}_p$N.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 1 thread)"; } > $OUT/scan_D${D}_p$N.log
  crun legscan_${D}_p$N 0 $CAP d18_hybsign.py "$PY" -u $WIN/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D${D}_p$N.jsonl >> $OUT/scan_D${D}_p$N.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/scan_D${D}_p$N.log
  local n; n=$(grep -c '^{' $OUT/scan_D${D}_p$N.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_D${D}_p$N: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n points" >> $SUM
  log "legscan_${D}_p$N exit $rc wall $w s capped $CAPPED"
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
{ echo "=== read_lower.py $WOUT -0.10 0.06"; "$PY" -W ignore $IN/read_lower.py $WOUT -0.10 0.06; echo "read_lower exit $?"; echo "=== repeat_check.py (merged scan file)"; "$PY" -I $IN/repeat_check.py $OUT/scan_D${D}_all.jsonl; echo "repeat_check exit $?"; echo "=== pair2025.py (P1 and P2 first records)"; "$PY" -I $IN/pair2025.py scan_D${D}_p1.jsonl scan_D${D}_p2.jsonl; echo "pair exit $?"; } > read_lower.txt 2>&1
cat scan_D${D}_all.jsonl | "$PY" -I -c "
import sys, json
rows = {}
for l in sys.stdin:
    if l.strip():
        r = json.loads(l); rows.setdefault(round(r['lam'], 4), []).append(r)
ls = sorted(rows)
print('lambda  hybrid  f64  ln|det| hybrid  ln|det| f64  slope(to next, per unit lambda)')
for i, l in enumerate(ls):
    r = rows[l][0]
    sl = (rows[ls[i+1]][0]['ln'] - r['ln']) / (ls[i+1] - l) if i + 1 < len(ls) else float('nan')
    print('%+.4f  %+d  %+d  %.4f  %.4f  %.1f' % (l, r['sign'], r['f64_sign'], r['ln'], r['f64_ln'], sl))" > ln_table.txt 2>&1
echo "legscan D $D reading: $(grep -E '^hybrid signs|^float64 sign differs|^robust changes|robust change \(' read_lower.txt | tr '\n' ' ' | cut -c1-900)" >> $SUM
log "legscan D $D scan done: $(tail -n 1 $SUM | cut -c1-300)"
touch $OUT/scan.done
exit 0
