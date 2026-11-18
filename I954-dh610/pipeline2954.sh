#!/bin/bash
# #954: the pipeline restarted at build C (the branch moved to 6d7b2927): build C, then the checks of A, B, C and D (the amendment), one after the other, 8 threads, nice 10.
. "$(dirname "$0")/common954.sh"
D=$(dirname "$0")
bash $D/buildC954.sh; grep -q '^exit 0' $OUT/buildC.log || { echo "$(stamp) UTC build C failed" >> $OUT/pipeline.txt; exit 1; }
echo "$(stamp) UTC build C done, checks A" >> $OUT/pipeline.txt
bash $D/checksA.sh; echo "$(stamp) UTC checks A done, checks B" >> $OUT/pipeline.txt
bash $D/checksB.sh; echo "$(stamp) UTC checks B done, checks C" >> $OUT/pipeline.txt
bash $D/checksC.sh; echo "$(stamp) UTC checks C done, checks D" >> $OUT/pipeline.txt
bash $D/checksD.sh; echo "$(stamp) UTC checks D done" >> $OUT/pipeline.txt
