#!/bin/bash
# #1079 dh610: the whole rerun, 4 processes of 1 thread at nice 15 (the leg lane of ../I1025-dh610/kc79_leg keeps priority): chain.sh and h2.sh of both zeros at once (point, box, Krawczyk, H1, H3 / H2 covering),
# then incl.sh and xload.sh of both (4 processes). Each script stops itself at a failed step and writes STOP: to steps.txt; this driver goes on to the next stage only when no STOP: line was written.
{
F=/home/nathan/Source/choptuik-large-d-raw/I1079-dh610; H=$F/steps.txt
stamp() { date -u '+%F %T'; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge 8388608 ] || { echo "$(stamp) STOP: run_all: MemAvailable $av kB is below 8 GiB (refusing to start; nothing is stopped for memory)" >> $H; exit 1; }
echo "$(stamp) run_all: stage 1 starts (chain 1, chain 2, h2 1, h2 2; MemAvailable $av kB, load $(cut -d' ' -f1-3 /proc/loadavg))" >> $H
for s in "chain.sh 1" "chain.sh 2" "h2.sh 1" "h2.sh 2"; do bash $F/$s & done
wait
grep -q 'STOP:' $H && { echo "$(stamp) run_all: a STOP line is in steps.txt after stage 1; stage 2 not started" >> $H; exit 1; }
echo "$(stamp) run_all: stage 2 starts (incl 1, incl 2, xload 1, xload 2)" >> $H
for s in "incl.sh 1" "incl.sh 2" "xload.sh 1" "xload.sh 2"; do bash $F/$s & done
wait
grep -q 'STOP:' $H && { echo "$(stamp) run_all: a STOP line is in steps.txt after stage 2" >> $H; exit 1; }
echo "$(stamp) run_all: all stages done" >> $H
exit 0
}
