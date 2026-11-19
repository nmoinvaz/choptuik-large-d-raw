#!/bin/bash
# #949 (2026-11-19, for dh370's bar test on #966): sync949.sh and queue_new949.py every 5 minutes, so a new ks_chain3b state is read within minutes of its push instead of up to 30 minutes
# after it (the 30-minute chore does the same by hand). Only the raw copies in ~/scratch949 and queue949.txt change. Deadline: the 48 h stop, 2026-11-19 22:42 UTC. usage: bash autoqueue949.sh
HERE=/home/nathan/Source/choptuik-large-d-raw/I949-dh170
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
END=$(date -u -d '2026-11-19 22:42:00' +%s)
cd $HERE || exit 9
echo "autoqueue started $(date -u '+%F %T') UTC, deadline $(date -u -d @$END '+%F %T') UTC"
while [ "$(date +%s)" -lt "$END" ]; do
  out=$(./sync949.sh 2>&1 | grep -E "^new I966|^new I903-win2/ks_chain2|^new I903-win2/ks_chain/leg0[89]" ; $PY queue_new949.py 2>&1)
  [ -n "$out" ] && echo "$(date -u '+%T') $out"
  sleep 300
done
echo "deadline reached $(date -u '+%F %T')"
