#!/bin/bash
# #812 step 1 (the coordinator): R 0.05 lens circles at the conjugates of #789's upper lens zeros, on each cut's saved
# state (hp/data/modecount_state_D61.0264_M48_kf<K>.npz of the #749 worktree), two at a time at 3 threads each.
. /Users/nathan/Source/choptuik-large-d-raw-749/I812-macm3/common.sh
go 39 lensc 3.134817,-0.114564,0.05 3 &
go 41 lensc 3.149784,-0.190236,0.05 3 &
wait
go 43 lensc 3.204892,-0.174493,0.05 3 &
go 45 lensc 3.131662,-0.162740,0.05 3 &
wait
echo "812 run_812_lens.sh done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_812.txt
