#!/bin/bash
# #1025 kc87_leg: push the live folder (every accepted state and the record file) to raw main from the separate push worktree of the raw clone (AGENTS.md: not from the live clone while the job writes),
# then print the commit and the blobs of the state of D $1 and of the record file as pushed (dh170 scans lambda_1 on the states; a growing record is pinned by commit).
# usage: push_point.sh 21.03125 "message"
{
D=$1; MSG=$2
LIVE=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc87_leg
RAW=/home/nathan/Source/choptuik-large-d-raw-push960
S=$(printf "sol_l1kc87Ldh370_D%.6f.npy" $D)
[ -s $LIVE/$S ] || { echo "no $LIVE/$S"; exit 1; }
# the record file must hold the line of D (the copy loop copies state and record together every 120 s)
python3 - <<PY || { echo "the record file has no line for D $D"; exit 1; }
import json, sys
r = [json.loads(l) for l in open("$LIVE/l1kc87Ldh370.jsonl") if l.strip()]
sys.exit(0 if any(abs(x["D"] - $D) < 1e-9 for x in r) else 1)
PY
c=$(bash $LIVE/push_kc87.sh "$MSG" | tail -1)
echo "raw commit $c: state $S blob $(git -C $RAW rev-parse --short=8 HEAD:I1025-dh370/kc87_leg/$S), record l1kc87Ldh370.jsonl blob $(git -C $RAW rev-parse --short=8 HEAD:I1025-dh370/kc87_leg/l1kc87Ldh370.jsonl) ($(grep -c . $LIVE/l1kc87Ldh370.jsonl) lines)"
exit 0
}
