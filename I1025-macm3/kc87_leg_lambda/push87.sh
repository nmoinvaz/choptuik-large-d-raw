#!/bin/bash
# push the live folder I1025-macm3/kc87_leg_lambda to raw (from the clean push worktree): bash push87.sh "commit message"
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
W=$HOME/Source/choptuik-large-d-raw-1076p
LOCK=$HOME/Source/.rawpush1076p.lock      # one push at a time into the shared push worktree (mkdir is atomic)
n=0; until mkdir $LOCK 2>/dev/null; do n=$((n+1)); [ $n -gt 120 ] && { echo "push lock busy"; exit 1; }; sleep 2; done
trap 'rmdir $LOCK 2>/dev/null' EXIT
cd $W || exit 1
git fetch -q && git merge -q --ff-only origin/main || { echo "ff-only merge failed"; exit 1; }
mkdir -p I1025-macm3/kc87_leg_lambda && rsync -a $L/ I1025-macm3/kc87_leg_lambda/ || exit 1
python3 make_index.py > /dev/null && git add I1025-macm3/kc87_leg_lambda INDEX.md && git commit -q -m "$1" || { echo "commit failed or nothing to commit"; exit 1; }
for i in 1 2 3; do
  git pull -q --rebase origin main && git push -q origin HEAD:main && { echo "pushed $(git log -1 --format=%h)"; exit 0; }
  sleep 5
done
echo "push failed"; exit 1
