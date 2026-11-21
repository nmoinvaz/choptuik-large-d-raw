#!/bin/bash
# #1014: start step B (run1014b.py) when step C's exit line is in exits_1014.txt, never before (coordinator: C then B, hc 2026-11-20 about 05:31 UTC).
cd /home/nathan/Source/choptuik-large-d-raw/I1014-dh170 || exit 9
until grep -q "stage 5 exit" exits_1014.txt; do sleep 30; done
exec /home/nathan/Source/choptuik-large-d-935/.venv/bin/python -u run1014b.py >> run1014b.out 2>&1
