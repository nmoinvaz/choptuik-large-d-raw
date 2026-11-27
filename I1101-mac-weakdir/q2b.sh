#!/bin/bash
{
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101
M=/Users/nathan/Source/choptuik-1101w/solver/matter
while pgrep -f "B/run_B.sh" > /dev/null; do sleep 20; done
for t in l1kc55k050m l1kc55k025m l1kc55k070m; do
  cp $M/data/$t.jsonl $M/data/sol_${t}_D16.0000.npy $W/B/in/
  TH=2 TOL=1e-6 B12=fast $W/B/root.sh $t 2.238 2.252
done
echo "$(date -u '+%Y-%m-%d %H:%M:%S') q2b done" >> $W/B/run_roots.log
exit
}
