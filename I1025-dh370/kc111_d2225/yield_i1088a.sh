#!/bin/bash
# yield_i1088a.sh: t5's order (hc 25 Nov, dh610's rule): while a systemd user unit i1088a-* is active, raise the nice value of this lane's own compute processes to 19, by exact pid
# and every thread of it (renice_threads.sh: on Linux a nice value is per thread), once per thread. The compute processes are the regrid's python (ell_refine.py l1kc103dh370d2225) and the
# scan's pythons (d18_hybsign.py ... l1kc111dh370d2225). It only raises, stops and kills nothing, and ends when the lane's unit i1025k111 has ended. One line per change in i1088a_yield.txt.
# Env for the test only: YIELD_FAKE_ACTIVE=1 treats an i1088a unit as active, YIELD_PATTERN replaces the process pattern, YIELD_LOG the log, YIELD_UNIT the unit to follow.
F=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc111_d2225
PAT=${YIELD_PATTERN:-"ell_refine.py l1kc103dh370d2225|d18_hybsign.py .*l1kc111dh370d2225"}
LOG=${YIELD_LOG:-$F/i1088a_yield.txt}
UNIT=${YIELD_UNIT:-i1025k111}
POLL=${YIELD_POLL:-30}
while systemctl --user is-active --quiet $UNIT; do
  if [ -n "${YIELD_FAKE_ACTIVE:-}" ] || [ -n "$(systemctl --user list-units 'i1088a-*' --state=active --no-legend 2>/dev/null)" ]; then
    for p in $(pgrep -f "$PAT"); do
      [ "$p" = "$$" ] && continue
      case "$(ps -o comm= -p $p 2>/dev/null)" in python*|timeout|time) ;; *) continue;; esac   # compute processes and their wrappers only, not a shell whose command text matches
      r=$($F/renice_threads.sh $p 19)
      [ "${r%%/*}" != 0 ] && echo "$(date -u '+%F %T') UTC an i1088a unit is active: pid $p, $r threads reniced to 19 ($(ps -o cmd= -p $p | cut -c1-70))" >> $LOG
    done
  fi
  sleep $POLL
done
