#!/bin/bash
# #949: copy win2b's order-tied chain states from origin/main of the raw repository into the scratch root ~/scratch949
# (the root near_null.py reads, same paths), byte for byte from the committed blobs, without touching any worktree.
# Copies dh370's ks_chain3 states (I966-dh370, from 2026-11-18, coordinator's note) as well as the chain's states (ks_chain, and ks_chain2 once win2b has pushed it) and the ks ladder's bases (ks_chain/ladder8/ks*/base_pin*.npz).
# usage: sync949.sh      prints one line per new state ("new PATH") and "synced COMMIT N states" at the end
G=/home/nathan/Source/choptuik-large-d-raw-push
S=/home/nathan/scratch949
git -C $G fetch -q origin || exit 9
C=$(git -C $G rev-parse --short origin/main)
n=0
for p in $(git -C $G ls-tree -r --name-only origin/main I903-win2/ks_chain/ I903-win2/ks_chain2/ I966-dh370/ks_chain3/ I966-dh370/ks_chain3b/ | grep -E '/(anm_pin3|base_pin[0-9]+)_D[0-9.]+\.npz$'); do
  n=$((n+1))
  [ -f "$S/$p" ] && continue
  mkdir -p "$S/$(dirname $p)"
  git -C $G cat-file blob "origin/main:$p" > "$S/$p.part" && mv "$S/$p.part" "$S/$p" && echo "new $p"
done
echo "synced $C $n states"
