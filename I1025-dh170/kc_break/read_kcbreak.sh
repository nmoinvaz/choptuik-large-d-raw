#!/bin/bash
# #1025 k_c break at D 18.4375: after both lanes end, the reading: d18k2_read.py D LO HI KC55_SCAN KC63_SCAN (det-linear estimates of each robust change; a k_c 63 root with a k_c 55 root within 0.01 is
# k_c-stable, else k_c-dependent; every ln|det| minimum without a sign change gets a dip fit; the float64 sign summary for k_c 55).
D=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc_break; PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
for K in 63 55; do
  until grep -qE "lane kc$K done|STOP|refuse" $D/exits_kc$K.txt 2>/dev/null; do sleep 20; done
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC both lanes ended; reading" >> $D/exits_kcread.txt
cd $D
if [ -s kc55_D18.4375_scan_dh170.jsonl ] && [ -s kc63_D18.4375_scan_dh170.jsonl ]; then
  $PY -W ignore d18k2_read.py 18.4375 1.62 1.80 kc55_D18.4375_scan_dh170.jsonl kc63_D18.4375_scan_dh170.jsonl > kc_break_read.txt 2>&1
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC reader exit $?" >> $D/exits_kcread.txt
else
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC no reading: a scan file is missing or empty" >> $D/exits_kcread.txt
fi
rm -rf $D/__pycache__
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC read done" >> $D/exits_kcread.txt
