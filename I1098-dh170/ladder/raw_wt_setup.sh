#!/bin/bash
# a sparse worktree of this machine's raw clone for #1098 (WT, ~/Source/choptuik-large-d-raw-1088a by default): the
# top-level files, every folder's README.md (make_index.py reads them) and the folder FOLDER; the clone itself is only
# fetched. One worktree takes the pushes (push_ladder.sh); a second (WT ...-live) is where runs write, never pulled
# while they run
#
#     raw_wt_setup.sh FOLDER [WT]
{
FOLDER=$1
R=$HOME/Source/choptuik-large-d-raw
WT=${2:-$HOME/Source/choptuik-large-d-raw-1088a}
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
