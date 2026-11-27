#!/bin/bash
{
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101
I=$W/in
TH=2 TOL=1e-6 B12=fast $W/B/root.sh l1kc55k035m 2.238 2.252
cd /Users/nathan/Source/choptuik-1101w/solver/matter
echo "$(date -u '+%Y-%m-%d %H:%M:%S') ne starts" >> $W/A/run_vroots.log
VECLIB_MAXIMUM_THREADS=2 nice -n 10 /Users/nathan/venv-1025dd/bin/python -u i1101_weakdir.py ne $I/l1kc55u040.jsonl $I/sol_l1kc55u040_D16.0000.npy 16.0 $W/A/ne --outer=6 > $W/A/ne_u40.log 2>&1
echo "$(date -u '+%Y-%m-%d %H:%M:%S') ne exit $?" >> $W/A/run_vroots.log
TH=2 TOL=1e-7 B12=fast $W/B/root.sh l1kc55u040 2.238 2.252
TH=2 TOL=1e-6 B12=fast $W/A/vroot.sh w10 2.246 2.266
TH=2 TOL=1e-6 B12=fast $W/A/vroot.sh w001 2.238 2.256
echo "$(date -u '+%Y-%m-%d %H:%M:%S') q1c done" >> $W/A/run_vroots.log
exit
}
