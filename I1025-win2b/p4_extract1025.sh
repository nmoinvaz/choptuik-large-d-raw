#!/usr/bin/env bash
# #1025 P4 (amendment 7), win2b: extract the driver, the pinned row list and every input the rows name from a raw clone's origin/main by git show (LF bytes, no checkout, no live folder touched)
# into a FRESH directory, and check each file's blob (git hash-object --no-filters) against the pinned id and against the tree's own blob id. Refuses if the directory exists or any blob differs.
# usage: bash p4_extract1025.sh RAWCLONE DEST [PAIRS_FILE]     (PAIRS_FILE: lines "path blob"; default: the pins below)
set -u
R=$1; DEST=$2; PAIRS=${3:-}
[ -e "$DEST" ] && { echo "refuse: $DEST exists (use a fresh directory)"; exit 2; }
if [ -z "$PAIRS" ]; then PAIRS_TXT="I1025-mac/p4_driver_rows.sh e004c9ec5c722578b460a1354adc337626e75129
I1025-mac/p4_hybrid.py a402559b5d37661b49da50f07f877af21fd29b3a
I1025-mac/out/l1kc55Fb1025.jsonl 5be40af42cdcf2c1c3751c1b28a03884759fcbd4
I1025-mac/out/sol_l1kc55Fb1025_D16.0000.npy 94c8b04878559d3ccdaef9535d4af6280d50edaf
I1025-mac/p4_rows_win2b.txt e0c173234c69941b16135ea529145c391599d80a
I1025-win2b/out/l1kc71Fw1025c.jsonl 0d174f3abea1dcc8f78dbe17ac5ee66980f7116b
I1025-win2b/out/sol_l1kc71Fw1025c_D16.5000.npy 8c8aa44ed5ca1e6349399f73311e50be580ec45c"
else PAIRS_TXT=$(cat "$PAIRS"); fi
head=$(git -C "$R" rev-parse --short=8 origin/main)
bad=0
while read -r p b; do
  [ -z "$p" ] && continue
  mkdir -p "$DEST/$(dirname "$p")"
  git -C "$R" show "origin/main:$p" > "$DEST/$p" 2> /dev/null || { echo "FAIL $p: not in origin/main $head"; bad=1; continue; }
  t=$(git -C "$R" rev-parse "origin/main:$p"); h=$(git hash-object --no-filters "$DEST/$p")
  if [ "$h" = "$b" ] && [ "$t" = "$b" ]; then echo "ok   $h $p"; else echo "FAIL $p: pinned $b, tree $t, extracted $h"; bad=1; fi
done <<< "$PAIRS_TXT"
echo "origin/main $head; $( [ $bad = 0 ] && echo 'all blobs match' || echo 'MISMATCH' ) ($(date -u '+%Y-%m-%d %H:%M:%S UTC'))"
exit $bad
