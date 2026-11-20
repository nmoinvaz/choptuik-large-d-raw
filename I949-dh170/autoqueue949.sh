#!/bin/bash
# #949 (2026-11-19, for dh370's bar test on #966): sync949.sh and queue_new949.py every 5 minutes, so a new ks_chain3b state is read within minutes of its push instead of up to 30 minutes
# after it (the 30-minute chore does the same by hand). Only the raw copies in ~/scratch949 and queue949.txt change. Stops when STOP949 exists (reopened 2026-11-20; the 48 h deadline of 2026-11-19 22:42 UTC is gone). usage: bash autoqueue949.sh
HERE=/home/nathan/Source/choptuik-large-d-raw/I949-dh170
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
cd $HERE || exit 9
echo "autoqueue started $(date -u '+%F %T') UTC, until STOP949 exists (reopened 2026-11-20)"
while [ ! -f STOP949 ]; do
  out=$(./sync949.sh 2>&1 | grep -E "^new I966|^new I903-win2/ks_chain2|^new I903-win2/ks_chain/leg0[89]" ; $PY queue_new949.py 2>&1)
  [ -n "$out" ] && echo "$(date -u '+%T') $out"
  sleep 300
done
echo "STOP949 seen $(date -u '+%F %T')"
