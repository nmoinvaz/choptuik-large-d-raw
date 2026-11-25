#!/bin/bash
# watch_end.sh M: tells the coordinator once when the unit i1090-m$M ends and why (a Python traceback in its journal, or the cap / the script's own stop / the last D done); alert-only, restarts and stops nothing.
M=$1; F=/home/nathan/Source/choptuik-large-d-raw/I1090-dh610; T5="nathans-macbook-air-m5-3/t5"; U=i1090-m$M; t0=$(date '+%F %T')
while [ "$(systemctl --user is-active $U)" = active ]; do sleep 30; done
tb=$(journalctl --user -u $U --since "$t0" --no-pager 2>/dev/null | grep -c "Traceback")
last=$(journalctl --user -u $U --since "$t0" --no-pager 2>/dev/null | grep -E "Error|Traceback|not converged|stop" | tail -n 1 | cut -c1-220)
echo "$(date -u '+%F %T') UTC unit $U ended (traceback lines $tb): $last" >> $F/end_M$M.txt
hc send "$T5" "dh610 i1090 (auto): unit $U ended (python tracebacks in its journal: $tb). last relevant line: $last. last log line: $(tail -n 1 $F/dd_M${M}_cont2/solve_dd_cont.log | cut -c1-200)" > /dev/null 2>&1
