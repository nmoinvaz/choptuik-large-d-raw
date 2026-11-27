#!/bin/bash
{
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101
I=$W/in
while pgrep -f "B/root.sh l1kc55k035m" > /dev/null; do sleep 20; done
cd /Users/nathan/Source/choptuik-1101w/solver/matter
echo "$(date -u '+%Y-%m-%d %H:%M:%S') ne starts" >> $W/A/run_vroots.log
VECLIB_MAXIMUM_THREADS=2 nice -n 10 /Users/nathan/venv-1025dd/bin/python -u i1101_weakdir.py ne $I/l1kc55u040.jsonl $I/sol_l1kc55u040_D16.0000.npy 16.0 $W/A/ne --outer=6 > $W/A/ne_u40.log 2>&1
echo "$(date -u '+%Y-%m-%d %H:%M:%S') ne exit $?" >> $W/A/run_vroots.log
$W/B/root.sh l1kc55u040 2.238 2.252
$W/A/vroot.sh w10 2.246 2.266
$W/A/vroot.sh w001 2.238 2.256
echo "$(date -u '+%Y-%m-%d %H:%M:%S') q1b done" >> $W/A/run_vroots.log
exit
}
