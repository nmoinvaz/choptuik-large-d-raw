#!/bin/bash
# #1013: the sheet check of rpi5's recount4 (recount3's 13 cells after the fu passes at xi1 0.18, 6da7da7b), as
# ../sheet_rpi5r3/run.sh with recount4's files. Checks, each written before the run: diag/sheet_check.py along grid lines
# of recount4's 0.18 cache, and of the pool of the sheetfix's 0.17 cache with recount4's 0.18 cache after it; on pass 1's
# leaves with --count; diag/nearest_f3.py of recount4's 0.18 and 0.17 records against the sheetfix's 0.17 cache; and
# prefix_keys.py (criterion 4 read as prefix and keys, independent of argcount_samebits.py).
# Controls, which must fail: --mutate=switch, nearest_f3.py on recount3's 11 removed off-sheet records, prefix_keys.py
# --mutate=edit.
#   run.sh RP PY      RP: I1013-rpi5-cap extracted at the raw commit used; PY: python. From I1021-mac/sheet_rpi5r4.
set -u
{ # read whole before it runs
RP=$1; P=$2; cd "$(dirname "$0")" || exit 1
SC=../diag/sheet_check.py; NF=../diag/nearest_f3.py
C=$RP/recount4/m3/points_M3_r0.18.jsonl; C17=$RP/recount4/m3/points_M3_r0.17.jsonl
S17=$RP/sheetfix/m3/points_M3_r0.17.jsonl; C3=$RP/recount3/m3/points_M3_r0.18.jsonl
L=$RP/recount4/m3/leaves_M3_recount4_pass1_r0.18.jsonl; K=$RP/recount4/m3/count_M3_recount4_pass1_r0.18.json
mkdir -p in
(cd "$RP" && shasum -a 256 recount4/m3/* recount3/m3/points_M3_r0.18.jsonl sheetfix/m3/points_M3_r0.17.jsonl recount3/removed_11_points.jsonl) > in/SHA256SUMS
cat "$S17" "$C" > in/pool_sheetfix017_recount4018.jsonl
{ echo "0.18 cache $(wc -l < $C | tr -d ' ') lines, recount4's 0.17 file $(wc -l < $C17 | tr -d ' ') lines"
  nice -n 19 $P $SC $C lines; echo "exit $?"
  nice -n 19 $P $SC in/pool_sheetfix017_recount4018.jsonl lines; echo "exit $?"
  nice -n 19 $P $SC $C $L --count $K; echo "exit $?"
  nice -n 19 $P $SC in/pool_sheetfix017_recount4018.jsonl $L --count $K; echo "exit $?"
  nice -n 19 $P $NF $S17 $C $C17; echo "exit $?"
  nice -n 19 $P -I prefix_keys.py $C3 $C; echo "exit $?"
} > sheet_check.log 2>&1
{ nice -n 19 $P $SC in/pool_sheetfix017_recount4018.jsonl lines --mutate=switch | tail -3; echo "exit (mutate=switch, must be 1) ${PIPESTATUS[0]}"
  nice -n 19 $P $NF $S17 $RP/recount3/removed_11_points.jsonl; echo "exit (nearest_f3 on the 11 removed records, must be 1) $?"
  nice -n 19 $P -I prefix_keys.py $C3 $C --mutate=edit | tail -1; echo "exit (prefix_keys --mutate=edit, must be 1) ${PIPESTATUS[0]}"
} > sheet_check_mutate.log 2>&1
cat sheet_check.log sheet_check_mutate.log
exit
}
