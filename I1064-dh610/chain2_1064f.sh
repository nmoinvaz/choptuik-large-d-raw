#!/bin/bash
# dry try 2 of run1064f.sh (rungs at --tol_od 1e-60, control at 2e-34), then unit i1064n only if both dry checks pass
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
date -u '+%F %T dry try 2 of run1064f.sh'
bash dry_1064f.sh > dry_1064f.out 2>&1
tail -3 dry_1064f.out
if grep -q 'DRY OK' dry_1064f.out; then bash start_1064_ho.sh; else date -u '+%F %T dry failed: unit i1064n not started'; fi
