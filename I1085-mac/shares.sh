#!/bin/bash
# #1085: the falling mode's share of the records' dDelta_dF, from the geom logs' J mode lines (the mode with |delta| > 0.1)
# and the records' dDelta_dF at that D. usage: bash shares.sh GEOM.log RECORD.jsonl D  (prints one row)
log=$1; rec=$2; D=$3
dd=$(jq -r "select(.D == $D) | .dDelta_dF" "$rec" | tail -1)
grep "J mode m" "$log" | awk -v dd="$dd" -v D="$D" -v f="$(basename "$log")" '
  { s = $8; sub(",", "", s); d = $11; sub(",", "", d); s = s + 0; d = d + 0; if (d < 0) d = -d
    if (d > 0.1) { r = d / s; printf "%s D %s: falling mode sigma %s, |delta| %s, |delta|/sigma %.4e, record dDelta_dF %.4e, share of the square %.4f\n", f, D, s, d, r, dd, (r / dd) ^ 2 } }'
