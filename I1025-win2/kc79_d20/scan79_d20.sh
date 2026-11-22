#!/bin/bash
# #1025 kc79_d20 on win2 (t5's hc, ~22:55 UTC 22 Nov): the hybrid scan of the accepted k_c 79 D 20 state at lambda 1.20 to 1.32 at 0.01 (13 values) plus a repeat of 1.26, SIX processes of ONE thread, xfkappa's d18_hybsign.py
# (blob e089207a, unchanged; its first line is the record-system check, exit 3 if not), the 1e-15 noise test and the float64 sign; read with read_lower.py (blob 89309d3c). Lists: P1 1.26 1.20 1.21 | P2 1.26 1.22 1.23 |
# P3 1.24 1.25 | P4 1.27 1.28 | P5 1.29 1.30 | P6 1.31 1.32 (14 evaluations); the repeat of 1.26 (P1, P2) is gated by pair79.py (a disagreement kills the six scans by exact pid). Caps 28800 s by the exact root pids.
# usage: scan79_d20.sh   (env DRY=1: pins, controls and the plan only)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc79_d20   # lib_kcl.sh sets OUT to the leap folder
EX=$OUT/exits_kc79.txt; SUM=$OUT/summary_kc79.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter; WOUT=D:/choptuik-i935-raw/I1025-win2/kc79_d20
TAG=l1kc79W20m1025; STD=20; CAP=28800
REC=$WOUT/rec_k79_D20.0000.jsonl; ST=$WOUT/sol_${TAG}_D20.0000.npy
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc79 scan refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $OUT/inputs/d18_hybsign.py e089207a "d18_hybsign.py"
chk $OUT/inputs/read_lower.py 89309d3c "read_lower.py"
chk $OUT/inputs/d185_scan_read.py 7c9d400f "d185_scan_read.py"
for i in 1 2 3 4 5 6; do [ -e $OUT/scan_k79d20_p$i.jsonl ] && { log "kc79 scan refuse: scan_k79d20_p$i.jsonl exists"; bad=1; }; done
[ "$DRY" = 1 ] || true
[ $bad = 0 ] || exit 2
cd $OUT
"$PY" -I inputs/read_lower.py selftest > selftest_read_lower.txt 2>&1; r1=$?
"$PY" -I inputs/read_lower.py selftest --mutate=shift > /dev/null 2>&1; r2=$?
"$PY" -I inputs/read_lower.py selftest --mutate=round2 > /dev/null 2>&1; r3=$?
"$PY" -I pair79.py --selftest > selftest_pair79.txt 2>&1; p1=$?
"$PY" -I pair79.py --selftest --break > /dev/null 2>&1; p2=$?
[ $r1 = 0 ] && [ $r2 = 1 ] && [ $r3 = 1 ] && [ $p1 = 0 ] && [ $p2 = 1 ] || { log "kc79 scan STOP: a control is wrong (read_lower $r1/$r2/$r3, pair79 $p1/$p2)"; exit 1; }
LISTS=("1.26,1.20,1.21" "1.26,1.22,1.23" "1.24,1.25" "1.27,1.28" "1.29,1.30" "1.31,1.32")
log "kc79 scan pins and controls ok (read_lower selftest + 2 mutations, pair79 selftest + break); lists: ${LISTS[*]}"
[ "$DRY" = 1 ] && { echo "DRY: lists ${LISTS[*]}; waits for $OUT/regrid_accepted.txt"; [ -e $OUT/regrid_accepted.txt ] || exit 0; }
log "kc79 scan waits for regrid_accepted.txt"
until [ -e $OUT/regrid_accepted.txt ]; do [ -e $OUT/regrid_refused.txt ] && { log "kc79 scan: the regrid was refused: no scan"; exit 3; }; sleep 30; done
chk $OUT/rec_k79_D20.0000.jsonl "" "the k_c 79 record line" ; [ -s $OUT/rec_k79_D20.0000.jsonl ] && [ -s $OUT/sol_${TAG}_D20.0000.npy ] || { log "kc79 scan STOP: record or state missing"; exit 1; }
cd $WT/solver/matter || exit 1
scan() {  # N LAMS
  local N=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $WOUT/inputs/d18_hybsign.py $REC $ST $STD $L $WOUT/scan_k79d20_p$N.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 1 thread)"; } > $OUT/scan_k79d20_p$N.log
  crun scan79_p$N 0 $CAP d18_hybsign.py "$PY" -u $WOUT/inputs/d18_hybsign.py $REC $ST $STD $L $WOUT/scan_k79d20_p$N.jsonl >> $OUT/scan_k79d20_p$N.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/scan_k79d20_p$N.log
  local n; n=$(grep -c '^{' $OUT/scan_k79d20_p$N.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_k79d20_p$N: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n points" >> $SUM
  log "scan79_p$N exit $rc wall $w s capped $CAPPED"
}
killroot() {
  local pid; pid=$(grep " $1 root pid " $EX | tail -1 | sed -E 's/.* root pid ([0-9]+),.*/\1/')
  [ -n "$pid" ] || return
  local cl; cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$pid\").CommandLine" | tr -d '\r')
  case "$cl" in *d18_hybsign.py*) log "gate: killing the tree of $1 pid $pid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $pid > /dev/null 2>&1;; *) log "gate: $1 pid $pid does not match d18_hybsign.py, nothing killed";; esac
}
for i in 1 2 3 4 5 6; do scan $i ${LISTS[$((i-1))]} & eval "q$i=\$!"; done
t0=$(date +%s); gate=none
while kill -0 $q1 2>/dev/null || kill -0 $q2 2>/dev/null || kill -0 $q3 2>/dev/null || kill -0 $q4 2>/dev/null || kill -0 $q5 2>/dev/null || kill -0 $q6 2>/dev/null; do
  "$PY" -I $OUT/pair79.py $WOUT/scan_k79d20_p1.jsonl $WOUT/scan_k79d20_p2.jsonl > $OUT/pair_check.txt 2>&1; g=$?
  if [ $g = 0 ]; then gate=pass; log "kc79 scan pair gate passed after $(( $(date +%s) - t0 )) s: $(cat $OUT/pair_check.txt | cut -c1-150)"; echo "kc79 scan pair gate: passed: $(cat $OUT/pair_check.txt)" >> $SUM; break; fi
  if [ $g = 1 ]; then gate=fail; log "kc79 scan pair gate FAILED: killing all six scans"; echo "kc79 scan pair gate: FAILED: $(cat $OUT/pair_check.txt)" >> $SUM; for n in 1 2 3 4 5 6; do killroot scan79_p$n; done; break; fi
  [ $(( $(date +%s) - t0 )) -gt 10800 ] && { gate=fail; log "kc79 scan pair gate: no first points after 10800 s; killing all six"; for n in 1 2 3 4 5 6; do killroot scan79_p$n; done; break; }
  sleep 30
done
[ $gate = none ] && { gate=fail; echo "kc79 scan: the scans ended before the repeat was compared" >> $SUM; }
for i in 1 2 3 4 5 6; do eval "wait \$q$i"; done
cd $OUT
if [ $gate = pass ]; then
  "$PY" -I inputs/read_lower.py $WOUT 1.20 1.32 > read_lower_k79_D20.txt 2>&1; echo "kc79 scan read_lower: exit $?" >> $SUM
fi
log "kc79 scan done (gate $gate)"; echo "kc79 scan done (pair gate $gate)" >> $SUM
touch $OUT/scan.done
exit 0
