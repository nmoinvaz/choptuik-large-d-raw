#!/bin/bash
# waits for unit i1064m (the projection-switch run) to end (cap 12000 s), runs the dry tests of run1064f.sh, and starts unit i1064n only if both dry checks pass
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
t0=$(date +%s)
while [ "$(systemctl --user is-active i1064m)" = active ]; do
  [ $(( $(date +%s) - t0 )) -ge 12000 ] && { date -u '+%F %T wait cap reached: nothing started'; exit 1; }
  sleep 30
done
date -u '+%F %T i1064m ended; dry runs of run1064f.sh'
bash dry_1064f.sh > dry_1064f.out 2>&1
tail -3 dry_1064f.out
if grep -q 'DRY OK' dry_1064f.out; then bash start_1064_ho.sh; else date -u '+%F %T dry failed: unit i1064n not started'; fi
