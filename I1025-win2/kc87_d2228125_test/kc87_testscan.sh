#!/bin/bash
# #1025 kc87_d2228125_test on win2 (the coordinator's hc of 2026-11-25 ~10:30 UTC): "Decide it with a test registered now: lambda -0.1990, -0.1985 and -0.1965 on the 3 free threads. Prediction from your zero fit (lc -0.1976, background slope -79.6, q -3.1),
# written in the README before the start: ln|det| at each point = the fit's background + ln|l - lc| within 0.05; a pole predicts the opposite sign of that term. Pass for 'zero' when all three are within 0.05 of the zero model and the sign changes between -0.1985
# and -0.1965; 'pole' when they follow the pole model; else undecided. No refit before reading." Same pinned state as ../kc87_d2228125_low, _neg and _fine. usage: kc87_testscan.sh   (DRY=1: pins, selftests, the fetch, the source acceptance and the plan; no scan).
# The 3 evaluations on THREE processes of one thread: P1 -0.1990 | P2 -0.1985 | P3 -0.1965. No wait for other d18_hybsign scans (the D 22.5 wide scan's last evaluation runs beside it, by order); the 18.4 GB free-memory wait stays. Caps 28800 s by the exact root pids.
# Then predict_check.py (registered before the scan; selftest and mutation in the preflight) reads the three points, read_lower.py over -0.1990 to -0.1965, and the joint reading with the three previous scans over -0.50 to 0.10.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw/I1025-win2
OUT=$BASE/kc87_d2228125_test; WOUT=D:/choptuik-i935-raw/I1025-win2/kc87_d2228125_test
EX=$OUT/exits_testscan.txt; SUM=$OUT/summary_testscan.txt
PREVLOW=$BASE/kc87_d2228125_low; PREVNEG=$BASE/kc87_d2228125_neg; PREVFINE=$BASE/kc87_d2228125_fine
IN=$BASE/kc95_d22/inputs; WIN=D:/choptuik-i935-raw/I1025-win2/kc95_d22/inputs
CK=$BASE/kc95_leap/inputs
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter
D=22.28125; TAG=l1kc87Lmacm3b2; SRCP=I1025-macm3/kc87_leg2/b2; CAP=28800; F4=$(printf "%.4f" $D)
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1 D18_DIR=$WIN
mkdir -p $OUT/in
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc87 test D $D refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $IN/d18_hybsign.py e089207a "d18_hybsign.py"
chk $IN/d185_scan_read.py 7c9d400f "d185_scan_read.py"
chk $IN/d18c_read.py 1383470f "d18c_read.py"
chk $IN/read_lower.py 89309d3c "read_lower.py"
chk $IN/repeat_check.py aaf598a9 "repeat_check.py"
chk $IN/pair2025.py e692c61d "pair2025.py"
chk $CK/kc95_syscheck_1025.py d487e628 "kc95_syscheck_1025.py"
chk $CK/kc87_syscheck_1025.py 6df5d960 "kc87_syscheck_1025.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "kc87 test D $D refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "kc87 test D $D refuse: solver code differs from 505d8399"; bad=1; }
for f in $OUT/scan_D${D}_p1.jsonl $OUT/scan.done $OUT/scan_refused.txt; do [ -e $f ] && { log "kc87 test D $D refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
refuse() { log "kc87 test D $D STOP: $*"; echo "kc87 test D $D STOP: $*" >> $SUM; echo "$*" > $OUT/scan_refused.txt; exit ${2:-1}; }
cd $OUT
"$PY" -I $IN/read_lower.py selftest > selftest_read_lower.txt 2>&1; r0=$?
"$PY" -I $IN/read_lower.py selftest --mutate=shift > /dev/null 2>&1; r1=$?
"$PY" -I $IN/read_lower.py selftest --mutate=round2 > /dev/null 2>&1; r2=$?
"$PY" -I $IN/repeat_check.py selftest > selftest_repeat_check.txt 2>&1; r3=$?
"$PY" -I $IN/pair2025.py --selftest > selftest_pair.txt 2>&1; p0=$?
"$PY" -I $IN/pair2025.py --selftest --break > /dev/null 2>&1; p1=$?
"$PY" -I $OUT/predict_check.py --selftest > selftest_predict.txt 2>&1; q0=$?
"$PY" -I $OUT/predict_check.py --selftest --mutate > /dev/null 2>&1; q1=$?
"$PY" -I $CK/kc95_syscheck_1025.py --selftest > selftest_kc95_syscheck.txt 2>&1; k0=$?
"$PY" -I $CK/kc87_syscheck_1025.py --selftest > selftest_kc87_syscheck.txt 2>&1; k1=$?
"$PY" -I $BASE/kc95_d22/fetch_macm3.py --selftest > selftest_fetch.txt 2>&1; f0=$?
"$PY" -I $BASE/kc95_d22/fetch_macm3.py --selftest --mutate > /dev/null 2>&1; f1=$?
echo "$r0 $r1 $r2 $r3 $p0 $p1 $k0 $k1 $f0 $f1 $q0 $q1" > selftest_exits.txt
[ "$r0 $r1 $r2 $r3 $p0 $p1 $k0 $k1 $f0 $f1 $q0 $q1" = "0 1 1 0 0 1 0 0 0 1 0 1" ] || refuse "the selftests did not behave (read_lower $r0 $r1 $r2, repeat_check $r3, pair $p0 $p1, kc95 check $k0, kc87 check $k1, fetch $f0 $f1, predict_check $q0 $q1; wanted 0 1 1 0 0 1 0 0 0 1 0 1)"
log "kc87 test D $D pins and selftests ok (read_lower + shift + round2, repeat_check, pair gate, kc95 and kc87 checks, fetch; each mutation exit 1)"
# the source: macm3's part b2 state and record, fetched by gh api (blob-checked against the listing); pinned by the state's blob and by the hash of the D row of the record file (the file's blob changes with every push of the leg)
"$PY" -I $BASE/kc95_d22/fetch_macm3.py $D $WOUT/in --path=$SRCP --tag=$TAG > fetch.log 2>&1 || refuse "fetch exit $? (see fetch.log)"
ST=$WOUT/in/sol_${TAG}_D${F4}.npy; REC=$WOUT/in/${TAG}.jsonl
bs=$(git hash-object --no-filters $OUT/in/sol_${TAG}_D${F4}.npy); br=$(git hash-object --no-filters $OUT/in/${TAG}.jsonl)
case "$bs" in 3ce8bc2e*) ;; *) refuse "the state is blob $bs, not 3ce8bc2e";; esac
rowsha=$("$PY" -I -c "
import json, hashlib
for l in open('$REC', 'rb'):
    if l.strip() and abs(json.loads(l)['D'] - $D) < 1e-9:
        print(hashlib.sha1(l.rstrip(b'\r\n')).hexdigest())" | tr -d '
' | tail -n 1)
case "$rowsha" in 0eb8d22e*) ;; *) refuse "the D row of the record file hashes to $rowsha, not 0eb8d22e";; esac
"$PY" -I $CK/kc87_syscheck_1025.py $REC $ST $D $WTM > source_kc87_syscheck.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' source_kc87_syscheck.txt >> $SUM
[ $s = 0 ] || refuse "kc87_syscheck_1025.py does not accept macm3's state (exit $s)"
for m in F steps; do "$PY" -I $CK/kc87_syscheck_1025.py $REC $ST $D $WTM --mutate=$m > source_kc87_syscheck_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the control --mutate=$m did not exit 1"; done
"$PY" -I $CK/kc95_syscheck_1025.py $REC $ST $D $WTM > source_kc95_syscheck_refuses.txt 2>&1; [ $? = 1 ] || refuse "kc95_syscheck_1025.py did not refuse the k_c 87 state"
log "kc87 test D $D source accepted: macm3's state blob $bs, the D row hash $rowsha, record file blob $br at the fetch (kc87 check exit 0; --mutate=F and --mutate=steps exit 1; the k_c 95 check refuses)"
LISTS=("-0.1990" "-0.1985" "-0.1965")
echo "lists: ${LISTS[*]}" > $OUT/scan_plan.txt
[ "$DRY" = 1 ] && { echo "DRY: lists ${LISTS[*]}"; log "kc87 test D $D DRY run ended before the scan"; exit 0; }
log "kc87 test D $D scan waits for memory only (at least 18.4 GB free; no wait for other d18_hybsign scans: the D 22.5 wide scan runs beside it, by order)"
tw=$(date +%s)
while :; do
  fm=$(powershell -NoProfile -Command "[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)" | tr -d '')
  [ "$fm" -ge 18400 ] && break
  [ $(( $(date +%s) - tw )) -lt 21600 ] || refuse "the wait for memory ended after 6 h ($fm MB free)"
  sleep 60
