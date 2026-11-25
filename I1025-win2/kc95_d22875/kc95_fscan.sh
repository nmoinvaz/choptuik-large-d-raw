#!/bin/bash
# #1025 kc95_d22875 / kc95_d23 on win2, the F scan after the k_c 95 regrid (the coordinator's hc of 25 Nov ~12:50 UTC): "then a scan lambda -0.06 to 0.30 by 0.02 plus the repeat of 0.10, 4 procs." usage: kc95_fscan.sh D NEWTAG SUBFOLDER   (DRY=1: pins, selftests, the plan)
# The 20 evaluations (19 lambdas -0.06 .. 0.30 by 0.02 and the repeat of 0.10), central values first, on FOUR processes of one thread: P1 0.10 0.14 0.24 0.28 0.00 | P2 0.10 (the repeat) 0.20 0.26 0.30 -0.02 | P3 0.18 0.22 0.08 0.04 -0.04 | P4 0.16 0.12 0.06 0.02 -0.06.
# Waits for SUB/regrid_accepted.txt (exit 3 if regrid_refused.txt appears) and for 18.4 GB free memory (no wait for other scans: two lanes run side by side, by order). xfkappa's d18_hybsign.py (e089207a, unchanged; its first line is the record-system check, exit 3 if not).
# Caps 28800 s by the exact root pids. Then read_lower.py (89309d3c) over -0.06 to 0.30, repeat_check.py (aaf598a9), pair2025.py (P1 and P2 first records), and a ln|det| table to four decimals. SRC_NOTE (env) is written into the summary as the source's quality note.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw/I1025-win2
D=$1; NEWTAG=$2; SUB=$3
SRC_NOTE=${SRC_NOTE//_/ }   # the note comes with underscores for spaces (the launcher cannot carry quotes)
[ -n "$D" ] && [ -n "$NEWTAG" ] && [ -n "$SUB" ] || { echo "usage: kc95_fscan.sh D NEWTAG SUBFOLDER"; exit 2; }
OUT=$BASE/$SUB; WOUT=D:/choptuik-i935-raw/I1025-win2/$SUB
EX=$OUT/exits_fscan.txt; SUM=$OUT/summary_fscan.txt
IN=$BASE/kc95_d22/inputs; WIN=D:/choptuik-i935-raw/I1025-win2/kc95_d22/inputs
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter
F4=$(printf "%.4f" $D); CAP=28800
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1 D18_DIR=$WIN
mkdir -p $OUT
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc95 F D $D refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $IN/d18_hybsign.py e089207a "d18_hybsign.py"
chk $IN/d185_scan_read.py 7c9d400f "d185_scan_read.py"
chk $IN/d18c_read.py 1383470f "d18c_read.py"
chk $IN/read_lower.py 89309d3c "read_lower.py"
chk $IN/repeat_check.py aaf598a9 "repeat_check.py"
chk $IN/pair2025.py e692c61d "pair2025.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "kc95 F D $D refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "kc95 F D $D refuse: solver code differs from 505d8399"; bad=1; }
for f in $OUT/scan_D${D}_p1.jsonl $OUT/scan.done $OUT/scan_refused.txt; do [ -e $f ] && { log "kc95 F D $D refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
refuse() { log "kc95 F D $D STOP: $*"; echo "kc95 F D $D STOP: $*" >> $SUM; echo "$*" > $OUT/scan_refused.txt; exit ${2:-1}; }
cd $OUT
"$PY" -I $IN/read_lower.py selftest > selftest_read_lower.txt 2>&1; r0=$?
"$PY" -I $IN/read_lower.py selftest --mutate=shift > /dev/null 2>&1; r1=$?
"$PY" -I $IN/read_lower.py selftest --mutate=round2 > /dev/null 2>&1; r2=$?
"$PY" -I $IN/repeat_check.py selftest > selftest_repeat_check.txt 2>&1; r3=$?
"$PY" -I $IN/pair2025.py --selftest > selftest_pair.txt 2>&1; p0=$?
"$PY" -I $IN/pair2025.py --selftest --break > /dev/null 2>&1; p1=$?
echo "$r0 $r1 $r2 $r3 $p0 $p1" > selftest_wide_exits.txt
[ "$r0 $r1 $r2 $r3 $p0 $p1" = "0 1 1 0 0 1" ] || refuse "the selftests did not behave (read_lower $r0 $r1 $r2, repeat_check $r3, pair $p0 $p1; wanted 0 1 1 0 0 1)"
LISTS=("0.10,0.14,0.24,0.28,0.00" "0.10,0.20,0.26,0.30,-0.02" "0.18,0.22,0.08,0.04,-0.04" "0.16,0.12,0.06,0.02,-0.06")
echo "lists: ${LISTS[*]}" > $OUT/scan_plan.txt
log "kc95 F D $D pins and selftests ok (read_lower + shift + round2, repeat_check, pair gate; each mutation exit 1); lists ${LISTS[*]}"
[ "$DRY" = 1 ] && { echo "DRY: lists ${LISTS[*]}"; exit 0; }
log "kc95 F D $D waits for regrid_accepted.txt and for memory (18.4 GB free); source note: ${SRC_NOTE:-none}"
echo "source note: ${SRC_NOTE:-none}" >> $SUM
until [ -s $OUT/regrid_accepted.txt ]; do [ -e $OUT/regrid_refused.txt ] && { log "kc95 F D $D: the regrid was refused: no scan"; exit 3; }; sleep 30; done
REC=$WOUT/rec_k95_D${F4}.jsonl; ST=$WOUT/sol_${NEWTAG}_D${F4}.npy
[ -s $OUT/rec_k95_D${F4}.jsonl ] && [ -s $OUT/sol_${NEWTAG}_D${F4}.npy ] || refuse "record or state missing"
log "kc95 F D $D: the regrid is accepted (state blob $(git hash-object --no-filters $OUT/sol_${NEWTAG}_D${F4}.npy | cut -c1-8), record blob $(git hash-object --no-filters $OUT/rec_k95_D${F4}.jsonl | cut -c1-8))"
tw=$(date +%s)
while :; do
  n=$(powershell -NoProfile -Command "@(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -match 'I1025-win2.*d18_hybsign.py' -and \$_.Name -match 'python' }).Count" | tr -d '\r')
  fm=$(powershell -NoProfile -Command "[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)" | tr -d '\r')
  [ "$fm" -ge 18400 ] && break
  [ $(( $(date +%s) - tw )) -lt 21600 ] || refuse "the wait for memory ended after 6 h ($fm MB free)"
  sleep 60
done
cd $WT/solver/matter || exit 1
scan() {  # N LAMS
  local N=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $WIN/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D${D}_p$N.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 1 thread)"; } > $OUT/scan_D${D}_p$N.log
  crun fscan95_p$N 0 $CAP d18_hybsign.py "$PY" -u $WIN/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D${D}_p$N.jsonl >> $OUT/scan_D${D}_p$N.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/scan_D${D}_p$N.log
  local n; n=$(grep -c '^{' $OUT/scan_D${D}_p$N.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_D${D}_p$N: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n points" >> $SUM
  log "fscan95_p$N exit $rc wall $w s capped $CAPPED"
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
{ echo "=== read_lower.py $WOUT -0.06 0.30"; "$PY" -W ignore $IN/read_lower.py $WOUT -0.06 0.30; echo "read_lower exit $?"; echo "=== repeat_check.py (merged scan file)"; "$PY" -I $IN/repeat_check.py $OUT/scan_D${D}_all.jsonl; echo "repeat_check exit $?"; echo "=== pair2025.py (P1 and P2 first records)"; "$PY" -I $IN/pair2025.py scan_D${D}_p1.jsonl scan_D${D}_p2.jsonl; echo "pair exit $?"; } > read_lower.txt 2>&1
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
echo "kc95 F D $D reading: $(grep -E '^hybrid signs|^float64 sign differs|^robust changes|robust change \(' read_lower.txt | tr '\n' ' ' | cut -c1-900)" >> $SUM
log "kc95 F D $D scan done: $(tail -n 1 $SUM | cut -c1-300)"
touch $OUT/scan.done
exit 0
