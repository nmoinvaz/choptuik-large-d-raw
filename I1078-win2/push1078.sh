#!/bin/bash
# copy the live folder (D:\choptuik-raw-i1078\I1078-win2) into the push worktree and push it; never touches the live clone's git state
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
MSG=${1:-"I1078-win2: progress"}
P=/d/choptuik-raw-i1078p
cd $P || exit 1
mkdir -p I1078-win2
cp -r /d/choptuik-raw-i1078/I1078-win2/. I1078-win2/
git fetch -q origin && git rebase -q origin/main 2>/dev/null || git rebase --abort 2>/dev/null
python make_index.py > /dev/null && git add I1078-win2 INDEX.md && git commit -q -m "$MSG"
for i in 1 2 3; do
  git pull -q --rebase origin main && git push -q origin HEAD:main && { echo "pushed $(git rev-parse --short=8 HEAD)"; exit 0; }
  sleep 5
done
echo "push FAILED"; exit 1
