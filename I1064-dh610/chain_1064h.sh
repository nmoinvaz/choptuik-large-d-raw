#!/bin/bash
# dry tests of run1064h.sh, then unit i1064p only if both dry checks pass
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
date -u '+%F %T dry runs of run1064h.sh'
bash dry_1064h.sh > dry_1064h.out 2>&1
tail -3 dry_1064h.out
if grep -q 'DRY OK' dry_1064h.out; then bash start_1064_ho3.sh; else date -u '+%F %T dry failed: unit i1064p not started'; fi
