#!/bin/bash
# Waits for the orphaned from101b_32x121 job at D 50.0075 (worker4's first, started 10:56 UTC) and then starts
# run_worker4.sh with rule 3b added.
HERE="$(cd "$(dirname "$0")" && pwd)"
while pgrep -f "tag from101b_32x121" >/dev/null; do sleep 10; done
touch "$HERE/fol/done_from101b_32x121_D50.0075"
exec "$HERE/run_worker4.sh"
