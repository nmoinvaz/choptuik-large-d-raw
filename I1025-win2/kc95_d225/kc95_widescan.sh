#!/bin/bash
# #1025 kc95_d225 on win2, the wide scan after the k_c 95 regrid at D 22.5 (the coordinator's hc of 2026-11-25 ~06:00 UTC): "no centred scan at D 22.5: under reading (ii) lambda_1 may already be negative there. When its turn comes, scan wide:
# lambda -0.10 to 0.50 by 0.04 plus the repeat of 0.14, 4 procs; report every robust change with orientation. I will narrow it if the D 22.28125 reading settles (i) vs (ii) first." and the earlier "Priority after that: the D 22.28125 low scan
# first, then the D 22.5 scan." usage: kc95_widescan.sh   (DRY=1: pins, selftests and the plan; no waiting)
# Waits for regrid_accepted.txt of this folder (exit 3 if regrid_refused.txt appears), for the D 22.28125 low scan to be done (../kc87_d2228125_low/scan.done, or its scan_refused.txt), for my other d18_hybsign scans to end and for 18.4 GB free.
# The 17 evaluations (-0.10 to 0.50 by 0.04 = 16, and the repeat of 0.14) on FOUR processes of one thread: P1 0.14 -0.10 0.18 0.34 0.50 | P2 0.14 (the repeat) -0.06 0.22 0.38 | P3 -0.02 0.10 0.26 0.42 | P4 0.02 0.06 0.30 0.46.
# xfkappa's d18_hybsign.py (blob e089207a, unchanged; its first line is the record-system check, exit 3 if not). Caps 28800 s by the exact root pids. Then read_lower.py (89309d3c) over -0.10 to 0.50, repeat_check.py (aaf598a9) and pair2025.py (P1 and P2 first records).
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw/I1025-win2
OUT=$BASE/kc95_d225; WOUT=D:/choptuik-i935-raw/I1025-win2/kc95_d225
EX=$OUT/exits_widescan.txt; SUM=$OUT/summary_widescan.txt
IN=$BASE/kc95_d22/inputs; WIN=D:/choptuik-i935-raw/I1025-win2/kc95_d22/inputs
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter
D=22.5; NEWTAG=l1kc95win2d225; F4=$(printf "%.4f" $D); CAP=28800
LOWDONE=$BASE/kc87_d2228125_low/scan.done; LOWREF=$BASE/kc87_d2228125_low/scan_refused.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1 D18_DIR=$WIN
mkdir -p $OUT
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc95 wide D $D refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $IN/d18_hybsign.py e089207a "d18_hybsign.py"
chk $IN/d185_scan_read.py 7c9d400f "d185_scan_read.py"
chk $IN/d18c_read.py 1383470f "d18c_read.py"
chk $IN/read_lower.py 89309d3c "read_lower.py"
chk $IN/repeat_check.py aaf598a9 "repeat_check.py"
chk $IN/pair2025.py e692c61d "pair2025.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "kc95 wide D $D refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "kc95 wide D $D refuse: solver code differs from 505d8399"; bad=1; }
for f in $OUT/scan_D${D}_p1.jsonl $OUT/scan.done $OUT/scan_refused.txt; do [ -e $f ] && { log "kc95 wide D $D refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
refuse() { log "kc95 wide D $D STOP: $*"; echo "kc95 wide D $D STOP: $*" >> $SUM; echo "$*" > $OUT/scan_refused.txt; exit ${2:-1}; }
cd $OUT
"$PY" -I $IN/read_lower.py selftest > selftest_read_lower.txt 2>&1; r0=$?
"$PY" -I $IN/read_lower.py selftest --mutate=shift > /dev/null 2>&1; r1=$?
"$PY" -I $IN/read_lower.py selftest --mutate=round2 > /dev/null 2>&1; r2=$?
"$PY" -I $IN/repeat_check.py selftest > selftest_repeat_check.txt 2>&1; r3=$?
"$PY" -I $IN/pair2025.py --selftest > selftest_pair.txt 2>&1; p0=$?
"$PY" -I $IN/pair2025.py --selftest --break > /dev/null 2>&1; p1=$?
echo "$r0 $r1 $r2 $r3 $p0 $p1" > selftest_wide_exits.txt
[ "$r0 $r1 $r2 $r3 $p0 $p1" = "0 1 1 0 0 1" ] || refuse "the selftests did not behave (read_lower $r0 $r1 $r2, repeat_check $r3, pair $p0 $p1; wanted 0 1 1 0 0 1)"
LISTS=("0.14,-0.10,0.18,0.34,0.50" "0.14,-0.06,0.22,0.38" "-0.02,0.10,0.26,0.42" "0.02,0.06,0.30,0.46")
echo "lists: ${LISTS[*]}" > $OUT/scan_wide_plan.txt
log "kc95 wide D $D pins and selftests ok (read_lower + shift + round2, repeat_check, pair gate; each mutation exit 1); lists ${LISTS[*]}"
[ "$DRY" = 1 ] && { echo "DRY: lists ${LISTS[*]}"; exit 0; }
log "kc95 wide D $D waits for regrid_accepted.txt, then for the D 22.28125 low scan, then for my other d18_hybsign scans and memory"
until [ -s $OUT/regrid_accepted.txt ]; do [ -e $OUT/regrid_refused.txt ] && { log "kc95 wide D $D: the regrid was refused: no scan"; exit 3; }; sleep 30; done
REC=$WOUT/rec_k95_D${F4}.jsonl; ST=$WOUT/sol_${NEWTAG}_D${F4}.npy
[ -s $OUT/rec_k95_D${F4}.jsonl ] && [ -s $OUT/sol_${NEWTAG}_D${F4}.npy ] || refuse "record or state missing"
log "kc95 wide D $D: the regrid is accepted (state blob $(git hash-object --no-filters $OUT/sol_${NEWTAG}_D${F4}.npy | cut -c1-8), record blob $(git hash-object --no-filters $OUT/rec_k95_D${F4}.jsonl | cut -c1-8))"
# START_NOW=1 (the coordinator's hc of 25 Nov ~07:45 UTC: "start the D 22.5 wide scan now, beside the low scan (8 threads)"): no wait for the D 22.28125 low scan and no wait for other d18_hybsign scans; the free-memory wait stays
if [ "$START_NOW" = 1 ]; then log "kc95 wide D $D: START_NOW=1: no wait for the D 22.28125 low scan; waits for memory only"
else
until [ -e $LOWDONE ] || [ -e $LOWREF ]; do sleep 60; done
log "kc95 wide D $D: the D 22.28125 low scan is over ($([ -e $LOWDONE ] && echo done || echo refused)); waits for threads and memory"
fi
tw=$(date +%s)
while :; do
  n=$(powershell -NoProfile -Command "@(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -match 'I1025-win2.*d18_hybsign.py' -and \$_.Name -match 'python' }).Count" | tr -d '\r')
  fm=$(powershell -NoProfile -Command "[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)" | tr -d '\r')
  { [ "$n" = 0 ] || [ "$START_NOW" = 1 ]; } && [ "$fm" -ge 18400 ] && break
  [ $(( $(date +%s) - tw )) -lt 21600 ] || refuse "the wait for threads and memory ended after 6 h ($n scans, $fm MB free)"
  sleep 60
done
cd $WT/solver/matter || exit 1
scan() {  # N LAMS
  local N=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $WIN/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D${D}_p$N.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 1 thread)"; } > $OUT/scan_D${D}_p$N.log
  crun widescan95_p$N 0 $CAP d18_hybsign.py "$PY" -u $WIN/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D${D}_p$N.jsonl >> $OUT/scan_D${D}_p$N.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/scan_D${D}_p$N.log
  local n; n=$(grep -c '^{' $OUT/scan_D${D}_p$N.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_D${D}_p$N: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n points" >> $SUM
  log "widescan95_p$N exit $rc wall $w s capped $CAPPED"
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
{ echo "=== read_lower.py $WOUT -0.10 0.50"; "$PY" -W ignore $IN/read_lower.py $WOUT -0.10 0.50; echo "read_lower exit $?"; echo "=== repeat_check.py (merged scan file)"; "$PY" -I $IN/repeat_check.py $OUT/scan_D${D}_all.jsonl; echo "repeat_check exit $?"; echo "=== pair2025.py (P1 and P2 first records)"; "$PY" -I $IN/pair2025.py scan_D${D}_p1.jsonl scan_D${D}_p2.jsonl; echo "pair exit $?"; } > read_lower.txt 2>&1
echo "kc95 wide D $D reading: $(grep -E '^hybrid signs|^float64 sign differs|^robust changes|robust change \(' read_lower.txt | tr '\n' ' ' | cut -c1-900)" >> $SUM
log "kc95 wide D $D scan done: $(tail -n 1 $SUM | cut -c1-300)"
touch $OUT/scan.done
exit 0
