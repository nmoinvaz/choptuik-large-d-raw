#!/bin/bash
# #1079 dh610 stage 2 by hand (run_all.sh does not start it after the STOP line of exc1's controls C6, which the coordinator resolved): xload.sh of both zeros as soon as both chain scripts are done (2 processes), incl.sh of both when both h2.sh are done.
F=/home/nathan/Source/choptuik-large-d-raw/I1079-dh610; H=$F/steps.txt
stamp() { date -u '+%F %T'; }
until grep -q 'chain exc1 .* chain done' $H && grep -q 'chain exc2 .* chain done' $H; do sleep 20; done
echo "$(stamp) stage2: both chain scripts done: xload 1 and xload 2 start" >> $H
bash $F/xload.sh 1 & bash $F/xload.sh 2 &
until grep -q 'h2 exc1 .* h2 done' $H && grep -q 'h2 exc2 .* h2 done' $H; do
  grep -q 'STOP: h2 exc' $H && { echo "$(stamp) stage2: an h2 STOP line is in steps.txt; incl not started" >> $H; wait; exit 1; }
  sleep 20; done
echo "$(stamp) stage2: both h2 scripts done: incl 1 and incl 2 start" >> $H
bash $F/incl.sh 1 & bash $F/incl.sh 2 &
wait
echo "$(stamp) stage2: done" >> $H
