#!/bin/bash
# #1025: push the leap's states and record lines (both runs: tags l1kc63dh370 and l1kc63dh370b) to raw from the separate push worktree, and the live folder's files.
# usage: bash push_leap.sh "<what landed>"      prints the commit
{
RAW=/home/nathan/Source/choptuik-large-d-raw-push960
D=/home/nathan/Source/choptuik-large-d-1025/solver/matter/data
LIVE=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370
cd $RAW || exit 9
git pull --rebase origin main 2>&1 | tail -1
mkdir -p I1025-dh370/kc63_leap
cp -u $D/*l1kc63dh370* I1025-dh370/kc63_leap/
cp -u $LIVE/kc63_leap/leap.log $LIVE/kc63_leap/exits_leap.txt I1025-dh370/kc63_leap/ 2>/dev/null
for f in README.md read_d19.py scan_hyb.sh check_states.py push_leap.sh run1025cont.sh; do cp -u $LIVE/$f I1025-dh370/ 2>/dev/null; done
[ -d $LIVE/kc63_leap_cont ] && { mkdir -p I1025-dh370/kc63_leap_cont; cp -u $LIVE/kc63_leap_cont/* I1025-dh370/kc63_leap_cont/; }
[ -d $LIVE/hyb_D19.000000 ] && { mkdir -p I1025-dh370/hyb_D19.000000; cp -u $LIVE/hyb_D19.000000/* I1025-dh370/hyb_D19.000000/ 2>/dev/null; }
python3 make_index.py 2>&1 | tail -1
git add I1025-dh370 INDEX.md
git commit -q -m "I1025-dh370: $1" || { echo "nothing to commit"; exit 0; }
git push origin HEAD:main 2>&1 | tail -1
git log --oneline | head -1 | cut -c1-8
exit 0
}
