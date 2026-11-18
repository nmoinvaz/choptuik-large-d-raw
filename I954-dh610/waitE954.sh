#!/bin/bash
. "$(dirname "$0")/common954.sh"
while ! grep -q 'checks D done' $OUT/pipeline.txt 2>/dev/null; do sleep 60; done
bash "$(dirname "$0")/checksE.sh"
echo "$(stamp) UTC checks E done" >> $OUT/pipeline.txt
