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
# a rejected push (someone pushed in between) is retried after a rebase, up to 4 times; 'pushed' is printed only when origin/main holds the commit
ok=0
for try in 1 2 3 4; do
  git pull --rebase origin main 2>&1 | tail -n 1
  if git push origin HEAD:main > /dev/null 2>&1; then ok=1; break; fi
  sleep 3
done
git fetch -q origin
if [ $ok = 1 ] && [ "$(git rev-list --left-right --count HEAD...origin/main | cut -f1)" = 0 ]; then git log -1 --format='pushed %h'; else echo 'PUSH FAILED'; exit 1; fi
git rev-list --left-right --count HEAD...origin/main