done
cd $WT/solver/matter || exit 1
scan() {  # N LAMS
  local N=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $WIN/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D${D}_p$N.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 1 thread)"; } > $OUT/scan_D${D}_p$N.log
  crun testscan87_p$N 0 $CAP d18_hybsign.py "$PY" -u $WIN/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D${D}_p$N.jsonl >> $OUT/scan_D${D}_p$N.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/scan_D${D}_p$N.log
  local n; n=$(grep -c '^{' $OUT/scan_D${D}_p$N.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_D${D}_p$N: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n points" >> $SUM
  log "testscan87_p$N exit $rc wall $w s capped $CAPPED"
}
for i in 1 2 3; do scan $i ${LISTS[$((i-1))]} & eval "q$i=\$!"; done
wait $q1 $q2 $q3
cd $OUT
for i in 1 2 3; do grep -E 'record system' scan_D${D}_p$i.log | head -1 | cut -c1-200 >> $SUM; done
cat scan_D${D}_p*.jsonl | "$PY" -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$WOUT/scan_D${D}_all.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $SUM
{ echo "=== predict_check.py (the registered test)"; "$PY" -I $OUT/predict_check.py $WOUT; echo "predict_check exit $?"; echo "=== read_lower.py $WOUT -0.1990 -0.1965 (this scan alone)"; "$PY" -W ignore $IN/read_lower.py $WOUT -0.1990 -0.1965; echo "read_lower exit $?"; } > read_lower.txt 2>&1
mkdir -p joint
for i in 1 2 3 4; do [ -e $PREVLOW/scan_D${D}_p$i.jsonl ] && cp $PREVLOW/scan_D${D}_p$i.jsonl joint/scan_D${D}_low_p$i.jsonl; [ -e $PREVNEG/scan_D${D}_p$i.jsonl ] && cp $PREVNEG/scan_D${D}_p$i.jsonl joint/scan_D${D}_neg_p$i.jsonl; [ -e $PREVFINE/scan_D${D}_p$i.jsonl ] && cp $PREVFINE/scan_D${D}_p$i.jsonl joint/scan_D${D}_fine_p$i.jsonl; done
for i in 1 2 3; do cp scan_D${D}_p$i.jsonl joint/scan_D${D}_test_p$i.jsonl; done
{ echo "=== joint read_lower.py joint -0.50 0.10 (this scan and the low, neg and fine scans; the rows's rows as of now)"; D18_DIR=$WIN "$PY" -W ignore $IN/read_lower.py $WOUT/joint -0.50 0.10; echo "read_lower exit $?"; } > joint/read_lower_joint.txt 2>&1
cat joint/scan_D${D}_*_p*.jsonl | "$PY" -I -c "
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
    print('%+.3f  %+d  %+d  %.4f  %.4f  %.1f' % (l, r['sign'], r['f64_sign'], r['ln'], r['f64_ln'], sl))" > joint/ln_table.txt 2>&1
echo "kc87 test D $D registered test: $(grep -E '^PRIMARY|^SECONDARY' read_lower.txt | tr '\n' ' ')| joint reading: $(grep -E '^hybrid signs|^float64 sign differs|^robust changes|robust change \(' joint/read_lower_joint.txt | tr '\n' ' ' | cut -c1-700)" >> $SUM
log "kc87 test D $D scan done: $(tail -n 1 $SUM | cut -c1-300)"
touch $OUT/scan.done
exit 0
