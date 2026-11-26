#!/bin/bash
# #1098: copies each run folder SRC into the raw worktree ~/Source/choptuik-large-d-raw-1088a at REL and pushes it, at
# once and then whenever a folder's run.log or its set of state files changes (a stage's end), every 2 min, until UNIT
# ends, then once more; each push's commit is logged to ~/Source/choptuik-large-d-1088a/out/ladder/push.log
#
#     push_ladder.sh UNIT SRC:REL [SRC:REL ...]
{
UNIT=$1; shift
WT=$HOME/Source/choptuik-large-d-raw-1088a
LOG=$HOME/Source/choptuik-large-d-1088a/out/ladder/push.log
[ -d $WT/.git ] || [ -f $WT/.git ] || exit 1
sig() {
  for p in "$@"; do
    s=${p%%:*}
    [ -d $s ] || continue
    { cat $s/run.log 2>/dev/null; ls -R $s | grep -E "\.npz$" | grep -v _step; } | md5sum
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
  python3 make_index.py > /dev/null
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
last=""
while true; do
  act=0
  systemctl --user is-active --quiet $UNIT && act=1
  cur=$(sig "$@")
  if [ "$cur" != "$last" ] || [ $act = 0 ]; then
    l=""
    for p in "$@"; do s=${p%%:*}; [ -s $s/run.log ] && l="$l $(basename $s): $(tail -1 $s/run.log | cut -c1-60);"; done
    r0=${1#*:}
    MSG="${r0%%/*}: ladder states and logs,$l"
    push "$@"
    last=$cur
  fi
  [ $act = 0 ] && break
  sleep 120
done
exit
}
