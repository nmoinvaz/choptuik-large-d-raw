#!/bin/bash
# #1025 kc87_leg: copy the live folder I1025-dh370/kc87_leg into the push worktree, commit, push to raw main; prints the commit.
# usage: bash push_i1080.sh "<message>"
{
RAW=/home/nathan/Source/choptuik-large-d-raw-push960
LIVE=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc87_leg
cd $RAW || exit 9
git pull --rebase origin main 2>&1 | tail -1
mkdir -p I1025-dh370/kc87_leg
cp -ru $LIVE/. I1025-dh370/kc87_leg/
python3 make_index.py 2>&1 | tail -1
git add I1025-dh370/kc87_leg INDEX.md
git commit -q -m "I1025-dh370/kc87_leg: $1" || { echo "nothing to commit"; exit 0; }
git push origin HEAD:main 2>&1 | tail -1
git log --oneline | head -1 | cut -c1-8
exit 0
}
