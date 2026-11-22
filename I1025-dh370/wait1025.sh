#!/usr/bin/env bash
# #1025 leap wake: fires when the leap's jsonl reaches D >= $1, or a 'fold watch' / 'failed at' line count exceeds $2 / $3, or the leap stops or ends ('stop at', 'reached D', unit i1025a inactive).
# usage: bash wait1025.sh TARGET_D FOLD_BASE FAIL_BASE      e.g. bash wait1025.sh 19 0 0
LOG=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc63_leap/leap.log
J=/home/nathan/Source/choptuik-large-d-1025/solver/matter/data/l1kc63dh370.jsonl
while sleep 20; do
  d=$(python3 -I -c "
import json,sys
m=0
try:
    for l in open('$J'): m=max(m,json.loads(l)['D'])
except Exception: pass
print(m)")
  python3 -I -c "import sys; sys.exit(0 if float('$d') >= float('$1')-1e-9 else 1)" && { echo "REACHED D $d (target $1)"; exit 0; }
  f=$(grep -c 'fold watch' $LOG 2>/dev/null); [ "${f:-0}" -gt "${2:-0}" ] && { echo "FOLD WATCH lines $f > $2 (D $d)"; grep 'fold watch' $LOG | tail -2 | cut -c1-240; exit 0; }
  g=$(grep -c '^failed at' $LOG 2>/dev/null); [ "${g:-0}" -gt "${3:-0}" ] && { echo "FAILED lines $g > $3 (D $d)"; grep '^failed at' $LOG | tail -2 | cut -c1-240; exit 0; }
  grep -qE '^stop at|^reached D|Traceback' $LOG 2>/dev/null && { echo "LEAP ENDED (D $d)"; tail -3 $LOG | cut -c1-240; exit 0; }
  [ "$(systemctl --user is-active i1025a)" != active ] && { echo "UNIT i1025a not active (D $d)"; tail -3 $LOG | cut -c1-240; exit 0; }
done
