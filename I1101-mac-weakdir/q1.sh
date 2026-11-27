#!/bin/bash
{
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101
while pgrep -f "B/root.sh l1kc55k035m" > /dev/null; do sleep 20; done
$W/B/root.sh l1kc55u040 2.238 2.252
$W/A/vroot.sh w10 2.246 2.266
$W/A/vroot.sh w001 2.238 2.256
echo "$(date -u '+%Y-%m-%d %H:%M:%S') q1 done" >> $W/A/run_vroots.log
exit
}
