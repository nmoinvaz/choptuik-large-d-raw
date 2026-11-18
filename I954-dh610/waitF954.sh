#!/bin/bash
. "$(dirname "$0")/common954.sh"
while ! grep -q 'checks E done' $OUT/pipeline.txt 2>/dev/null; do sleep 60; done
bash "$(dirname "$0")/checksF.sh"
echo "$(stamp) UTC checks F done" >> $OUT/pipeline.txt
