#!/bin/bash
# #1087 T2, amended (t5): K 293 once with --keep_plan 1 (the stored plan; must print the state's own 1.04e-38), then K 315, 330, 360, 420 with
# --keep_plan 0 as ordered (every K > 293 plans again). --base_polish 1 throughout. 4 threads, nice 10, each rung capped at its first
# "on 0: |F|" line or 3600 s by exact pid. results.txt gets one row per rung.
{
D=/home/nathan/Source/choptuik-large-d-raw-wt613/I1087-dh370
cd $D || exit 9
echo "# $(date -u '+%F %T') UTC start of the amended chain: K 293 with --keep_plan 1, then 315 330 360 420 with --keep_plan 0" >> results.txt
for K in 293 315 330 360 420; do
  if [ $K = 293 ]; then KPV=1; TAG=p1kp1; else KPV=0; TAG=p1; fi
  BP=1 KP=$KPV bash $D/run_rung.sh $K $TAG 3600 > /dev/null 2>&1
  L=$(grep -m1 -E 'on 0: \|F\| ' $D/ks${K}_$TAG/stdout.log)
  A=$(echo "$L" | sed -E 's/.*on 0: \|F\| ([0-9.e+-]+).*/\1/')
  S=$(sed -nE 's/.*seconds to that point ([0-9]+);.*/\1/p' $D/ks${K}_$TAG/rung.txt)
  H=$(sed -nE 's/.*ended by: (.*); seconds.*/\1/p' $D/ks${K}_$TAG/rung.txt)
  echo "$(date -u '+%F %T') UTC K $K keep_plan $KPV: A $A, $S s, ended by $H; line: $L" >> results.txt
  if [ "$K" = 293 ] && [ "$A" != "1.04e-38" ]; then echo "$(date -u '+%F %T') UTC CONTROL K 293 keep_plan 1: A '$A' is not the state's own 1.04e-38: stop" >> results.txt; echo stop > STOP.txt; exit 1; fi
  if [ -z "$A" ]; then echo "$(date -u '+%F %T') UTC K $K printed no on 0 line: stop" >> results.txt; echo stop > STOP.txt; exit 1; fi
done
echo "$(date -u '+%F %T') UTC done" >> results.txt
exit 0
}
