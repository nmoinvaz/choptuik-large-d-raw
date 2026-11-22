#!/bin/bash
# #997 Delta series at D 3.04315 (dh610): preflight, then run997c.py (the command diffed, the pilot stop rule, the sampler)
cd ~/Source/choptuik-large-d-raw/I997-dh610/series_D304315 || exit 9
RAW=/home/nathan/Source/choptuik-large-d-raw; WT=/home/nathan/Source/choptuik-large-d-997c
[ "$(git -C $WT rev-parse HEAD)" = ab0ddb8c7cea4ac057fb7024bd27921d5343a00f ] && [ -z "$(git -C $WT status --short)" ] || { echo "997c worktree not a clean ab0ddb8c: stop $(date -u '+%F %T') UTC" >> exits_997c.txt; exit 1; }
[ "$(git -C $RAW hash-object --no-filters $RAW/I945-win2/leg/states/lowD343_D3.043150_M320.npz)" = c23b9cb371e959f77d02d3d78785927500a24373 ] || { echo "997c the state's blob is not c23b9cb3: stop $(date -u '+%F %T') UTC" >> exits_997c.txt; exit 1; }
exec /home/nathan/Source/venv-i1058/bin/python -u run997c.py
