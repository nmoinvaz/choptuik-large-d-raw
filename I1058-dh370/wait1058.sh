#!/usr/bin/env bash
# wakes when the #1058 build ends ('build exit N' in exits_1058.txt), on the first alert line (alerts1058.txt), on 'checks done' or when unit i1058b is inactive
cd /home/nathan/Source/choptuik-large-d-raw-wt613/I1058-dh370 || exit 9
a0=$(wc -l < alerts1058.txt 2>/dev/null || echo 0)
while sleep 15; do
  grep -q 'build exit' exits_1058.txt && { echo "BUILD ENDED"; grep '^1058' exits_1058.txt | tail -3; exit 0; }
  a=$(wc -l < alerts1058.txt 2>/dev/null || echo 0)
  [ "$a" -gt "$a0" ] && { echo ALERT; tail -n $((a-a0)) alerts1058.txt; exit 0; }
  [ "$(systemctl --user is-active i1058b)" = active ] || { echo "UNIT i1058b NOT ACTIVE"; tail -n 3 exits_1058.txt; exit 0; }
done
