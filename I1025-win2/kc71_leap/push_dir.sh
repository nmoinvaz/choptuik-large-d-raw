#!/usr/bin/env bash
# Raw push of one folder of I1025-win2 (usage: bash push_dir.sh DIRNAME "commit message", e.g. kc79_d20) from the live clone D:/choptuik-i935-raw through the clean worktree D:/choptuik-large-d-raw-743p (linear history, pull --rebase only).
# Files deleted in the live folder are deleted in the worktree too. INDEX.md is not regenerated (this folder is indexed; make_index.py exits 1 while another agent's folder lacks its README title line).
set -e
[ -n "$1" ] && [ -n "$2" ] || { echo "usage: push_dir.sh DIRNAME MESSAGE"; exit 2; }
W=/d/choptuik-large-d-raw-743p
S=/d/choptuik-i935-raw/I1025-win2/$1
cd $W
git pull --rebase origin main 2>&1 | tail -n 1
mkdir -p $W/I1025-win2/$1
cp -r $S/. $W/I1025-win2/$1/
find $W/I1025-win2/$1 -name __pycache__ -type d -prune -exec rm -r {} + 2>/dev/null || true
# remove from the worktree what the live folder no longer has (the files under the folder only)
( cd $W/I1025-win2/$1 && git ls-files . | while read -r f; do [ -e "$S/$f" ] || git rm -q -f "$f"; done )
git add I1025-win2/$1
git commit -q -m "$2" || { echo "nothing to commit"; exit 0; }
git pull --rebase origin main 2>&1 | tail -n 1
git push origin HEAD:main 2>&1 | tail -n 1
git log -1 --format='pushed %h'
git rev-list --left-right --count HEAD...origin/main
