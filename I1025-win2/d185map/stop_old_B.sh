#!/bin/bash
# #1025 d185map: stops the first run's window B (root pid 26404, scan_B.jsonl) by its exact pid once the first run's repeat gate has passed (the coordinator's hc: split B, keep A running).
# The first driver's gate loop needs B's first point to pass; killing B before it would end in that gate killing A after 2700 s. A is not touched.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/d185map
PID=26404
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
until grep -qE "repeat gate: (passed|FAILED|no first)" $OUT/summary_d185map.txt; do sleep 5; done
if grep -q "repeat gate: passed" $OUT/summary_d185map.txt; then
  cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$PID\").CommandLine" | tr -d '\r')
  case "$cl" in
    *d18_hybsign.py*/d185map/scan_B.jsonl*) echo "d185map B stopped by hand for the split: killing the tree of pid $PID after the first gate passed, $(stamp)" >> $OUT/exits_d185map.txt
       MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $PID > /dev/null 2>&1; echo "stopped pid $PID at $(stamp)" > $OUT/stop_old_B.done;;
    *) echo "d185map stop_old_B: pid $PID does not match the old window B (${cl:0:100}), nothing killed, $(stamp)" >> $OUT/exits_d185map.txt; echo "nothing killed at $(stamp)" > $OUT/stop_old_B.done;;
  esac
else
  echo "the first gate did not pass (see summary_d185map.txt): nothing to stop by hand, $(stamp)" > $OUT/stop_old_B.done
fi
