#!/bin/bash
# sheet check of the merged cache: along grid lines, along every part's leaves, and the planted switch (must exit 1)
R=$1; P=$2; SC=$R/diag/sheet_check.py; cd "$(dirname "$0")"
nice -n 19 $P $SC merged.jsonl lines; echo "exit $?"
for L in ../m3/leaves_M3_cand_r0.17_fix_b07-10.jsonl in/leaves_M3_cand_r0.17_fix_b11-15.jsonl \
         in/leaves_M3_cand_r0.17_fix_b16-20.jsonl in/leaves_M3_cand_r0.17_fix_b21-25_998fd290.jsonl \
         in/leaves_M3_cand_r0.17_fix_b26-31_998fd290.jsonl; do
  nice -n 19 $P $SC merged.jsonl "$L"; echo "exit $?"
done
nice -n 19 $P $SC merged.jsonl lines --mutate=switch | tail -3; echo "exit (mutate=switch, must be 1) ${PIPESTATUS[0]}"
