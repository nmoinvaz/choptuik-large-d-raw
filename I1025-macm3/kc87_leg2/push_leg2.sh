#!/bin/bash
# push the live folder I1025-macm3/kc87_leg2 to raw (from the clean push worktree): bash push_leg2.sh "commit message"; prints "pushed <hash>"
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2
W=$HOME/Source/choptuik-large-d-raw-1076p
cd $W || exit 1
git fetch -q && git merge -q --ff-only origin/main || { echo "ff-only merge failed"; exit 1; }
mkdir -p I1025-macm3/kc87_leg2 && rsync -a --exclude 'work/' $L/ I1025-macm3/kc87_leg2/ || exit 1
python3 make_index.py > /dev/null && git add I1025-macm3/kc87_leg2 INDEX.md && git commit -q -m "$1" || { echo "commit failed or nothing to commit"; exit 1; }
for i in 1 2 3; do
  git pull -q --rebase origin main && git push -q origin HEAD:main && { echo "pushed $(git log -1 --format=%h)"; exit 0; }
  sleep 5
done
echo "push failed"; exit 1
