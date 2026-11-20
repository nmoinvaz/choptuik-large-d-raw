#!/bin/bash
# #1021: sheet check of dh610's b21-25-fu cache before the merge: along grid lines, along the b21-25 job's leaves and
# along every follow-up pass's leaves, and the planted switch (must exit 1).
#   sheet_fu.sh DH PY      DH: I1021-dh610 at raw 18338ce4; PY: python. From I1021-mac/merge_fu; writes nothing.
set -u
{ # read whole before it runs
DH=$1; P=$2; cd "$(dirname "$0")" || exit 1
SC=../diag/sheet_check.py; F=$DH/b21-25-fu; C=$F/points_M3_r0.17.jsonl
echo "cache b21-25-fu/points_M3_r0.17.jsonl: $(wc -l < $C | tr -d ' ') lines, sha256 $(shasum -a 256 $C | cut -c1-16)"
nice -n 19 $P $SC $C lines; echo "exit $?"
for L in $DH/b21-25/leaves_M3_cand_r0.17_fix_b21-25_998fd290.jsonl $F/leaves_fu_step*_pass*.jsonl; do
  nice -n 19 $P $SC $C "$L"; echo "exit $?"
done
nice -n 19 $P $SC $C lines --mutate=switch | tail -3; echo "exit (mutate=switch, must be 1) ${PIPESTATUS[0]}"
exit
}
