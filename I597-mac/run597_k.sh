#!/bin/bash
# #597: smooth_k597.py (modecount_smooth's statistic at k-ulp steps) on the new build, 4 threads, nice 10.
source "$(dirname "$0")/env597.sh"
cd "$WT/hp" || exit 1
mkdir -p "$RAW/smooth_k"
run() {  # name state M kf re im ks
  new "$RAW/smooth_k597.py" "$2" "$3" "$4" "$5" "$6" "$7" > "$RAW/smooth_k/$1.log" 2>&1
  echo "smooth_k $1 exit $? at $(date -u +%FT%TZ)" >> "$RAW/exits.txt"
}
run D30_M48_phys "$STATES/modecount_state_D30.0688_M48.npz" 48 none 2.0797477 0 1,4,16,64,256,1024,4096
run D61_M64_s3 "$STATES/modecount_state_D61.0264_M64_kf23.npz" 64 23 0.132 2.912795 1,16,256,4096
run D30_M80_phys "$STATES/modecount_state_D30.0688_M80.npz" 80 none 2.0797477 0 1,16,256,4096
