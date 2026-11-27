#!/bin/bash
# (copy of push_1025.sh that adds I1102-win; push_1025.sh itself is unchanged) commit and push I1102-win linearly from the push worktree; usage: bash push_1025.sh "commit message"; stops at the first failing step
set -euo pipefail
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
python3 make_index.py > /dev/null
git add I1102-win INDEX.md
git commit -q -m "$1"
git pull --rebase -q origin main
python3 make_index.py > /dev/null
git add INDEX.md
git commit -q --amend --no-edit
git push -q origin HEAD:main
git rev-list --parents -n1 HEAD
git log -1 --format='%h %s' | cut -c1-120
