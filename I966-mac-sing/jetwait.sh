#!/bin/bash
# fires when origin/main gains a saved jet (jet_pin3_D*.npz) under I966-dh370/ks_chain3b/, or after CAP_MIN minutes.
# Usage: jetwait.sh CAP_MIN. Fetch failures (a lock held by another fetch) are retried at the next check.
set -u
{
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad; CAP=$1
cd $S/raw1021push
list() { git ls-tree -r --name-only origin/main I966-dh370/ks_chain3b/ | grep -E '/jet_pin3_D[0-9.]+[.]npz$' | sort; }
git fetch -q origin 2>/dev/null; k0=$(list)
for i in $(seq 1 $CAP); do
  sleep 60
  if [ $((i % 2)) -eq 0 ]; then git fetch -q origin 2>/dev/null || continue
    new=$(comm -13 <(echo "$k0") <(list)); [ -n "$new" ] && { echo "new jets at $(git rev-parse --short origin/main):"; echo "$new"; break; }; fi
done
date -u "+%F %T"; true
exit
}
