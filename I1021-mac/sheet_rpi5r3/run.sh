#!/bin/bash
# #1013: the sheet check of rpi5's recount3 (the upper box's 13 cells at xi1 0.18, 6da7da7b), as sheet_rpi5fix's.
#   run.sh RP PY      RP: I1013-rpi5-cap extracted at the raw commit used; PY: python. From I1021-mac/sheet_rpi5r3.
# Checks, each written before the run: diag/sheet_check.py along grid lines of the 0.18 cache, and of the pool of the
# sheetfix's 0.17 cache with the 0.18 cache after it (F_3 does not depend on xi1 on a sheet, so a 0.18 value replaces
# its 0.17 twin and must sit on its neighbours' sheet); on recount3's leaves with --count, when the leaves exist (argcount
# writes them only at the end); diag/nearest_f3.py of the 0.18 and 0.17 records against the sheetfix's 0.17 cache.
# Controls, which must fail: --mutate=switch, and nearest_f3.py on step 2's 11 removed off-sheet records.
set -u
{ # read whole before it runs
RP=$1; P=$2; cd "$(dirname "$0")" || exit 1
SC=../diag/sheet_check.py; NF=../diag/nearest_f3.py
C=$RP/recount3/m3/points_M3_r0.18.jsonl; C17=$RP/recount3/m3/points_M3_r0.17.jsonl
S17=$RP/sheetfix/m3/points_M3_r0.17.jsonl
L=$RP/recount3/m3/leaves_M3_recount3_r0.18.jsonl; K=$RP/recount3/m3/count_M3_recount3_r0.18.json
mkdir -p in
(cd "$RP" && shasum -a 256 recount3/m3/* sheetfix/m3/points_M3_r0.17.jsonl recount3/removed_11_points.jsonl) > in/SHA256SUMS
cat "$S17" "$C" > in/pool_sheetfix017_recount3018.jsonl
{ echo "0.18 cache $(wc -l < $C | tr -d ' ') lines, recount3's 0.17 file $(wc -l < $C17 | tr -d ' ') lines; leaves $( [ -e $L ] && echo present || echo absent)"
  nice -n 19 $P $SC $C lines; echo "exit $?"
  nice -n 19 $P $SC in/pool_sheetfix017_recount3018.jsonl lines; echo "exit $?"
  if [ -e $L ]; then
    nice -n 19 $P $SC $C $L --count $K; echo "exit $?"
    nice -n 19 $P $SC in/pool_sheetfix017_recount3018.jsonl $L --count $K; echo "exit $?"
  fi
  nice -n 19 $P $NF $S17 $C $C17; echo "exit $?"
} > sheet_check.log 2>&1
{ nice -n 19 $P $SC in/pool_sheetfix017_recount3018.jsonl lines --mutate=switch | tail -3; echo "exit (mutate=switch, must be 1) ${PIPESTATUS[0]}"
  nice -n 19 $P $NF $S17 $RP/recount3/removed_11_points.jsonl; echo "exit (nearest_f3 on the 11 removed records, must be 1) $?"
} > sheet_check_mutate.log 2>&1
cat sheet_check.log sheet_check_mutate.log
exit
}
