#!/bin/bash
# fires when origin/main gains an .npz under I1064-dh610/front_D262.7908/, or after CAP_MIN minutes. Usage: jetwait1064.sh CAP_MIN
set -u
{
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad; CAP=$1
cd $S/raw1021push
list() { git ls-tree -r --name-only origin/main I1064-dh610/front_D262.7908/ 2>/dev/null | grep -E '[.]npz$' | sort; }
git fetch -q origin 2>/dev/null; k0=$(list)
for i in $(seq 1 $CAP); do
  sleep 60
  if [ $((i % 4)) -eq 1 ]; then git fetch -q origin 2>/dev/null || continue
    new=$(comm -13 <(echo "$k0") <(list)); [ -n "$new" ] && { echo "new front jets at $(git rev-parse --short origin/main):"; echo "$new"; break; }; fi
done
date -u "+%F %T"; true
exit
}
