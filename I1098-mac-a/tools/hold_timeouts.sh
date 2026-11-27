#!/bin/bash
# #1098: lengthen the time limits of one ladder point's stages without stopping them. ladder_point2.sh runs each stage
# as `timeout 6h|4h|10h python ...`; at D >= 5555 a stage can need more. Every `timeout` process whose command names
# OUT is stopped (SIGSTOP), so its alarm stays pending and cannot end the child; when the child exits, the timeout is
# continued (SIGCONT) and exits with the child, or with 124 if its alarm is handled first, which the stage script only
# logs (it goes on when the stage's state file exists). New stop rule: a child still running CAP seconds after its
# timeout was stopped is ended by continuing the timeout, whose pending alarm then signals it as before.
#
#     hold_timeouts.sh OUT CAP_SECONDS LOG      (ends when OUT/run.log has a "job rc" line, or after 48 h)
{
O=$1; CAP=${2:-57600}; LOG=${3:-$1/hold_timeouts.log}
[ -d "$O" ] || { echo "usage: hold_timeouts.sh OUT CAP_SECONDS LOG"; exit 1; }
say() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" >> $LOG; }
say "start: OUT $O, CAP $CAP s"
end=$(( $(date +%s) + 172800 ))
seen=" "
while [ $(date +%s) -lt $end ]; do
  grep -q "^job rc" $O/run.log 2>/dev/null && { say "job rc in run.log: done"; break; }
  for T in $(pgrep -f "^timeout [0-9]+[smh]? .*$O/"); do
    case "$seen" in *" $T "*) continue;; esac
    C=$(pgrep -P $T | head -1)
    [ -n "$C" ] || continue
    kill -STOP $T || continue
    seen="$seen$T "
    say "stopped timeout $T (child $C: $(ps -o command= -p $C | cut -c1-160))"
    ( t0=$(date +%s)
      # a stopped timeout cannot reap its child, so an exited child stays a zombie (state Z), for which kill -0 succeeds
      while kill -0 $C 2>/dev/null && [ "$(ps -o stat= -p $C | cut -c1)" != Z ]; do
        if [ $(( $(date +%s) - t0 )) -gt $CAP ]; then say "child $C past CAP $CAP s: timeout $T continued, its alarm ends the child"; kill -CONT $T; exit; fi
        sleep 30
      done
      kill -CONT $T
      say "child $C ended; timeout $T continued" ) &
  done
  sleep 60
done
wait
say "end"
exit
}
