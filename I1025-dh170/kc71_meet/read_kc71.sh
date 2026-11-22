#!/bin/bash
# #1025 kc71_meet: after both lanes end, the reading (the coordinator rules): read_lower.py (dh170's, blob 89309d3c, unedited) on each lane: every robust change with bracket, orientation as printed, det-linear estimate
# and range; changes touching a non-robust point; ln|det| minima without a sign change; the repeat of 1.50; then repeat_check.py on each scan.
F=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc71_meet; PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
for N in 1 2; do
  until grep -qE "lane $N done|STOP|refuse" $F/lane$N/exits.txt 2>/dev/null; do sleep 20; done
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC both lanes ended; reading" >> $F/exits_read.txt
cd $F; export D18_DIR=$F/in
{
  for XL in "1 19.1875" "2 19.25"; do
    set -- $XL; echo "=== lane $1, D $2: read_lower.py lane$1 1.42 1.58"
    $PY -W ignore in/read_lower.py lane$1 1.42 1.58; echo "read_lower exit $?"
    $PY -W ignore in/repeat_check.py lane$1/scan_D$2_p0.jsonl; echo "repeat_check exit $?"
  done
} > read_kc71.txt 2>&1
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC read done" >> $F/exits_read.txt
rm -rf $F/__pycache__ $F/in/__pycache__
