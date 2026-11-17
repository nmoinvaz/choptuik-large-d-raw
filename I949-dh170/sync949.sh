#!/bin/bash
# #949: copy win2b's order-tied chain states from origin/main of the raw repository into the scratch root ~/scratch949
# (the root near_null.py reads, same paths), byte for byte from the committed blobs, without touching any worktree.
# usage: sync949.sh      prints one line per new state ("new PATH") and "synced COMMIT N states" at the end
G=/home/nathan/Source/choptuik-large-d-raw-push
S=/home/nathan/scratch949
git -C $G fetch -q origin || exit 9
C=$(git -C $G rev-parse --short origin/main)
n=0
for p in $(git -C $G ls-tree -r --name-only origin/main I903-win2/ks_chain/ | grep -E '/anm_pin3_D[0-9.]+\.npz$'); do
  n=$((n+1))
  [ -f "$S/$p" ] && continue
  mkdir -p "$S/$(dirname $p)"
  git -C $G cat-file blob "origin/main:$p" > "$S/$p.part" && mv "$S/$p.part" "$S/$p" && echo "new $p"
done
echo "synced $C $n states"
