#!/bin/bash
# #1025 kc71_leap on win2: an EXTENSION of the window of one D (the coordinator's rule of 2026-11-22: "if the root read sits within 0.03 of a window edge, extend that side by 0.10 before reading it"). usage: kcl_ext.sh D SIDE K PATH
# (SIDE low or high; K the extension number, 1, 2, ...). The edge point e of the window so far (the lowest or highest lambda of the scan files of D) is evaluated again as a repeat (first, in both processes) and 10 new points follow
# (e -/+ 0.01 i, i = 1 to 10): X<K>1 = i 0 to 5, X<K>2 = i 0 and 6 to 10 (6 evaluations each), 4 threads each, caps 28800 s by the exact root pids, the same scanner, state and record as the D's scan (rec_D<D>.jsonl, states/).
# The pair gate (kcl_ext.py gate) compares the two edge points (same sign, ln|det| within 1e-6) and kills both by exact pid on a disagreement; the reader's repeat rule compares them with the original scan's edge point.
# Then kc71_leap_read.py reads again (read_D<D>_ext<K>.txt).
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
D=$1; SIDE=$2; K=$3; PTH=$4
OUT=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $OUT/lib_kcl.sh
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/kc71_leap
Q=D:/choptuik-large-d-raw-push/I1025-mac/d18
WT=/d/choptuik-i1025k71
WTM=D:/choptuik-i1025k71/solver/matter
TAGL=l1kc71Lw1025
CAP=28800
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1
DS=$("$PY" -c "print('%g' % float('$D'))")
DF=$("$PY" -c "print('%.6f' % float('$D'))")
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "D $DS ext$K refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2 "d18_hybsign.py"
for pr in "d18d_read.py 6b608903" "d185_scan_read.py 7c9d400f" "d18c_read.py 1383470f"; do set -- $pr; chk /d/choptuik-i935-raw/I1025-win2/d18mid/pinned/$1 $2 "pinned/$1"; done
[ -e $OUT/rec_D${DS}.jsonl ] && [ -e $OUT/states/sol_${TAGL}_D${DF}.npy ] || { log "D $DS ext$K refuse: no record snapshot or state (the D's scan has not started)"; bad=1; }
for i in 1 2; do [ -e $OUT/scan_D${DS}_X$K$i.jsonl ] && { log "D $DS ext$K refuse: scan_D${DS}_X$K$i.jsonl exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
cd $OUT
"$PY" kcl_ext.py selftest > selftest_ext.txt 2>&1; e1=$?
"$PY" kcl_ext.py selftest --break > selftest_ext_break.txt 2>&1; e2=$?
[ $e1 = 0 ] && [ $e2 = 1 ] || { log "D $DS ext$K: a control is wrong ($e1/$e2): stop"; exit 1; }
EDGE=$("$PY" kcl_ext.py edge $WOUT $DS $SIDE)
mapfile -t XL < <("$PY" kcl_ext.py lists $EDGE $SIDE)
LX1=${XL[0]}
LX2=${XL[1]}
log "D $DS ext$K ($SIDE, edge $EDGE): X${K}1 $LX1 | X${K}2 $LX2"
echo "D $DS extension $K ($SIDE side of the window, edge $EDGE): X${K}1 $LX1; X${K}2 $LX2" >> $SUM
ST=$WOUT/states/sol_${TAGL}_D${DF}.npy
REC=$WOUT/rec_D${DS}.jsonl
cd $WT/solver/matter || exit 1
scan() {  # P LAMS
  local P=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $Q/d18_hybsign.py $REC $ST $DS $L $WOUT/scan_D${DS}_$P.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 4 threads)"; } > $OUT/scan_D${DS}_$P.log
  crun scanD${DS}_$P 0 $CAP d18_hybsign.py "$PY" -u $Q/d18_hybsign.py $REC $ST $DS $L $WOUT/scan_D${DS}_$P.jsonl >> $OUT/scan_D${DS}_$P.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/scan_D${DS}_$P.log
  local n; n=$(grep -c '^{' $OUT/scan_D${DS}_$P.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_D${DS}_$P: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n points" >> $SUM
  log "scanD${DS}_$P exit $rc wall $w s capped $CAPPED"
}
killroot() {
  local pid; pid=$(grep " $1 root pid " $EX | tail -1 | sed -E 's/.* root pid ([0-9]+),.*/\1/')
  [ -n "$pid" ] || return
  local cl; cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$pid\").CommandLine" | tr -d '\r')
  case "$cl" in *d18_hybsign.py*) log "gate: killing the tree of $1 pid $pid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $pid > /dev/null 2>&1;; *) log "gate: $1 pid $pid does not match d18_hybsign.py (${cl:0:60}), nothing killed";; esac
}
scan X${K}1 $LX1 &
q1=$!
scan X${K}2 $LX2 &
q2=$!
t0=$(date +%s); gate=none
while kill -0 $q1 2> /dev/null || kill -0 $q2 2> /dev/null; do
  "$PY" $OUT/kcl_ext.py gate $WOUT $DS $K $EDGE > $OUT/pair_check_D${DS}_X$K.txt 2>&1; g=$?
  if [ $g = 0 ]; then gate=pass; log "D $DS ext$K pair gate passed"; echo "D $DS ext$K pair gate: passed after $(( $(date +%s) - t0 )) s: $(head -n 1 $OUT/pair_check_D${DS}_X$K.txt | cut -c1-200)" >> $SUM; break; fi
  if [ $g = 1 ]; then gate=fail; log "D $DS ext$K pair gate FAILED: killing both scans"; echo "D $DS ext$K pair gate: FAILED: $(head -n 1 $OUT/pair_check_D${DS}_X$K.txt)" >> $SUM; killroot scanD${DS}_X${K}1; killroot scanD${DS}_X${K}2; break; fi
  if [ $(( $(date +%s) - t0 )) -gt 7200 ]; then gate=fail; log "D $DS ext$K pair gate: no first points after 7200 s; killing both scans"; echo "D $DS ext$K pair gate: no first points after 7200 s" >> $SUM; killroot scanD${DS}_X${K}1; killroot scanD${DS}_X${K}2; break; fi
  sleep 30
done
[ $gate = none ] && { gate=fail; echo "D $DS ext$K pair gate: the scans ended before the first points were compared" >> $SUM; }
wait $q1; wait $q2
cd $OUT
if [ $gate = pass ]; then
  "$PY" kc71_leap_read.py $WOUT $DS $PTH > read_D${DS}_ext${K}.txt 2>&1
  echo "D $DS ext$K kc71_leap_read: exit $?: $(grep -E '^(LAMBDA_1|NOT READ|STOP-level|EDGE)' read_D${DS}_ext${K}.txt | cut -c1-260 | tr '\n' ' ')" >> $SUM
fi
"$PY" points_table_leap.py $WOUT $DS > points_D${DS}.md 2>&1
log "D $DS ext$K done (gate $gate)"; echo "D $DS ext$K done (pair gate $gate)" >> $SUM
touch $OUT/scan_D${DS}_ext$K.done
exit 0
