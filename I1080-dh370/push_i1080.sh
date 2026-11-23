#!/bin/bash
# #1080: copy the live folder I1080-dh370 into the push worktree, commit, push to raw main; prints the commit.
# usage: bash push_i1080.sh "<message>"
{
RAW=/home/nathan/Source/choptuik-large-d-raw-push960
LIVE=/home/nathan/Source/choptuik-large-d-raw-wt613/I1080-dh370
cd $RAW || exit 9
git pull --rebase origin main 2>&1 | tail -1
mkdir -p I1080-dh370
cp -ru $LIVE/. I1080-dh370/
python3 make_index.py 2>&1 | tail -1
git add I1080-dh370 INDEX.md
git commit -q -m "I1080-dh370: $1" || { echo "nothing to commit"; exit 0; }
git push origin HEAD:main 2>&1 | tail -1
git log --oneline | head -1 | cut -c1-8
exit 0
}
