#!/bin/bash
# #1025 kc95_d2225_low on win2 (the coordinator's hc of 2026-11-25 ~04:55 UTC): "a low-lambda scan of dh610's k_c 95 state at D 22.25 (raw I1025-dh610/kc95_d2225, tag l1kc95dh610d2225; pin by blob; kc95 check accepts it, controls 1 1).
# Scan lambda 0.02 to 0.18 by 0.02 plus the repeat of 0.10, and 0.20 to 0.40 by 0.04, 4 procs. Report every robust change by position and orientation. Reason: at k_c 87 a second root appeared at D 22.25 near lambda 0.11 ('- to +', macm3);
# at k_c 95 the lambda_1 root at 0.434 still reads '- to +', so either k_c 95 has no second root there yet or it sits elsewhere."
# usage: kc95_lowscan.sh   (DRY=1: pins, selftests, the fetch, the source acceptance and the plan; no scan)
# The 16 evaluations (0.02 .. 0.18 by 0.02 = 9, the repeat of 0.10 = 1, 0.20 .. 0.40 by 0.04 = 6) on FOUR processes of one thread, 4 each (the centre of the likely second root first): P1 0.10 0.14 0.24 0.36 | P2 0.10 (the repeat) 0.06 0.20 0.32 |
# P3 0.12 0.08 0.04 0.28 | P4 0.16 0.18 0.02 0.40. xfkappa's d18_hybsign.py (blob e089207a, unchanged; its first line is the record-system check, exit 3 if not). Caps 28800 s by the exact root pids. Then read_lower.py (89309d3c) over 0.02 to 0.40,
# repeat_check.py (aaf598a9) and pair2025.py (the first records of P1 and P2, the same lambda).
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw/I1025-win2
OUT=$BASE/kc95_d2225_low; WOUT=D:/choptuik-i935-raw/I1025-win2/kc95_d2225_low
EX=$OUT/exits_lowscan.txt; SUM=$OUT/summary_lowscan.txt
IN=$BASE/kc95_d22/inputs; WIN=D:/choptuik-i935-raw/I1025-win2/kc95_d22/inputs
CK=$BASE/kc95_leap/inputs
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter
D=22.25; TAG=l1kc95dh610d2225; SRCP=I1025-dh610/kc95_d2225; CAP=28800
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1 D18_DIR=$WIN
mkdir -p $OUT/in
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc95 low D $D refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $IN/d18_hybsign.py e089207a "d18_hybsign.py"
chk $IN/d185_scan_read.py 7c9d400f "d185_scan_read.py"
chk $IN/d18c_read.py 1383470f "d18c_read.py"
chk $IN/read_lower.py 89309d3c "read_lower.py"
chk $IN/repeat_check.py aaf598a9 "repeat_check.py"
chk $IN/pair2025.py e692c61d "pair2025.py"
chk $CK/kc95_syscheck_1025.py d487e628 "kc95_syscheck_1025.py"
chk $CK/kc87_syscheck_1025.py 6df5d960 "kc87_syscheck_1025.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "kc95 low D $D refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "kc95 low D $D refuse: solver code differs from 505d8399"; bad=1; }
for f in $OUT/scan_D${D}_p1.jsonl $OUT/scan.done $OUT/scan_refused.txt; do [ -e $f ] && { log "kc95 low D $D refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
refuse() { log "kc95 low D $D STOP: $*"; echo "kc95 low D $D STOP: $*" >> $SUM; echo "$*" > $OUT/scan_refused.txt; exit ${2:-1}; }
cd $OUT
"$PY" -I $IN/read_lower.py selftest > selftest_read_lower.txt 2>&1; r0=$?
"$PY" -I $IN/read_lower.py selftest --mutate=shift > /dev/null 2>&1; r1=$?
"$PY" -I $IN/read_lower.py selftest --mutate=round2 > /dev/null 2>&1; r2=$?
"$PY" -I $IN/repeat_check.py selftest > selftest_repeat_check.txt 2>&1; r3=$?
"$PY" -I $IN/pair2025.py --selftest > selftest_pair.txt 2>&1; p0=$?
"$PY" -I $IN/pair2025.py --selftest --break > /dev/null 2>&1; p1=$?
"$PY" -I $CK/kc95_syscheck_1025.py --selftest > selftest_kc95_syscheck.txt 2>&1; k0=$?
"$PY" -I $CK/kc87_syscheck_1025.py --selftest > selftest_kc87_syscheck.txt 2>&1; k1=$?
"$PY" -I $BASE/kc95_d22/fetch_macm3.py --selftest > selftest_fetch.txt 2>&1; f0=$?
"$PY" -I $BASE/kc95_d22/fetch_macm3.py --selftest --mutate > /dev/null 2>&1; f1=$?
echo "$r0 $r1 $r2 $r3 $p0 $p1 $k0 $k1 $f0 $f1" > selftest_exits.txt
[ "$r0 $r1 $r2 $r3 $p0 $p1 $k0 $k1 $f0 $f1" = "0 1 1 0 0 1 0 0 0 1" ] || refuse "the selftests did not behave (read_lower $r0 $r1 $r2, repeat_check $r3, pair $p0 $p1, kc95 check $k0, kc87 check $k1, fetch $f0 $f1; wanted 0 1 1 0 0 1 0 0 0 1)"
log "kc95 low D $D pins and selftests ok (read_lower + shift + round2, repeat_check, pair gate, kc95 and kc87 checks, fetch; each mutation exit 1)"
# the source: dh610's state and record, fetched by gh api (blob-checked against the listing), pinned by the blobs the order's raw commit names
"$PY" -I $BASE/kc95_d22/fetch_macm3.py $D $WOUT/in --path=$SRCP --tag=$TAG > fetch.log 2>&1 || refuse "fetch exit $? (see fetch.log)"
ST=$WOUT/in/sol_${TAG}_D22.2500.npy; REC=$WOUT/in/${TAG}.jsonl
bs=$(git hash-object --no-filters $OUT/in/sol_${TAG}_D22.2500.npy); br=$(git hash-object --no-filters $OUT/in/${TAG}.jsonl)
case "$bs" in d709a8c0*) ;; *) refuse "the state is blob $bs, not d709a8c0";; esac
case "$br" in e83e529e*) ;; *) refuse "the record file is blob $br, not e83e529e";; esac
"$PY" -I $CK/kc95_syscheck_1025.py $REC $ST $D $WTM > source_kc95_syscheck.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' source_kc95_syscheck.txt >> $SUM
[ $s = 0 ] || refuse "kc95_syscheck_1025.py does not accept dh610's state (exit $s)"
for m in F steps; do "$PY" -I $CK/kc95_syscheck_1025.py $REC $ST $D $WTM --mutate=$m > source_kc95_syscheck_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the control --mutate=$m did not exit 1"; done
"$PY" -I $CK/kc87_syscheck_1025.py $REC $ST $D $WTM > source_kc87_syscheck_refuses.txt 2>&1; [ $? = 1 ] || refuse "kc87_syscheck_1025.py did not refuse the k_c 95 state"
log "kc95 low D $D source accepted: dh610's state blob $bs, record file blob $br (kc95 check exit 0; --mutate=F and --mutate=steps exit 1; the k_c 87 check refuses)"
LISTS=("0.10,0.14,0.24,0.36" "0.10,0.06,0.20,0.32" "0.12,0.08,0.04,0.28" "0.16,0.18,0.02,0.40")
echo "lists: ${LISTS[*]}" > $OUT/scan_plan.txt
[ "$DRY" = 1 ] && { echo "DRY: lists ${LISTS[*]}"; log "kc95 low D $D DRY run ended before the scan"; exit 0; }
log "kc95 low D $D scan waits for my other d18_hybsign scans to end and for memory (at least 4 x 3.6 GB + 4 GB free)"
tw=$(date +%s)
while :; do
  n=$(powershell -NoProfile -Command "@(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -match 'I1025-win2.*d18_hybsign.py' -and \$_.Name -match 'python' }).Count" | tr -d '\r')
  fm=$(powershell -NoProfile -Command "[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)" | tr -d '\r')
  [ "$n" = 0 ] && [ "$fm" -ge 18400 ] && break
  [ $(( $(date +%s) - tw )) -lt 21600 ] || refuse "the wait for threads and memory ended after 6 h ($n scans, $fm MB free)"
  sleep 60
