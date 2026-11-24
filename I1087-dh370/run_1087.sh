#!/bin/bash
# #1087 T2: the five rungs, one at a time (4 threads, nice 10, each capped at its first "on 0: |F|" line or 3600 s, exact pid).
# The line's --base_polish 0 is replaced by --base_polish 1 (README). Control: K 293's starting |F| must print as the state's own 1.04e-38;
# otherwise the chain stops after K 293. results.txt gets one row per rung.
{
D=/home/nathan/Source/choptuik-large-d-raw-wt613/I1087-dh370
cd $D || exit 9
echo "# $(date -u '+%F %T') UTC start; K, starting |F| (first 'on 0: |F|' line), seconds to that line, how it ended" >> results.txt
for K in 293 315 330 360 420; do
  bash $D/run_rung.sh $K p1 3600 --base_polish 1 > /dev/null 2>&1
  L=$(grep -m1 -E 'on 0: \|F\| ' $D/ks${K}_p1/stdout.log)
  A=$(echo "$L" | sed -E 's/.*on 0: \|F\| ([0-9.e+-]+).*/\1/')
  S=$(sed -nE 's/.*seconds to that point ([0-9]+);.*/\1/p' $D/ks${K}_p1/rung.txt)
  H=$(sed -nE 's/.*ended by: (.*); seconds.*/\1/p' $D/ks${K}_p1/rung.txt)
  echo "$(date -u '+%F %T') UTC K $K: A $A, $S s, ended by $H; line: $L" >> results.txt
  if [ "$K" = 293 ] && [ "$A" != "1.04e-38" ]; then echo "$(date -u '+%F %T') UTC CONTROL K 293: A '$A' is not the state's own 1.04e-38: stop" >> results.txt; echo stop > STOP.txt; exit 1; fi
  if [ -z "$A" ]; then echo "$(date -u '+%F %T') UTC K $K printed no on 0 line: stop" >> results.txt; echo stop > STOP.txt; exit 1; fi
done
echo "$(date -u '+%F %T') UTC done" >> results.txt
exit 0
}
