#!/bin/bash
# #903 grip: next.sh DIR DMIN prints the path of DIR's first stored base anm_pin3_D<D>.npz with D >= DMIN on
# choptuik-large-d-raw's origin/main, fetching every 10 min until one lands (git fetch and ls-tree in the push worktree).
P=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw828push
dir=$1; dmin=$2
while :; do
  git -C "$P" fetch -q origin
  f=$(git -C "$P" ls-tree --name-only origin/main "$dir/" | grep -E '/anm_pin3_D[0-9.]+\.npz$' |
      awk -v m="$dmin" '{d=$0; sub(/.*_D/, "", d); sub(/\.npz$/, "", d); if (d + 0 >= m + 0) print d, $0}' |
      sort -n | head -1 | cut -d' ' -f2)
  [ -n "$f" ] && { echo "$f"; exit 0; }
  sleep 600
done
