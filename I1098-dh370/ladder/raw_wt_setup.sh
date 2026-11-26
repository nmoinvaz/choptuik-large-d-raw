#!/bin/bash
# a sparse worktree of this machine's raw clone for #1098's pushes (~/Source/choptuik-large-d-raw-1088a): the top-level
# files, every folder's README.md (make_index.py reads them) and the folder FOLDER; the clone itself is only fetched
{
FOLDER=$1
R=$HOME/Source/choptuik-large-d-raw
WT=$HOME/Source/choptuik-large-d-raw-1088a
[ -n "$FOLDER" ] || exit 1
if [ ! -d $WT ]; then
  git -C $R fetch -q origin || exit 2
  git -C $R worktree add -q --no-checkout --detach $WT origin/main || exit 3
  git -C $WT sparse-checkout set --no-cone '/*' '!/*/' '/*/README.md' "/$FOLDER/" || exit 4
  git -C $WT checkout -q --detach origin/main || exit 5
fi
git -C $WT log --oneline -1
ls $WT | wc -l
ls $WT/$FOLDER
exit
}
