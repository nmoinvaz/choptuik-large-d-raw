#!/bin/bash
# waits until the 1-minute load average is below the limit, then runs the command (#845: the kernel runs only at a
# load below about 30) and returns its exit status. Usage: gate.sh <limit> <log> <command ...>
LIMIT=$1; LOG=$2; shift 2
while :; do
    L=$(sysctl -n vm.loadavg | awk '{print $2}')
    if awk -v l="$L" -v m="$LIMIT" 'BEGIN {exit !(l < m)}'; then break; fi
    echo "$(date -u '+%F %T') UTC waiting: load $L" >> "$LOG"
    /bin/sleep 60
done
echo "$(date -u '+%F %T') UTC start: load $L" >> "$LOG"
"$@"
rc=$?
echo "$(date -u '+%F %T') UTC exit $rc" >> "$LOG"
exit $rc
