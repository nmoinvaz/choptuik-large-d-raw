#!/bin/bash
# #1110 (mm5): wait for dh170's chord state and its map on origin/main of the raw repository (git fetch every 10 min, 4 h at most),
# then copy both into in/ and print their blobs. Exit 0 when both are there, 1 on the time-out.
{
R=$HOME/Source/choptuik-large-d-raw
OUT=$R/I1110-mm5/in
P=I1110-dh170/sol_chord035_D23.0000
t0=$(date +%s)
while true; do
  git -C $R fetch -q origin 2>/dev/null
  if git -C $R cat-file -e origin/main:$P.npy 2>/dev/null && git -C $R cat-file -e origin/main:$P.map.json 2>/dev/null; then
    git -C $R show origin/main:$P.npy > $OUT/sol_chord035_D23.0000.npy
    git -C $R show origin/main:$P.map.json > $OUT/sol_chord035_D23.0000.map.json
    echo "both files found $(date -u '+%Y-%m-%d %H:%M:%S UTC'); origin/main $(git -C $R rev-parse --short origin/main)"
    git hash-object --no-filters $OUT/sol_chord035_D23.0000.npy $OUT/sol_chord035_D23.0000.map.json
    git -C $R rev-parse origin/main:$P.npy origin/main:$P.map.json
    exit 0
  fi
  if [ $(( $(date +%s) - t0 )) -ge 14400 ]; then echo "time-out after 4 h $(date -u '+%Y-%m-%d %H:%M:%S UTC'): the files are not on origin/main"; exit 1; fi
  sleep 600
done
}
