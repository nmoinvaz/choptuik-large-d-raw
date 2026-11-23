#!/bin/bash
# copies this run's outputs from the worktree (solver/proof: data/A_M_*_M3x?E2*, A_M_6a_*, logs/, lemmas_M_runs/, lemma6b1_runs_M3_exc?_linux/) into out/ (a copy, tracked files untouched) and pushes the folder
W=/home/nathan/Source/choptuik-large-d-1079a/solver/proof; F=/home/nathan/Source/choptuik-large-d-raw/I1079-dh610; PUSH=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/push_folder.sh
mkdir -p $F/out/data $F/out/logs $F/out/lemmas_M_runs
rsync -a $W/data/ $F/out/data/ --include='A_M_*M3x?E2*' --include='A_M_6a_*' --exclude='*'
rsync -a $W/logs/ $F/out/logs/ --include='*M3x?E2*' --include='I1079_*' --include='XL_*' --exclude='*'
rsync -a $W/lemmas_M_runs/ $F/out/lemmas_M_runs/
for d in $W/lemma6b1_runs_M3_exc?_linux; do [ -d $d ] && rsync -a $d $F/out/; done
bash $PUSH I1079-dh610 "${1:-I1079-dh610: progress}"
