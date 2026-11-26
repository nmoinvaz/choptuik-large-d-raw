#!/bin/bash
# #1025 kc135_d23 on win2 (the coordinator's hc of 2026-11-26 14:14 UTC), step 4: the scan of the accepted k_c 135 state at D 23.0 with the new scanner, d18_secant.py scan (wip/ell1-speed 92b9bf53, blob eb1396ad).
# Before: d18_secant.py selftest (exit 0) and its three mutations half, norobust, nosigncheck (exit 1 each); read_lower.py selftest (0) and --mutate=shift, --mutate=round2 (1 1); repeat_check.py selftest (0); pair2025.py selftest (0) and --break (1).
# Scan: lambda 0.04, 0.045, 0.05, 0.055 and a repeat of 0.045, FOUR processes of one thread, BelowNormal is not set (Normal, as the regrid): P1 0.04 then the repeat 0.045 | P2 0.045 | P3 0.05 | P4 0.055; cap 43200 s each by the exact root pid.
# Then read_lower.py (89309d3c) over 0.04 to 0.055, repeat_check.py and pair2025.py (the two 0.045 records), and a ln|det| table.
# usage: kc135_scan.sh   (DRY=1: pins, selftests, a 90 s probe of the scan command on the k_c 127 source; no waiting for the regrid)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw/I1025-win2
OUT=$BASE/kc135_d23; WOUT=D:/choptuik-i935-raw/I1025-win2/kc135_d23
IN=$OUT/inputs; WIN=$WOUT/inputs
SC=$OUT/scan; WSC=$WOUT/scan; SUM=$OUT/summary_scan.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
SWT=/d/choptuik-i1025secant92; SWTM=D:/choptuik-i1025secant92/solver/matter
NEW=l1kc135win2d23; D=23.0; CAP=43200
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$SWTM PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1 D18_DIR=$WIN/readers
mkdir -p $SC
refuse() { log "kc135 scan STOP: $*"; echo "kc135 scan STOP: $*" >> $SUM; echo "$*" > $OUT/scan_refused.txt; exit ${2:-1}; }
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc135 scan refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $SWT/solver/matter/d18_secant.py eb1396ad "d18_secant.py"
chk $SWT/solver/matter/ell_fastm.py 93f963f6 "ell_fastm.py"
chk $IN/readers/read_lower.py 89309d3c "read_lower.py"
chk $IN/readers/d185_scan_read.py 7c9d400f "d185_scan_read.py"
chk $IN/readers/d18c_read.py 1383470f "d18c_read.py"
chk $IN/readers/repeat_check.py aaf598a9 "repeat_check.py"
chk $IN/readers/pair2025.py e692c61d "pair2025.py"
[ "$(git -C $SWT rev-parse HEAD | cut -c1-8)" = 92b9bf53 ] || { log "kc135 scan refuse: the worktree is not at 92b9bf53"; bad=1; }
git -C $SWT diff --quiet 92b9bf533ff371247be642c47e067a9042cabed1 -- solver/matter || { log "kc135 scan refuse: the secant worktree's solver/matter is modified"; bad=1; }
for f in $SC/scan_D${D}_p1.jsonl $OUT/scan.done $OUT/scan_refused.txt; do [ -e $f ] && { log "kc135 scan refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
cd $OUT
ex=""
for m in "" --mutate=half --mutate=norobust --mutate=nosigncheck; do
  ( cd $SWT/solver/matter && "$PY" -u d18_secant.py selftest $m ) > selftest_d18_secant${m:+_${m#--mutate=}}.txt 2>&1; ex="$ex $?"
done
"$PY" -I $IN/readers/read_lower.py selftest > selftest_read_lower.txt 2>&1; ex="$ex $?"
"$PY" -I $IN/readers/read_lower.py selftest --mutate=shift > /dev/null 2>&1; ex="$ex $?"
"$PY" -I $IN/readers/read_lower.py selftest --mutate=round2 > /dev/null 2>&1; ex="$ex $?"
"$PY" -I $IN/readers/repeat_check.py selftest > selftest_repeat_check.txt 2>&1; ex="$ex $?"
"$PY" -I $IN/readers/pair2025.py --selftest > selftest_pair.txt 2>&1; ex="$ex $?"
"$PY" -I $IN/readers/pair2025.py --selftest --break > /dev/null 2>&1; ex="$ex $?"
echo "$ex" | sed 's/^ //' > selftest_scan_exits.txt
[ "$(cat selftest_scan_exits.txt)" = "0 1 1 1 0 1 1 0 0 1" ] || refuse "the selftests did not behave (d18_secant plain/half/norobust/nosigncheck, read_lower plain/shift/round2, repeat_check, pair plain/break: $(cat selftest_scan_exits.txt); wanted 0 1 1 1 0 1 1 0 0 1)"
log "kc135 scan pins and selftests ok (d18_secant selftest 0 and half, norobust, nosigncheck 1 1 1; read_lower 0 1 1; repeat_check 0; pair 0 1)"
if [ "$DRY" = 1 ]; then
  # a 90 s probe on the k_c 127 source: the scan command's syntax, its pin check and its record-system check (the cap kills it by the exact pid)
  mkdir -p $OUT/scan_probe; cd $SWT/solver/matter
  { echo "# probe $(date -u '+%F %T') UTC"; } > $OUT/scan_probe/probe.log
  crun scan_probe 0 90 d18_secant.py "$PY" -u $SWTM/d18_secant.py scan $WIN/src/l1kc127wind23.jsonl $WIN/src/sol_l1kc127wind23_D23.0000.npy $D 0.04 $WOUT/scan_probe/probe.jsonl --pin=7a1b150c,eea03461 >> $OUT/scan_probe/probe.log 2>&1
  grep -E "record system|NOT" $OUT/scan_probe/probe.log | head -2 | cut -c1-250
  [ -n "$(grep 'the record system' $OUT/scan_probe/probe.log)" ] || refuse "the 90 s probe did not print the record system line (see scan_probe/probe.log)"
  log "kc135 scan DRY: the probe on the k_c 127 source printed the record system line (capped at 90 s: $CAPPED)"; exit 0
fi
log "kc135 scan waits for the accepted k_c 135 state (regrid_accepted.txt)"
until [ -e $OUT/regrid_accepted.txt ]; do
  [ -e $OUT/regrid_refused.txt ] && refuse "the regrid was refused: $(cat $OUT/regrid_refused.txt | head -c 200)"
  sleep 30
done
SB=$(sed 's/.*state blob \([0-9a-f]*\).*/\1/' $OUT/regrid_accepted.txt); RB=$(sed 's/.*record blob \([0-9a-f]*\).*/\1/' $OUT/regrid_accepted.txt)
chk $OUT/sol_${NEW}_D23.0000.npy $SB "the accepted k_c 135 state"; chk $OUT/${NEW}.jsonl $RB "the accepted k_c 135 record"
[ $bad = 0 ] || refuse "the accepted state or record changed since the acceptance"
REC=$WOUT/${NEW}.jsonl; ST=$WOUT/sol_${NEW}_D23.0000.npy
log "kc135 scan: state $SB, record $RB; the four processes start one after another, 240 s apart, each when 14 GB of RAM is free (a k_c 127 process needs about 8 GB, winb; this machine has about 38 GB free with nothing running, so the first version's 46 GB gate could never open)"
freemb() { powershell -NoProfile -Command "[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)" | tr -d '\r'; }
LISTS=("0.04,0.045" "0.045" "0.05" "0.055")
echo "lists: ${LISTS[*]}" > $OUT/scan_plan.txt
cd $SWT/solver/matter || exit 1
scan() {  # N LAMS
  local N=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $SWTM/d18_secant.py scan $REC $ST $D $L $WSC/scan_D${D}_p$N.jsonl --pin=$SB,$RB (cwd $SWTM, 1 thread)"; } > $SC/scan_D${D}_p$N.log
  crun kc135scan_p$N 0 $CAP d18_secant.py "$PY" -u $SWTM/d18_secant.py scan $REC $ST $D $L $WSC/scan_D${D}_p$N.jsonl --pin=$SB,$RB >> $SC/scan_D${D}_p$N.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $SC/scan_D${D}_p$N.log
  local n; n=$(grep -c '^{' $SC/scan_D${D}_p$N.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_D${D}_p$N: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n points" >> $SUM
  log "kc135scan_p$N exit $rc wall $w s capped $CAPPED"
}
for i in 1 2 3 4; do
  tw=$(date +%s)
  while :; do
    fm=$(freemb); [ "$fm" -ge 14000 ] && break
    [ $(( $(date +%s) - tw )) -lt 21600 ] || refuse "the wait for memory before process $i ended after 6 h ($fm MB free)"
    sleep 60
  done
  log "kc135 scan: starting process $i (list ${LISTS[$((i-1))]}) with $(freemb) MB of free RAM"
  scan $i ${LISTS[$((i-1))]} & eval "q$i=\$!"
  [ $i = 4 ] || sleep 240
done
log "kc135 scan: all four processes started; free RAM $(freemb) MB"
wait $q1 $q2 $q3 $q4
cd $SC
for i in 1 2 3 4; do grep -E 'record system' scan_D${D}_p$i.log | head -1 | cut -c1-200 >> $SUM; done
cat scan_D${D}_p*.jsonl | "$PY" -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$WOUT/scan_D${D}_all.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $SUM
{ echo "=== read_lower.py $WSC 0.04 0.055"; "$PY" -W ignore $IN/readers/read_lower.py $WSC 0.04 0.055; echo "read_lower exit $?"; echo "=== repeat_check.py (merged scan file)"; "$PY" -I $IN/readers/repeat_check.py $OUT/scan_D${D}_all.jsonl; echo "repeat_check exit $?"; } > $OUT/read_lower.txt 2>&1
# the two 0.045 records (p2's and p1's second)
"$PY" -I -c "
import json
a = [json.loads(l) for l in open('$SC/scan_D${D}_p2.jsonl') if l.strip()][0]
b = [json.loads(l) for l in open('$SC/scan_D${D}_p1.jsonl') if l.strip()][-1]
open('$SC/_pair_a.jsonl', 'w').write(json.dumps(a) + '\n'); open('$SC/_pair_b.jsonl', 'w').write(json.dumps(b) + '\n')" 2>/dev/null
{ echo "=== pair2025.py (the two lambda 0.045 records: p2's and p1's second)"; "$PY" -I $IN/readers/pair2025.py $SC/_pair_a.jsonl $SC/_pair_b.jsonl; echo "pair exit $?"; } >> $OUT/read_lower.txt 2>&1
cat $OUT/scan_D${D}_all.jsonl | "$PY" -I -c "
import sys, json
rows = {}
for l in sys.stdin:
    if l.strip():
        r = json.loads(l); rows.setdefault(round(r['lam'], 4), []).append(r)
ls = sorted(rows)
print('lambda  hybrid  f64  robust  dln  ln|det| hybrid  ln|det| f64  sec')
for l in ls:
    for r in rows[l]:
        print('%+.4f  %+d  %+d  %s  %s  %.6f  %.6f  %s' % (l, r['sign'], r['f64_sign'], r.get('robust'), r.get('dln'), r['ln'], r['f64_ln'], r.get('sec')))" > $OUT/ln_table.txt 2>&1
echo "kc135 scan reading: $(grep -E '^hybrid signs|^float64 sign differs|^robust changes|robust change \(' $OUT/read_lower.txt | tr '\n' ' ' | cut -c1-900)" >> $SUM
log "kc135 scan done: $(tail -n 1 $SUM | cut -c1-300)"
touch $OUT/scan.done
exit 0
