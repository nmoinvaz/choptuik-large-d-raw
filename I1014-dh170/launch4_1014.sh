#!/bin/bash
# #1014: start stage 4 (series from T82-win's own M 320 state) when stage 3's exit line is in exits_1014.txt, never before (coordinator's hc 2026-11-20 ~01:05 UTC).
cd /home/nathan/Source/choptuik-large-d-raw/I1014-dh170 || exit 9
until grep -q "stage 3 exit" exits_1014.txt; do sleep 30; done
exec ./stage4_1014.sh
