#!/bin/bash
# notify_i1090.sh: sends the coordinator an hc line at the first D of each unit, at "not converged", "stop", an error trace, and at D 245.64, D 263.60 and D 1000 of each log (alert-only helper; ends when both units ended).
F=/home/nathan/Source/choptuik-large-d-raw/I1090-dh610; T5="nathans-macbook-air-m5-3/t5"
( tail -n0 -F $F/dd_M12_cont2/solve_dd_cont.log $F/dd_M14_cont2/solve_dd_cont.log 2>/dev/null & echo $! > $F/notify_tail2.pid; wait ) | while read -r line; do
  case "$line" in
    "==> "*) cur=$(echo "$line" | grep -o 'M1[24]' | head -1);;
    *"not converged"*|*"stop"*|*Traceback*|*Error*|*"D   100.00  max"*|*"D   245.64  max"*|*"D   263.60  max"*|*"D  1000.00  max"*) hc send "$T5" "dh610 i1090 (auto) ${cur:-M?}: ${line:0:420}" > /dev/null 2>&1;;
  esac
  a=$(systemctl --user is-active i1090-m12 i1090-m14 | grep -c '^active'); [ $a = 0 ] && break
done
