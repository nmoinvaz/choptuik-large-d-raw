#!/bin/bash
# #597: the frozen rows' difference, old build against new, at two kfreeze states (mm597.py dump and compare), 4 threads.
source "$(dirname "$0")/env597.sh"
cd "$WT/hp" || exit 1
mkdir -p "$RAW/kf" "$SP/i597/dumps"
dump() {  # build name state M kf lams...
  local b=$1 n=$2
  shift 2
  $b "$RAW/mm597.py" dump "$SP/i597/dumps/${b}_$n.npz" "$@" > "$RAW/kf/${b}_$n.log" 2>&1
  echo "dump ${b}_$n exit $? at $(date -u +%FT%TZ)" >> "$RAW/exits.txt"
}
cmp_() {
  "$PY" "$RAW/mm597.py" compare "$SP/i597/dumps/old_$1.npz" "$SP/i597/dumps/new_$1.npz" --rows=HORIZON_P > "$RAW/kf/compare_$1.log" 2>&1
  echo "compare $1 exit $? at $(date -u +%FT%TZ)" >> "$RAW/exits.txt"
}
for b in new old; do dump $b D40_M32_kf13 data/states/up7_D40.0201.npz 32 13 1.7,0 2.0627797,0 0.5,1.6 3.0,2.5; done
cmp_ D40_M32_kf13
for b in new old; do dump $b D61_M64_kf23 "$STATES/modecount_state_D61.0264_M64_kf23.npz" 64 23 0.132,2.912795 1.98,0.749808; done
cmp_ D61_M64_kf23
# the no-cut control of the comparison: old against new at D 30 M 32 must give 0 differing entries (and its exit 0)
for b in new old; do dump $b D30_M32_nocut data/states/up6_D30.0688.npz 32 none 2.0797477,0 0.055758,1.411769; done
"$PY" "$RAW/mm597.py" compare "$SP/i597/dumps/old_D30_M32_nocut.npz" "$SP/i597/dumps/new_D30_M32_nocut.npz" > "$RAW/kf/compare_D30_M32_nocut.log" 2>&1
echo "compare D30_M32_nocut exit $? at $(date -u +%FT%TZ)" >> "$RAW/exits.txt"
