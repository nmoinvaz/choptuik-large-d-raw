#!/bin/bash
# push_i1090.sh: the coordinator's order (hc, 25 Nov): push I1090-dh610/ at each D (the dd_M12_cont and dd_M14_cont folders grow by one json per D and a log). Polls every 120 s; pushes the folder (scratchpad/push_folder.sh: flock,
# make_index, rebase, push from the separate worktree) when a new D json appeared, or when a log grew and 30 min passed since the last push; ends when both units i1090-m12 and i1090-m14 have ended (one last push).
F=/home/nathan/Source/choptuik-large-d-raw/I1090-dh610; PUSH=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/push_folder.sh
lastj=""; lastl=""; tl=0; seen=0; t00=$(date +%s)
while :; do
  a=$(systemctl --user is-active i1090-m12 i1090-m14 | grep -c '^active')
  sj=$(ls $F/dd_M12_cont/sdd_D*.json $F/dd_M14_cont/sdd_D*.json 2>/dev/null | md5sum | cut -c1-12)
  sl=$(cat $F/dd_M12_cont/*.log $F/dd_M14_cont/*.log 2>/dev/null | wc -c)
  now=$(date +%s); [ $a -gt 0 ] && seen=1
  if [ "$sj" != "$lastj" ] || { [ "$sl" != "$lastl" ] && [ $(( now - tl )) -ge 1800 ]; } || { [ $a = 0 ] && [ "$sl" != "$lastl" ]; }; then
    n12=$(ls $F/dd_M12_cont/sdd_D*.json 2>/dev/null | wc -l); n14=$(ls $F/dd_M14_cont/sdd_D*.json 2>/dev/null | wc -l)
    if bash $PUSH I1090-dh610 "I1090-dh610: dd continuation, D done: M12 $n12, M14 $n14" > $F/push_last.txt 2>&1; then lastj=$sj; lastl=$sl; tl=$now; fi
    echo "$(date -u '+%F %T') UTC push (M12 $n12 D, M14 $n14 D): $(tail -n 1 $F/push_last.txt)" >> $F/pushes.txt
  fi
  [ $a = 0 ] && { [ $seen = 1 ] || [ $(( now - t00 )) -gt 900 ]; } && [ "$sj" = "$lastj" ] && [ "$sl" = "$lastl" ] && break
  sleep 120
done
