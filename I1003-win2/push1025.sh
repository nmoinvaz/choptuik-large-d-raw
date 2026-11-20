#!/usr/bin/env bash
# Raw push of I1025-win2b (from the live clone D:/choptuik-large-d-raw, where no job writes now) through the SEPARATE worktree D:/choptuik-large-d-raw-743p (linear history, pull --rebase only).
# A new folder with a README was added, so INDEX.md is regenerated (make_index.py, as AGENTS.md says). Nothing in a job's clone is touched except read. usage: bash push1025.sh "commit message"
set -e
W=/d/choptuik-large-d-raw-743p
cd $W
git pull --rebase origin main 2>&1 | tail -n 1
mkdir -p $W/I1025-win2b
cp -r /d/choptuik-large-d-raw/I1025-win2b/. $W/I1025-win2b/
python make_index.py > /dev/null
git add I1025-win2b INDEX.md
git commit -q -m "$1" || { echo "nothing to commit"; exit 0; }
git pull --rebase origin main 2>&1 | tail -n 1
git push origin HEAD:main 2>&1 | tail -n 1
git log -1 --format='pushed %h'