done
cd $WT/solver/matter || exit 1
scan() {  # N LAMS
  local N=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $WIN/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D${D}_p$N.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 1 thread)"; } > $OUT/scan_D${D}_p$N.log
  crun lowscan95_p$N 0 $CAP d18_hybsign.py "$PY" -u $WIN/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D${D}_p$N.jsonl >> $OUT/scan_D${D}_p$N.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/scan_D${D}_p$N.log
  local n; n=$(grep -c '^{' $OUT/scan_D${D}_p$N.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_D${D}_p$N: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n points" >> $SUM
  log "lowscan95_p$N exit $rc wall $w s capped $CAPPED"
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
{ echo "=== read_lower.py $WOUT 0.02 0.40"; "$PY" -W ignore $IN/read_lower.py $WOUT 0.02 0.40; echo "read_lower exit $?"; echo "=== repeat_check.py (merged scan file)"; "$PY" -I $IN/repeat_check.py $OUT/scan_D${D}_all.jsonl; echo "repeat_check exit $?"; echo "=== pair2025.py (P1 and P2 first records)"; "$PY" -I $IN/pair2025.py scan_D${D}_p1.jsonl scan_D${D}_p2.jsonl; echo "pair exit $?"; } > read_lower.txt 2>&1
echo "kc95 low D $D reading: $(grep -E '^hybrid signs|^float64 sign differs|^robust changes|robust change \(' read_lower.txt | tr '\n' ' ' | cut -c1-700)" >> $SUM
log "kc95 low D $D scan done: $(tail -n 1 $SUM | cut -c1-300)"
touch $OUT/scan.done
exit 0
