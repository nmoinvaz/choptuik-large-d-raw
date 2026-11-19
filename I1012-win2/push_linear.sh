#!/bin/bash
# Linear push of task folders to choptuik-large-d-raw main, from the dedicated push worktree (never from a folder a live job writes to).
#   bash push_linear.sh "commit message" FOLDER [FOLDER ...]       folders are names under D:/choptuik-i935-raw (the live worktree)
# Steps: copy each folder into the push worktree (files only, nothing removed), regenerate INDEX.md there, commit, `git pull --rebase origin main`
# (on an INDEX.md conflict: python3 make_index.py && git add INDEX.md && git rebase --continue), push HEAD:main, print the commit and its parent count.
# No merge commits, no git merge-tree (the coordinator's rule, 2026-11-19).
set -e
LIVE=/d/choptuik-i935-raw
PUSH=/d/choptuik-large-d-raw-push
MSG="$1"; shift
[ -n "$MSG" ] && [ "$#" -ge 1 ] || { echo "usage: push_linear.sh MESSAGE FOLDER..."; exit 2; }
cd "$PUSH"
[ -z "$(git status --short)" ] || { echo "the push worktree is not clean:"; git status --short | head; exit 3; }
git fetch origin main -q
git merge-base --is-ancestor HEAD origin/main || { echo "the push worktree has commits that are not on origin/main"; exit 4; }
git pull --rebase origin main -q
for f in "$@"; do
  [ -d "$LIVE/$f" ] || { echo "no folder $LIVE/$f"; exit 5; }
  mkdir -p "$PUSH/$f"
  cp -r "$LIVE/$f/." "$PUSH/$f/"
done
python3 make_index.py | tail -1
git add "$@" INDEX.md
git commit -q -m "$MSG"
if ! git pull --rebase origin main -q 2>/dev/null; then
  if git diff --name-only --diff-filter=U | grep -q '^INDEX.md$'; then
    python3 make_index.py | tail -1; git add INDEX.md; GIT_EDITOR=true git rebase --continue
  else
    echo "rebase conflict outside INDEX.md:"; git status --short | head; exit 6
  fi
fi
git push origin HEAD:main 2>&1 | tail -2
echo "pushed commit $(git rev-parse HEAD), parents: $(git log -1 --format=%p)"
[ "$(git rev-list --parents -1 HEAD | wc -w)" = "2" ] && echo "linear: one parent" || echo "WARNING: more than one parent"
