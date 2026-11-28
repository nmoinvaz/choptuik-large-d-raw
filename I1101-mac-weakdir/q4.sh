#!/bin/bash
{
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101
while pgrep -f "w1101/q2b.sh" > /dev/null; do sleep 20; done
TH=2 TOL=1e-5 B12=fast $W/A/vroot.sh ne1 2.24 2.40
echo "$(date -u '+%Y-%m-%d %H:%M:%S') q4 done" >> $W/A/run_vroots.log
exit
}
