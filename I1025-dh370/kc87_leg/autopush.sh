#!/bin/bash
# #1025 kc87_leg: pushes each newly accepted point (state and record, in the live folder after the leg's copy loop) to raw by push_point.sh, as t5 asked, and logs the commit and blobs to push_log.txt.
# Polls every 60 s; ends when LEG_DONE.txt exists and everything is pushed. Unit i1025push. No hc from here.
{
LIVE=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc87_leg
last=21.03125
while true; do
  new=$(python3 - <<PY
import json, os
live = "$LIVE"; last = $last
rs = [json.loads(l) for l in open(live + "/l1kc87Ldh370.jsonl") if l.strip()] if os.path.exists(live + "/l1kc87Ldh370.jsonl") else []
for r in rs:
    D = r["D"]
    if D > last + 1e-9 and os.path.exists(live + "/sol_l1kc87Ldh370_D%.6f.npy" % D):
        print(repr(D)); break
PY
)
  if [ -n "$new" ]; then
    sleep 20      # the copy loop copies state and record in one pass; settle
    out=$(bash $LIVE/push_point.sh $new "k_c 87 leg: the accepted state and record of D $new (for dh170's scan)" 2>&1 | tail -1)
    echo "$(date -u '+%F %T') UTC D $new: $out" >> $LIVE/push_log.txt
    case "$out" in raw\ commit*) last=$new;; *) sleep 60;; esac
  else
    [ -f $LIVE/LEG_DONE.txt ] && break
    sleep 60
  fi
done
echo "$(date -u '+%F %T') UTC autopush ends (LEG_DONE)" >> $LIVE/push_log.txt
exit 0
}
