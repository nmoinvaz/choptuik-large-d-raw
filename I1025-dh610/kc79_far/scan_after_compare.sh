#!/bin/bash
# scan_after_compare.sh D CENTER PRED [dry|check]: the coordinator's order of 24 Nov (hc, after the first comparison): at the shared D 21.34375 the tag i state is scanned too, after the side-by-side comparison, with the
# window and the rule of tag g's scan there (CENTER the multiple of 0.005 nearest PRED = tag g's prediction, grid +-0.015 by 0.005 plus a repeat, widen once by 0.015, bar 0.01). Waits (cap CAP s, default 43200) for the
# comparison of D to end (its line "states compared ... far point done" in D<D>/exits_far.txt, or CMPFILE); a STOP or refuse line there, or no end line within the cap, stops this script with nothing scanned. Then the thread
# gate of wait_and_run.sh (budget.txt), the far lock, and lane_far.sh with FARDIR=D<D>/i (default; the env FARDIR is for the tests): the state is the one the comparison pinned (i/in, blobs in i/in_blobs.txt), the outputs are in
# D<D>/i/ (exits_far.txt, scan/, src/, read_lower.txt, leg_read.txt).
D=$1; C=$2; PRED=$3; MODE=${4:-}
FAR=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_far; F=$FAR/D$D; I=${FARDIR:-$F/i}; CMP=${CMPFILE:-$F/exits_far.txt}; L=$I/exits_far.txt; CAP=${CAP:-43200}
mkdir -p $I
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc79_far D $D (tag i scan): $*" | tee -a $L; }
t0=$(date +%s)
while :; do
  grep -q -E "kc79_far D $D: (STOP: |refuse: )" $CMP 2>/dev/null && { say "STOP: the comparison of D $D stopped or refused (see $CMP); the scan of the tag i state does not start"; exit 1; }
  grep -q -E "kc79_far D $D: states compared.*far point done" $CMP 2>/dev/null && break
  [ $(( $(date +%s) - t0 )) -lt $CAP ] || { say "STOP: the comparison of D $D did not end within $CAP s; nothing scanned"; exit 1; }
  sleep 20
done
say "the comparison of D $D is done: the scan of the tag i state follows (window around $C, prediction $PRED)"
tw=$(date +%s)
while :; do
  LIM=$(cat $FAR/budget.txt 2>/dev/null || echo 20); used=0
  [ "$(systemctl --user is-active i1076d)" = active ] && used=$((used + 12))
  ( flock -n 7 ) 7> /tmp/claude-1000/kc79_leg.lock || used=$((used + 8))
  [ $((used + 8)) -le $LIM ] && break
  [ -e $I/budget_wait.txt ] || say "waiting for threads: $used planned in use (recount 12 if active, tag g lane 8 if running) + 8 > $LIM"
  echo "$(date -u '+%F %T') UTC $used in use, limit $LIM" > $I/budget_wait.txt
  sleep 60
done
say "threads: $used planned in use + 8 <= $LIM (budget.txt), waited $(( $(date +%s) - tw )) s"
exec 8> /tmp/claude-1000/kc79_far.lock
flock 8
say "lock taken, lane starts"
FARDIR=$I bash $FAR/lane_far.sh $D $C $PRED $MODE
