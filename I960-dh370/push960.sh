#!/usr/bin/env bash
# copies the live folder into the push worktree and pushes it (the live folder is never touched by git). usage: bash push960.sh "message"
LIVE=/home/nathan/Source/choptuik-large-d-raw-wt613/I960-dh370
P=/home/nathan/Source/choptuik-large-d-raw-push960
cd $P || exit 9
mkdir -p I960-dh370 && cp -a $LIVE/. I960-dh370/
find I960-dh370 -type f -size +90M | head -1 | grep . && { echo "file over 90 MB"; exit 8; }
git add I960-dh370 && git commit -q -m "${1:-I960-dh370: progress}" || exit 7
for i in 1 2 3 4; do
  git pull -q --rebase origin main && python3 make_index.py && git add I960-dh370 INDEX.md && git commit -q --amend --no-edit && git push -q origin HEAD:main && break
  sleep 5
done
git fetch -q origin; echo "HEAD $(git rev-parse --short HEAD) origin/main $(git rev-parse --short origin/main)"
