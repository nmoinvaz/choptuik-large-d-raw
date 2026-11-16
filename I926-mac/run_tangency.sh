#!/bin/bash
# the gap line through the M 320 records (last 3, 4, 6 states by smallest D) and its control; from hp/ of wip/sa-926
PY=${PY:-python3}
R=${R:-../../choptuik-large-d-raw/I926-mac}
for opt in "--last 3" "--last 4" "--last 6" "--last 3 --mutate slope"; do
    echo "== tangency depth_M320.jsonl --M 320 $opt"
    $PY sonic_valley.py tangency $R/depth_M320.jsonl --M 320 $opt
    echo "exit $?"
done
