#!/usr/bin/env bash
# #1032 runner checks: usage: bash wait1032.sh checks|ab
# checks: wakes at once when a check exits other than expected (mock floor time bits accuracy 0, bits_ulp acc_sign acc_nobar 1), a control's log has a Traceback, or the unit ends early; else when all eight logs have an exit line.
# ab: wakes when the unit i1032a ends (step_new and step_old done), or at once when step_new.log ends with a Traceback.
D=/home/nathan/Source/choptuik-large-d-raw-wt613/I1032-dh370
declare -A want=([mock]=0 [floor]=0 [time]=0 [bits]=0 [accuracy]=0 [bits_ulp]=1 [acc_sign]=1 [acc_nobar]=1)
while sleep 15; do
  if [ "$1" = checks ]; then
    done_n=0
    for n in "${!want[@]}"; do
      [ -f $D/$n.log ] || continue
      e=$(grep -m1 '^exit ' $D/$n.log | cut -d' ' -f2)
      [ -z "$e" ] && continue
      done_n=$((done_n+1))
      [ "$e" != "${want[$n]}" ] && { echo "VIOLATION $n exit $e (want ${want[$n]})"; tail -3 $D/$n.log | cut -c1-200; exit 0; }
      [ "${want[$n]}" = 1 ] && grep -q '^Traceback' $D/$n.log && { echo "CONTROL $n exited 1 with a Traceback"; exit 0; }
    done
    [ $done_n -ge 8 ] && { echo "CHECKS DONE 8"; exit 0; }
    [ "$(systemctl --user is-active i1032a)" != active ] && { echo "UNIT ENDED early, $done_n checks done"; exit 0; }
  else
    grep -q '^Traceback' $D/step_new.log 2>/dev/null && { echo "TRACEBACK step_new"; exit 0; }
    [ "$(systemctl --user is-active i1032a)" != active ] && { echo "UNIT ENDED"; exit 0; }
  fi
done
