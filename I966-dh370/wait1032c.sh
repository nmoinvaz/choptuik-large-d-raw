#!/usr/bin/env bash
# #1032 second round (hc 2026-11-19): usage bash wait1032c.sh old|rest
#  old : wakes when the old-head step_new has ended (step_new_ended.txt), or on a cap.
#  rest: wakes at once on an exit 2 of any check, a control exiting 0 (or not 1), accuracy2/time2 exiting other than 0, 'no basin plant', a Traceback in step_new2.log,
#        a cap (3x the estimate) exceeded by a running proj_check/anm_run pid; else when time2 has ended (checks done), and when the unit i1032b has ended (A/B done).
D=/home/nathan/Source/choptuik-large-d-raw-wt613/I1032-dh370
cap() { # pid -> prints cap seconds for its command, nothing if not one of ours
  c=$(tr '\0' ' ' < /proc/$1/cmdline 2>/dev/null)
  case "$c" in
    *"proj_check.py accuracy"*"--mutate sign"*|*"proj_check.py accuracy"*"--mutate o_nobar"*) echo 2700;;
    *"proj_check.py accuracy"*) echo 8100;;
    *"proj_check.py time"*) echo 4500;;
    *"I1032-dh370/step_new2 "*) echo 7200;;
    *"I1032-dh370/step_old2 "*) echo 12600;;
    *"I1032-dh370/step_new --state"*) echo 7200;;
  esac
}
while sleep 15; do
  for p in $(cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/i1032b.service/cgroup.procs 2>/dev/null) 798427; do
    k=$(cap $p); [ -z "$k" ] && continue
    et=$(ps -o etimes= -p $p 2>/dev/null | tr -d ' '); [ -z "$et" ] && continue
    [ "$et" -gt "$k" ] && { echo "CAP exceeded: pid $p ran $et s, cap $k s: $(tr '\0' ' ' < /proc/$p/cmdline | cut -c1-200)"; exit 0; }
  done
  if [ "$1" = old ]; then
    [ -f $D/step_new_ended.txt ] && { echo "OLD step_new ended: $(cat $D/step_new_ended.txt)"; exit 0; }
    continue
  fi
  for n in accuracy2 acc_sign2 acc_nobar2 time2; do
    [ -f $D/$n.log ] || continue
    e=$(grep -m1 '^exit ' $D/$n.log | cut -d' ' -f2); [ -z "$e" ] && continue
    [ "$e" = 2 ] && { echo "CHECK ERROR $n exit 2"; tail -4 $D/$n.log | cut -c1-200; exit 0; }
    case $n in acc_sign2|acc_nobar2) w=1;; *) w=0;; esac
    [ "$e" != "$w" ] && { echo "VIOLATION $n exit $e (want $w)"; tail -4 $D/$n.log | cut -c1-200; exit 0; }
    [ "$w" = 1 ] && grep -q '^Traceback' $D/$n.log && { echo "CONTROL $n exit 1 with a Traceback"; exit 0; }
  done
  grep -q 'no basin plant' $D/accuracy2.log 2>/dev/null && { echo "NO BASIN PLANT"; exit 0; }
  grep -q '^Traceback' $D/step_new2.log 2>/dev/null && { echo "TRACEBACK step_new2"; exit 0; }
  [ -n "$(grep -m1 '^exit ' $D/time2.log 2>/dev/null)" ] && [ -z "$(ls $D/CHECKS2_REPORTED 2>/dev/null)" ] && { echo "CHECKS2 DONE (time2 ended)"; touch $D/CHECKS2_REPORTED; exit 0; }
  [ "$(systemctl --user is-active i1032b)" = inactive ] && [ -f $D/step_new_ended.txt ] && { echo "UNIT i1032b ENDED"; exit 0; }
done
