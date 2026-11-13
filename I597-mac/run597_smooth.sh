#!/bin/bash
# #597: hp/modecount_smooth.py --joint on the new build (engine mode matrix) and the old (main 3c35f0c's modecount_cx),
# one process at a time (the script fixes 4 threads), nice 10, from hp/ of the worktree. States: #609's (I609-macm3
# states/, sha256 in its state_sha256.txt) and #445's D 61 M 64 kf 23 (I252-mac), given by path so setup loads them as is.
source "$(dirname "$0")/env597.sh"
cd "$WT/hp" || exit 1
mkdir -p "$RAW/smooth"
D30=data/states/up6_D30.0688.npz
PHYS=2.0797477,0
P1=0.055758,1.411769
S3=0.132000,2.912795
run() {  # build name state M kf re,im [extra]
  local b=$1 n=$2
  $b modecount_smooth.py "$3" "$4" "$5" "${6%,*}" "${6#*,}" --joint $7 > "$RAW/smooth/${b}_$n.log" 2>&1
  echo "${b}_$n exit $? at $(date -u +%FT%TZ)" >> "$RAW/exits.txt"
}
for b in new old; do run $b ctrl_D30_M32_phys $D30 32 none $PHYS; done
run new mutate_lo_D30_M32_phys $D30 32 none $PHYS --mutate=lo
for c in "D30_M40_phys $STATES/modecount_state_D30.0688_M40.npz 40 none $PHYS" \
         "D30_M48_phys $STATES/modecount_state_D30.0688_M48.npz 48 none $PHYS" \
         "D30_M64_phys $STATES/modecount_state_D30.0688_M64.npz 64 none $PHYS" \
         "D30_M80_phys $STATES/modecount_state_D30.0688_M80.npz 80 none $PHYS" \
         "D61_M64_s3 $STATES/modecount_state_D61.0264_M64_kf23.npz 64 23 $S3" \
         "D30_M64_pos1 $STATES/modecount_state_D30.0688_M64.npz 64 none $P1" \
         "D30_M80_pos1 $STATES/modecount_state_D30.0688_M80.npz 80 none $P1"; do
  set -- $c
  for b in new old; do run $b "$@"; done
done
echo "chain done at $(date -u +%FT%TZ)" >> "$RAW/exits.txt"
