#!/bin/bash
# #1025 kc111_d2225: copy the live folder into the push worktree of the raw clone, commit, push to raw main; prints the commit. usage: bash push_k111.sh "<message>"
{
RAW=/home/nathan/Source/choptuik-large-d-raw-push960
LIVE=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc111_d2225
cd $RAW || exit 9
git pull --rebase origin main 2>&1 | tail -1
mkdir -p I1025-dh370/kc111_d2225
cp -ru $LIVE/. I1025-dh370/kc111_d2225/
python3 make_index.py 2>&1 | tail -1
git add I1025-dh370/kc111_d2225 INDEX.md
git commit -q -m "I1025-dh370/kc111_d2225: $1" || { echo "nothing to commit"; exit 0; }
git push origin HEAD:main 2>&1 | tail -1
git log --oneline | head -1 | cut -c1-8
exit 0
}
