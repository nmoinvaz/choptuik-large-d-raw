#!/bin/bash
# #1025 kc71_meet, t5's order (hc, 22 Nov): stop lane 2 (unit i1025-kc71b, D 19.25) after the point in flight lands, so dh610 can rerun the whole D 19.25 window. This waits for the next lam line of lane 2's scan.raw
# (and its jsonl row), then stops the unit. The finished points are kept by the caller (lane2 is renamed lane2_stopped, nothing deleted).
F=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc71_meet; LOG=$F/stop_lane2.log
N0=$(grep -c '^  lam ' $F/lane2/scan.raw)
echo "== $(date -u '+%F %T') UTC waiting for lane 2's next point ($N0 finished)" >> $LOG
until [ "$(grep -c '^  lam ' $F/lane2/scan.raw)" -gt "$N0" ] && [ "$(wc -l < $F/lane2/scan_D19.25_p0.jsonl)" -gt "$N0" ]; do sleep 2; done
echo "== $(date -u '+%F %T') UTC lane 2's point $((N0 + 1)) landed ($(grep '^  lam ' $F/lane2/scan.raw | tail -n 1 | cut -c1-60)); stopping unit i1025-kc71b" >> $LOG
systemctl --user stop i1025-kc71b.service; r=$?
echo "== $(date -u '+%F %T') UTC systemctl stop exit $r; unit state: $(systemctl --user is-active i1025-kc71b.service)" >> $LOG
