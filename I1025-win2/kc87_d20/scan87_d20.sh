#!/bin/bash
# #1025 kc87_d20 on win2 (the coordinator's task, comment 7090320838): step 2, after the k_c 87 regrid of D 20 is ACCEPTED: xfkappa's d18_hybsign.py (blob e089207a, unchanged; its first line is the record-system check, exit 3 if not)
# at lambda 1.20 to 1.28 by 0.01 (9 values), 1.290 to 1.330 by 0.005 (9 values) and a repeat of 1.25: 19 evaluations on SEVEN processes of ONE thread, beside leg 3 of the leap, with the 1e-15 noise test and the float64 sign.
# Lists: P1 1.25 1.20 1.21 | P2 1.25 1.22 1.23 | P3 1.24 1.26 1.27 | P4 1.28 1.290 1.295 | P5 1.300 1.305 1.310 | P6 1.315 1.320 | P7 1.325 1.330. The repeat of 1.25 (P1, P2) is gated by pair87.py (1e-6; a disagreement kills
# the seven scans by exact pid). Caps 28800 s by the exact root pids. Then read_lower.py (89309d3c) after its selftest and --mutate=shift and --mutate=round2 (exit 1 each). usage: scan87_d20.sh   (env DRY=1: pins, controls and the plan only)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc87_d20   # lib_kcl.sh sets OUT to the leap folder
EX=$OUT/exits_kc87.txt; SUM=$OUT/summary_kc87.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter; WOUT=D:/choptuik-i935-raw/I1025-win2/kc87_d20
TAG=l1kc87win2d20; STD=20; CAP=28800
REC=$WOUT/rec_k87_D20.0000.jsonl; ST=$WOUT/sol_${TAG}_D20.0000.npy
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc87 scan refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $OUT/inputs/d18_hybsign.py e089207a "d18_hybsign.py"
chk $OUT/inputs/read_lower.py 89309d3c "read_lower.py"
chk $OUT/inputs/d185_scan_read.py 7c9d400f "d185_scan_read.py"
for i in 1 2 3 4 5 6 7; do [ -e $OUT/scan_k87d20_p$i.jsonl ] && { log "kc87 scan refuse: scan_k87d20_p$i.jsonl exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
cd $OUT
"$PY" -I inputs/read_lower.py selftest > selftest_read_lower.txt 2>&1; r1=$?
"$PY" -I inputs/read_lower.py selftest --mutate=shift > /dev/null 2>&1; r2=$?
"$PY" -I inputs/read_lower.py selftest --mutate=round2 > /dev/null 2>&1; r3=$?
"$PY" -I pair87.py --selftest > selftest_pair87.txt 2>&1; p1=$?
"$PY" -I pair87.py --selftest --break > /dev/null 2>&1; p2=$?
[ $r1 = 0 ] && [ $r2 = 1 ] && [ $r3 = 1 ] && [ $p1 = 0 ] && [ $p2 = 1 ] || { log "kc87 scan STOP: a control is wrong (read_lower $r1/$r2/$r3, pair87 $p1/$p2)"; exit 1; }
LISTS=("1.25,1.20,1.21" "1.25,1.22,1.23" "1.24,1.26,1.27" "1.28,1.290,1.295" "1.300,1.305,1.310" "1.315,1.320" "1.325,1.330")
log "kc87 scan pins and controls ok (read_lower selftest + shift + round2 exit 1, pair87 selftest + break); lists: ${LISTS[*]}"
[ "$DRY" = 1 ] && { echo "DRY: lists ${LISTS[*]}; waits for $OUT/regrid_accepted.txt"; [ -e $OUT/regrid_accepted.txt ] || exit 0; }
log "kc87 scan waits for regrid_accepted.txt"
until [ -e $OUT/regrid_accepted.txt ]; do [ -e $OUT/regrid_refused.txt ] && { log "kc87 scan: the regrid was refused: no scan"; exit 3; }; sleep 30; done
[ -s $OUT/rec_k87_D20.0000.jsonl ] && [ -s $OUT/sol_${TAG}_D20.0000.npy ] || { log "kc87 scan STOP: record or state missing"; exit 1; }
cd $WT/solver/matter || exit 1
scan() {  # N LAMS
  local N=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $WOUT/inputs/d18_hybsign.py $REC $ST $STD $L $WOUT/scan_k87d20_p$N.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 1 thread)"; } > $OUT/scan_k87d20_p$N.log
  crun scan87_p$N 0 $CAP d18_hybsign.py "$PY" -u $WOUT/inputs/d18_hybsign.py $REC $ST $STD $L $WOUT/scan_k87d20_p$N.jsonl >> $OUT/scan_k87d20_p$N.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/scan_k87d20_p$N.log
  local n; n=$(grep -c '^{' $OUT/scan_k87d20_p$N.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_k87d20_p$N: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n points" >> $SUM
  log "scan87_p$N exit $rc wall $w s capped $CAPPED"
}
killroot() {
  local pid; pid=$(grep " $1 root pid " $EX | tail -1 | sed -E 's/.* root pid ([0-9]+),.*/\1/')
  [ -n "$pid" ] || return
  local cl; cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$pid\").CommandLine" | tr -d '\r')
  case "$cl" in *d18_hybsign.py*) log "gate: killing the tree of $1 pid $pid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $pid > /dev/null 2>&1;; *) log "gate: $1 pid $pid does not match d18_hybsign.py, nothing killed";; esac
}
for i in 1 2 3 4 5 6 7; do scan $i ${LISTS[$((i-1))]} & eval "q$i=\$!"; done
t0=$(date +%s); gate=none
alive() { kill -0 $q1 2>/dev/null || kill -0 $q2 2>/dev/null || kill -0 $q3 2>/dev/null || kill -0 $q4 2>/dev/null || kill -0 $q5 2>/dev/null || kill -0 $q6 2>/dev/null || kill -0 $q7 2>/dev/null; }
while alive; do
  "$PY" -I $OUT/pair87.py $WOUT/scan_k87d20_p1.jsonl $WOUT/scan_k87d20_p2.jsonl > $OUT/pair_check.txt 2>&1; g=$?
  if [ $g = 0 ]; then gate=pass; log "kc87 scan pair gate passed after $(( $(date +%s) - t0 )) s: $(cat $OUT/pair_check.txt | cut -c1-150)"; echo "kc87 scan pair gate: passed: $(cat $OUT/pair_check.txt)" >> $SUM; break; fi
  if [ $g = 1 ]; then gate=fail; log "kc87 scan pair gate FAILED: killing all seven scans"; echo "kc87 scan pair gate: FAILED: $(cat $OUT/pair_check.txt)" >> $SUM; for n in 1 2 3 4 5 6 7; do killroot scan87_p$n; done; break; fi
  [ $(( $(date +%s) - t0 )) -gt 10800 ] && { gate=fail; log "kc87 scan pair gate: no first points after 10800 s; killing all seven"; for n in 1 2 3 4 5 6 7; do killroot scan87_p$n; done; break; }
  sleep 30
done
[ $gate = none ] && { gate=fail; echo "kc87 scan: the scans ended before the repeat was compared" >> $SUM; }
for i in 1 2 3 4 5 6 7; do eval "wait \$q$i"; done
cd $OUT
if [ $gate = pass ]; then
  "$PY" -I inputs/read_lower.py $WOUT 1.20 1.33 > read_lower_k87_D20.txt 2>&1; echo "kc87 scan read_lower: exit $?" >> $SUM
fi
log "kc87 scan done (gate $gate)"; echo "kc87 scan done (pair gate $gate)" >> $SUM
touch $OUT/scan.done
exit 0
