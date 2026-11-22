#!/bin/bash
# (leg1_guard2.sh = leg1_guard.sh plus the GDRY dry run, written for restart 1 of the leap while leg1_guard.sh was running; set GROOT to the new root pid)
# #1025 kc71_leap, first leg, on win2: replaces the parts of run_leap.sh that died at 07:17 UTC 22 Nov when the old runner's terminal was ended (its bash tree, the copier loop, the 12 h cap,
# the leap_report step and the end markers; the leap's python, root pid 35992 and child 23496, survived). Does what run_leap.sh's leap section did: every 120 s copies new saved states and the record into
# states/ (a file at least 30 s old), kills the exact root pid's tree (taskkill /T /F /PID) once 43200 s have passed since the leap's start 03:50:08 UTC AND the pid's command line contains ell_leap.py,
# and when the pid is gone copies once more, logs how it ended (the exit code is not available: its parent is dead; the log's last line says reached / stop), touches leap.finished, runs leap_report.py and
# touches all.done. Lines go to exits_kcl.txt and summary_kcl.txt as before. env overrides for the planted test only: GOUT GDATA GROOT GCAP_EPOCH GRX GTAG.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=${GOUT:-/d/choptuik-i935-raw/I1025-win2/kc71_leap}
. /d/choptuik-i935-raw/I1025-win2/kc71_leap/lib_kcl.sh
OUT=${GOUT:-$OUT}; EX=$OUT/exits_kcl.txt; SUM=$OUT/summary_kcl.txt
DATA=${GDATA:-/d/choptuik-i1025k71/solver/matter/data}
TAGL=${GTAG:-l1kc71Lw1025}
ROOT=${GROOT:-35992}
RX=${GRX:-ell_leap.py}
START=$(date -u -d '2026-11-22 03:50:08' +%s)
CAPE=${GCAP_EPOCH:-$(( START + 43200 ))}
log "leg1 guard started: root pid $ROOT, cap at $(date -u -d @$CAPE '+%F %T') UTC (43200 s after the leap's start 03:50:08), copier every 120 s, the driver tree of run_leap.sh is dead since 07:17 UTC"
copy_all() {
  for f in $DATA/sol_${TAGL}_D*.npy $DATA/sol_${TAGL}_last.npy $DATA/sol_${TAGL}_prev.npy $DATA/${TAGL}.jsonl; do
    [ -e "$f" ] || continue
    b=$(basename $f)
    if [ $(( $(date +%s) - $(date -r "$f" +%s) )) -ge ${1:-30} ] && ! cmp -s "$f" "$OUT/states/$b"; then cp "$f" "$OUT/states/$b"; fi
  done
}
alive() { tasklist //FI "PID eq $ROOT" 2>/dev/null | grep -q " $ROOT "; }
if [ "$GDRY" = 1 ]; then  # dry run: says whether the cap would kill the root pid (alive and its command line holds $RX); kills nothing, writes no markers
  if alive; then cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$ROOT\").CommandLine" | tr -d '\r'); case "$cl" in *$RX*) echo "DRY: pid $ROOT is alive and its command line holds $RX: the cap at $(date -u -d @$CAPE '+%F %T') UTC would kill its tree";; *) echo "DRY: pid $ROOT is alive but its command line does NOT hold $RX: the cap would kill nothing";; esac; else echo "DRY: pid $ROOT is not running"; fi
  exit 0
fi
CAPPED=0
mkdir -p $OUT/states
while alive; do
  copy_all 30
  if [ $(date +%s) -ge $CAPE ] && [ $CAPPED = 0 ]; then
    cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$ROOT\").CommandLine" | tr -d '\r')
    case "$cl" in
      *$RX*) log "leap cap $(( $(date +%s) - START )) s since the start reached, killing the tree of pid $ROOT"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $ROOT > /dev/null 2>&1; CAPPED=1;;
      *) log "leap pid $ROOT does not match '$RX' (command line: ${cl:0:80}), nothing killed"; CAPPED=2;;
    esac
  fi
  for i in 1 2 3 4 5 6 7 8; do alive || break; sleep 15; done
done
copy_all 0
w=$(( $(date +%s) - START ))
echo "leap: root pid $ROOT ended after $w s since the start$([ $CAPPED = 1 ] && echo ", capped at 43200 s"), exit code not available (its parent died at 07:17 UTC): $(grep -E '^(reached|stop at)' $OUT/leap.log | tail -n 1)" >> $SUM
log "leg1 leap ended wall $w s capped $CAPPED"
touch $OUT/leap.finished
if [ -z "$GOUT" ]; then
  C:/Users/nathan/Source/venv-md510/Scripts/python.exe -I $OUT/leap_report.py D:/choptuik-i935-raw/I1025-win2/kc71_leap > $OUT/leap_report.md 2>&1
  echo "leap_report: exit $?" >> $SUM
fi
log "leg1 guard done"; echo "kcl leap done" >> $SUM
touch $OUT/all.done
exit 0
