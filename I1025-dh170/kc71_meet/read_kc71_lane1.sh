#!/bin/bash
# #1025 kc71_meet, after lane 2 (D 19.25) was stopped on t5's order: the reading of lane 1 only (D 19.1875): read_lower.py (dh170's, blob 89309d3c, unedited) with the repeat check; lane 2's four finished
# points (lane2_stopped/) are listed beside as the cross-machine data for dh610's rerun of D 19.25. The reader unit i1025-kc71read (read_kc71.sh, which waits for both lanes) was stopped.
F=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc71_meet; PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
until grep -qE "lane 1 done|STOP|refuse" $F/lane1/exits.txt 2>/dev/null; do sleep 20; done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC lane 1 ended; reading" >> $F/exits_read.txt
cd $F; export D18_DIR=$F/in
{
  echo "=== lane 1, D 19.1875: read_lower.py lane1 1.42 1.58"
  $PY -W ignore in/read_lower.py lane1 1.42 1.58; echo "read_lower exit $?"
  $PY -W ignore in/repeat_check.py lane1/scan_D19.1875_p0.jsonl; echo "repeat_check exit $?"
  echo "=== lane 2 (D 19.25), stopped after 4 points: hybrid sign and ln|det| per point (for the comparison with dh610's rerun)"
  $PY -c "
import json
for l in open('lane2_stopped/scan_D19.25_p0.jsonl'):
    r = json.loads(l); print('  lam %.2f: hybrid %+d ln|det| %.10f noise_robust %s float64 %+d (%d s)' % (r['lam'], r['sign'], r['ln'], r['noise_robust'], r['f64_sign'], r['sec']))"
} > read_kc71.txt 2>&1
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC read done" >> $F/exits_read.txt
rm -rf $F/__pycache__ $F/in/__pycache__
