#!/bin/bash
# #903 grip: drive.sh runs one base and exits: the first pending target of targets.txt ("TAG DIR DMIN", not in done.txt)
# whose chain has a stored base with D >= DMIN on choptuik-large-d-raw's origin/main (fetched every 10 min), at its own
# order and ks 200 (state.sh), then appends it to done.txt. Pending targets are tried in the file's order.
O=$(cd "$(dirname "$0")" && pwd)
P=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw828push
while :; do
  git -C "$P" fetch -q origin
  while read -r tag dir dmin; do
    grep -q "^$tag $dir $dmin " "$O/done.txt" && continue
    f=$(git -C "$P" ls-tree --name-only origin/main "$dir/" | grep -E '/anm_pin3_D[0-9.]+\.npz$' |
        awk -v m="$dmin" '{d=$0; sub(/.*_D/, "", d); sub(/\.npz$/, "", d); if (d + 0 >= m + 0) print d, $0}' |
        sort -n | head -1 | cut -d' ' -f2)
    if [ -n "$f" ]; then
      echo "target $tag $dmin: $f $(date -u '+%H:%M')"
      "$O/state.sh" "$tag" "$f" 200
      echo "$tag $dir $dmin $f" >> "$O/done.txt"
      exit 0
    fi
  done < "$O/targets.txt"
  sleep 600
done
