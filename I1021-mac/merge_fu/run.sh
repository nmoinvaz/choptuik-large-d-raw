#!/bin/bash
# #1021: merge of the M = 3 parts at xi1 0.17 for the recount of record, and its checks: ../merge_dry/run.sh with
# dh610's b21-25-fu in place of b21-25 (raw 18338ce4) and the follow-up passes' leaves in the sheet check.
#   run.sh DH B2125 CODE PY      DH: I1021-dh610 at the raw commit used; B2125: b21-25 or b21-25-fu (its folder in DH);
#                                CODE: a worktree at 6da7da7b (argcount_merge.py, argcount_samebits.py); PY: python
# From I1021-mac/merge_fu. Inputs are copied to in/ (in/SHA256SUMS); the fix2931 part is the prefix plus fix2931's two
# records that value boxes 29-31's points (lines 889 and 808 of ../fix2931/points_M3_r0.17.jsonl). Writes merged.jsonl
# and the logs; each control must exit 1.
set -u
{ # read whole before it runs
DH=$1; B2125=$2; CODE=$3; PY=$4
cd "$(dirname "$0")" || exit 1
[ "$(git -C "$CODE" rev-parse HEAD)" = 6da7da7be3f2325208f2d4f9570a5e5a8790bd78 ] || { echo "CODE is not at 6da7da7b"; exit 1; }
[ -e merged.jsonl ] && { echo "merged.jsonl exists"; exit 1; }
IS=$CODE/solver/inner_stokes
mkdir -p in
cp -p ../m3/points_M3_r0.17.jsonl in/points_mac.jsonl
for b in b11-15 b16-20 b26-31; do cp -p "$DH/$b/points_M3_r0.17.jsonl" "in/points_$b.jsonl"; done
cp -p "$DH/$B2125/points_M3_r0.17.jsonl" in/points_$B2125.jsonl
cp -p "$DH"/b11-15/leaves_M3_cand_r0.17_fix_b11-15.jsonl "$DH"/b16-20/leaves_M3_cand_r0.17_fix_b16-20.jsonl \
      "$DH"/b21-25/leaves_M3_cand_r0.17_fix_b21-25_998fd290.jsonl "$DH"/b26-31/leaves_M3_cand_r0.17_fix_b26-31_998fd290.jsonl in/
[ "$B2125" = b21-25-fu ] && cp -p "$DH"/b21-25-fu/leaves_fu_step*_pass*.jsonl in/
{ cat ../split/points_M3_r0.17_in.jsonl; sed -n 889p ../fix2931/points_M3_r0.17.jsonl; sed -n 808p ../fix2931/points_M3_r0.17.jsonl; } > in/part_fix2931.jsonl
sed -n 889p ../fix2931/points_M3_r0.17.jsonl | cmp - ../fu_seed/point_3.6623456_1.06904321.jsonl || { echo "fix2931 line 889 is not fu_seed's"; exit 1; }
(cd in && shasum -a 256 *.jsonl > SHA256SUMS)
PARTS="in/points_b11-15.jsonl in/points_b16-20.jsonl in/points_$B2125.jsonl in/points_b26-31.jsonl in/part_fix2931.jsonl"
$PY $IS/argcount_merge.py merged.jsonl in/points_mac.jsonl ../split/points_M3_r0.17_in.jsonl $PARTS > merge.log 2>&1
echo "merge exit $?" >> merge.log
$PY $IS/argcount_merge.py merged_mutate.jsonl in/points_mac.jsonl ../split/points_M3_r0.17_in.jsonl $PARTS --mutate=prefix > merge_mutate.log 2>&1
echo "merge --mutate=prefix exit $? (must be 1)" >> merge_mutate.log
$PY ../diag/merge_check.py merged.jsonl spec.json > merge_check.log 2>&1; echo "exit $?" >> merge_check.log
$PY ../diag/merge_check.py merged.jsonl spec.json --mutate=noise > merge_check_mutate.log 2>&1
echo "exit $? (mutate=noise, must be 1)" >> merge_check_mutate.log
./sheet_dry.sh .. "$PY" > sheet_check.log 2>&1
{ for f in in/points_mac.jsonl $PARTS; do $PY $IS/argcount_samebits.py $f merged.jsonl; echo "exit $?"; done
  $PY $IS/argcount_samebits.py in/points_mac.jsonl merged.jsonl --mutate=flip; echo "exit (mutate=flip, must be 1) $?"; } > samebits.log 2>&1
grep -h -E '^merge|^merge check|sheet check|bit check|must be 1' merge.log merge_mutate.log merge_check.log merge_check_mutate.log sheet_check.log samebits.log
exit
}
