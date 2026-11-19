#!/usr/bin/env bash
# Raw push of I945-win2 (from the live clone) and I1003-win2 (from the K 49 job's folder in the raw-743 worktree) through a SEPARATE worktree, D:/choptuik-large-d-raw-743p, as the coordinator ordered
# (hc of 2026-11-19 ~11:00 UTC: never pull, rebase or reset a clone a job writes into; linear history, pull --rebase only). Nothing in raw-743 or in the live clone is touched except read.
# Folders are copied with cp -r (no -u: the worktree's files are newer than the sources). INDEX.md is not regenerated (no folder or README is added). usage: bash push743.sh "commit message"
set -e
W=/d/choptuik-large-d-raw-743p
cd $W
git pull --rebase origin main 2>&1 | tail -n 1
cp -r /d/choptuik-large-d-raw/I945-win2/. $W/I945-win2/
cp -r /d/choptuik-large-d-raw-743/I1003-win2/. $W/I1003-win2/
git add I945-win2 I1003-win2
git commit -q -m "$1" || { echo "nothing to commit"; exit 0; }
git pull --rebase origin main 2>&1 | tail -n 1
git push origin HEAD:main 2>&1 | tail -n 1
git log -1 --format='pushed %h'
