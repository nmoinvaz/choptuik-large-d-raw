#!/usr/bin/env bash
# Raw push of I1025-win2/kc71_leap from the live clone D:/choptuik-i935-raw (where jobs write) through the separate clean worktree D:/choptuik-large-d-raw-743p (linear history, pull --rebase only).
# The live clone is only read. usage: bash push_raw.sh "commit message"
set -e
W=/d/choptuik-large-d-raw-743p
S=/d/choptuik-i935-raw/I1025-win2/kc71_leap
cd $W
git pull --rebase origin main 2>&1 | tail -n 1
mkdir -p $W/I1025-win2/kc71_leap
cp -r $S/. $W/I1025-win2/kc71_leap/
find $W/I1025-win2/kc71_leap -name __pycache__ -type d -prune -exec rm -r {} + 2>/dev/null || true
# INDEX.md is not regenerated: this folder is already indexed, and make_index.py exits 1 while another agent's folder lacks its README title line
git add I1025-win2/kc71_leap
git commit -q -m "$1" || { echo "nothing to commit"; exit 0; }
git pull --rebase origin main 2>&1 | tail -n 1
git push origin HEAD:main 2>&1 | tail -n 1
git log -1 --format='pushed %h'
git rev-list --left-right --count HEAD...origin/main
