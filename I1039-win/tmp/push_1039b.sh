#!/bin/bash
# push I1039-win's README fix linearly from the push worktree; stops at the first failing step
set -euo pipefail
RAW=/c/Users/nathan/Source/choptuik-large-d-raw
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
git fetch -q origin
git checkout -q --detach origin/main
cp "$RAW/I1039-win/README.md" I1039-win/README.md
cp -r "$RAW/I1039-win/tmp/." I1039-win/tmp/
python3 make_index.py > /dev/null
git add I1039-win INDEX.md
git commit -q -m "I1039-win: README line-ending note corrected (the six route3_bound logs are byte-identical to I1030-rpi5's as stored in git)"
git pull --rebase -q origin main
python3 make_index.py > /dev/null
git add INDEX.md
git commit -q --amend --no-edit
git push -q origin HEAD:main
git rev-list --parents -n1 HEAD
git log -2 --format='%h %s' | cut -c1-110
