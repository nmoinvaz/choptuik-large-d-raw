#!/bin/bash
# #1098 on win2 (Git Bash): copies each run folder SRC (in the live raw worktree) into the push worktree
# /d/choptuik-i1098-raw-push at REL and pushes it, at once and then whenever a folder's run.log, exit_codes.txt or its
# set of state files changes (a stage's end), every 2 min, until the file DONE exists (the job's last act) or CAP_H
# hours pass, then once more; each push's commit is logged to /d/choptuik-i1098-logs/i1098_push.log.
# Linux's push_ladder.sh watches systemd units; this one watches a marker file. SRC is written in Git Bash's form
# (/d/...): the colon of D:/ would split SRC:REL.
#
#     PY=/c/Users/nathan/Source/venv-i1098/Scripts/python.exe push_ladder_win.sh CAP_H DONE SRC:REL [SRC:REL ...]
{
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
CAP=$1; DONE=$2; shift 2
WT=/d/choptuik-i1098-raw-push
LOG=/d/choptuik-i1098-logs/i1098_push.log
mkdir -p /d/choptuik-i1098-logs
PY=${PY:-/c/Users/nathan/Source/venv-i1098/Scripts/python.exe}
[ -e $WT/.git ] || exit 1
sig() {
  for p in "$@"; do
    s=${p%%:*}
    [ -d $s ] || continue
    { cat $s/run.log $s/exit_codes.txt 2>/dev/null; ls -R $s | grep -E "\.npz$" | grep -v _step; } | md5sum
  done | md5sum
}
push() {
  for p in "$@"; do
    s=${p%%:*}; r=${p#*:}
    [ -d $s ] || continue
    mkdir -p $WT/$r
    cp -a $s/. $WT/$r/
  done
  cd $WT || return 1
  $PY make_index.py > /dev/null
  git add INDEX.md
  for p in "$@"; do r=${p#*:}; [ -d $r ] && git add $r; done
  if git diff --cached --quiet; then return 0; fi
  git commit -qm "$MSG"
  for i in 1 2 3 4 5; do
    git pull -q --rebase origin main && git push -q origin HEAD:main && break
    sleep 60
  done
  echo "$(date -u +%H:%M:%S) $(git rev-parse --short=9 HEAD) $MSG" >> $LOG
}
t0=$(date +%s)
last=""
while true; do
  fin=0
  [ -e "$DONE" ] && fin=1
  [ $(( $(date +%s) - t0 )) -ge $(( CAP * 3600 )) ] && fin=1
  cur=$(sig "$@")
  if [ "$cur" != "$last" ] || [ $fin = 1 ]; then
    l=""
    for p in "$@"; do s=${p%%:*}; [ -s $s/run.log ] && l="$l $(basename $s): $(tail -1 $s/run.log | cut -c1-60);"; done
    r0=${1#*:}
    MSG="${r0%%/*}: states and logs,$l"
    push "$@"
    last=$cur
  fi
  [ $fin = 1 ] && break
  sleep 120
done
exit
}
