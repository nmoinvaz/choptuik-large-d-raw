#!/bin/bash
# #1098 on win2 (Git Bash): two sparse worktrees of the raw clone R (/d/choptuik-large-d-raw by default), each with the
# top-level files, every folder's README.md (make_index.py reads them) and the folders named:
#   /d/choptuik-i1098-raw-live  I1098-win2/ and I1098-mac-a/tools/: where the runs write and read their tools; never
#                               pulled while a run writes there (a fetch is fine: it rewrites no file)
#   /d/choptuik-i1098-raw-push  I1098-win2/: push_ladder_win.sh copies the runs' folders in and pushes from here
# The clone itself is only fetched.
#
#     setup_wt.sh [R]
{
R=${1:-/d/choptuik-large-d-raw}
git -C $R fetch -q origin || exit 2
mk() {  # WT FOLDER...
  local wt=$1; shift
  [ -d $wt ] && { echo "$wt exists, kept"; return 0; }
  git -C $R worktree add -q --no-checkout --detach $wt origin/main || return 3
  local pat=("/*" "!/*/" "/*/README.md")
  for f in "$@"; do pat+=("/$f/"); done
  git -C $wt sparse-checkout set --no-cone "${pat[@]}" || return 4
  git -C $wt checkout -q --detach origin/main || return 5
  echo "$wt: $(git -C $wt log --oneline -1), $(ls $wt | wc -l) entries"
}
mk /d/choptuik-i1098-raw-live I1098-win2 I1098-mac-a/tools || exit $?
mk /d/choptuik-i1098-raw-push I1098-win2 || exit $?
mkdir -p /d/choptuik-i1098-raw-live/I1098-win2
ls /d/choptuik-i1098-raw-live/RAW_DATA_REPO /d/choptuik-i1098-raw-live/I1098-mac-a/tools/ladder_point2.sh || exit 6
exit
}
