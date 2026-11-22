#!/bin/bash
# #1025 kc79_d19125low: after both scan processes end, the reading (the coordinator rules): read_lower.py (dh170's, blob 89309d3c) on the scan folder: every robust change with bracket, orientation as printed, det-linear estimate
# and range, the edge signs, changes touching a non-robust point, ln|det| minima without a sign change, the repeat of 1.30 (across the two processes); repeat_check.py on the merged file; and my 1.44 against dh370's 1.44 row (the seam).
F=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc79_d19125low; PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
for P in 0 1; do
  until grep -qE "process $P done|STOP|refuse" $F/scan/exits_p$P.txt 2>/dev/null; do sleep 20; done
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC both processes ended; reading" >> $F/exits_read.txt
cd $F; export D18_DIR=$F/in
cat scan/scan_D19.125_p0.jsonl scan/scan_D19.125_p1.jsonl > merged_D19.125.jsonl
{
  echo "=== read_lower.py scan 1.10 1.44"
  $PY -W ignore in/read_lower.py scan 1.10 1.44; echo "read_lower exit $?"
  $PY -W ignore in/repeat_check.py merged_D19.125.jsonl; echo "repeat_check exit $?"
  echo "=== the seam: my lambda 1.44 against dh370's 1.44 row (same state, a Linux build on 1 thread)"
  $PY -W ignore in/cross_check.py merged_D19.125.jsonl in/ref_dh370_scan_rows.jsonl 19.125 overlap; echo "overlap exit $?"
} > read_k79.txt 2>&1
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC read done" >> $F/exits_read.txt
rm -rf $F/__pycache__ $F/in/__pycache__
