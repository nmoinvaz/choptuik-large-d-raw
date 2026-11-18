#!/bin/bash
# #954: after build954.sh (A and B) ends with "exit 0": build C, then the checks of A, B and C, one after the other (8 threads, nice 10).
. "$(dirname "$0")/common954.sh"
D=$(dirname "$0")
while ! grep -q '^exit' $OUT/build.log 2>/dev/null; do sleep 30; done
grep -q '^exit 0' $OUT/build.log || { echo "build954.sh failed" > $OUT/pipeline.txt; exit 1; }
echo "$(stamp) UTC builds A and B done, building C" >> $OUT/pipeline.txt
bash $D/buildC954.sh; grep -q '^exit 0' $OUT/buildC.log || { echo "$(stamp) UTC build C failed" >> $OUT/pipeline.txt; exit 1; }
echo "$(stamp) UTC build C done, checks A" >> $OUT/pipeline.txt
bash $D/checksA.sh; echo "$(stamp) UTC checks A done, checks B" >> $OUT/pipeline.txt
bash $D/checksB.sh; echo "$(stamp) UTC checks B done, checks C" >> $OUT/pipeline.txt
bash $D/checksC.sh; echo "$(stamp) UTC checks C done" >> $OUT/pipeline.txt
