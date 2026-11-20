#!/bin/bash
# #1014: start stage 3 (M 384 series) as soon as stage 2's exit line is in exits_1014.txt (the 30-minute rule on its target stage), never before.
cd /home/nathan/Source/choptuik-large-d-raw/I1014-dh170 || exit 9
until grep -q "stage 2 exit" exits_1014.txt; do sleep 10; done
exec ./stage3_1014.sh
