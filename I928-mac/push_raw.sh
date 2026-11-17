#!/bin/bash
# #928: copies the working directory's scripts, logs and records into I928-mac of a temporary worktree of the raw
# repository, with local paths removed, and pushes. Usage: push_raw.sh "<commit message>"
set -e
J=$(cd "$(dirname "$0")" && pwd)
RAW=<raw clone>
W=<raw worktree>
cd "$RAW" && git fetch -q origin && git worktree add -q "$W" -b i928-mac origin/main
R=$W/I928-mac
mkdir -p "$R/out"
cp "$J"/*.sh "$J"/*.py "$R/"
cp "$J/README.md" "$R/README.md"
for f in "$J"/out/*.txt "$J"/out/*.json "$J"/out/*.jsonl "$J"/out/*.log "$J"/out/*.npz; do
    case "$f" in *_ckpt.npz) continue;; esac
    [ -e "$f" ] && cp "$f" "$R/out/"
done
fd -t f . "$R" -e txt -e log -e json -e jsonl -e sh -e py -e md -x gsed -i \
    -e 's###g' \
    -e 's###g' \
    -e 's###g' \
    -e 's#<working directory>#<working directory>#g' \
    -e 's#<site of #918>#<site of \#918>#g' \
    -e 's#python3#python3#g' \
    -e 's###g' \
    -e 's#<raw worktree>#<raw worktree>#g' \
    -e 's#<raw clone>#<raw clone>#g' {}
echo "files naming a home directory: $(grep -rl '/Users/' "$R" | wc -l | tr -d ' ')"
cd "$W" && python3 make_index.py | tail -1 && git add I928-mac INDEX.md && git commit -q -m "$1" && git pull -q --rebase origin main && git push -q origin HEAD:main && git log -1 --format='raw %h'
cd "$RAW" && git worktree remove "$W" && git branch -q -D i928-mac
