#!/bin/bash
# #1025 lower_root: after both lanes end, the reading (the coordinator rules on the tracks): read_lower.py on each lane (every robust change with its det-linear estimate and range, the
# repeat, the minima without a change), repeat_check.py on each scan, lane A's cross-machine overlap and seam against the Mac's D 18.5 data, and the unmodified read_d19.py on lane A (a 0.02 grid
# it can read) as a second reader.
F=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/lower_root; PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
for X in A B; do
  until grep -qE "lane $X done|STOP|refuse" $F/lane$X/exits.txt 2>/dev/null; do sleep 20; done
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC both lanes ended; reading" >> $F/exits_read.txt
cd $F; export D18_DIR=$F
{
  for XL in "A 1.20 1.54" "B 1.47 1.55"; do
    set -- $XL; echo "=== lane $1: read_lower.py $1 $2 $3"
    $PY -W ignore read_lower.py lane$1 $2 $3; echo "read_lower exit $?"
    $PY -W ignore repeat_check.py lane$1/scan_D*_p0.jsonl; echo "repeat_check exit $?"
  done
  echo "=== lane A against the Mac's D 18.5 data"
  $PY -W ignore cross_check_mac.py laneA/scan_D18.5_p0.jsonl in/d18_refsign_1025_mac.jsonl 18.5 overlap; echo "overlap exit $?"
  $PY -W ignore cross_check_mac.py laneA/scan_D18.5_p0.jsonl in/d185_scan_1025_mac.jsonl 18.5 seam; echo "seam exit $?"
  echo "=== lane A with the unmodified read_d19.py (blob 13bd4997), second reader"
  $PY -W ignore read_d19.py laneA 1.20 1.54; echo "read_d19 exit $?"
} > read_lower.txt 2>&1
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC read done" >> $F/exits_read.txt
rm -rf $F/__pycache__
