#!/bin/bash
# I249-macm3: the progress table for the four counts (determinants, edges done of 14, last edge finished, mismatches in any pass / last pass over the finished edges)
cd ~/Source/choptuik-large-d
R=../choptuik-large-d-raw/I249-macm3
echo "| D | determinants | edges done of 14 | seconds per determinant | mismatches (any pass / last pass) over the finished edges |"
echo "|---|---|---|---|---|"
for T in D56.0117 D57.0333 D58.0060 D59.0250
do
  n=$(wc -l < $R/$T/data/modecount_${T}_M48_kf23_evals.jsonl | tr -d ' ')
  e=$(grep -c '  edge ' $R/$T/count.log)
  s=$(grep -E 'evaluations,' $R/$T/count.log | tail -1 | sed 's/.*, \([0-9.]*\) s each/\1/')
  m=$(grep '  edge ' $R/$T/count.log | sed 's/.*mismatch \([0-9]*\), last pass \([0-9]*\)).*/\1 \2/' | awk '{a+=$1; b+=$2} END {print a " / " b}')
  echo "| ${T#D} | $n | $e | $s | $m |"
done
