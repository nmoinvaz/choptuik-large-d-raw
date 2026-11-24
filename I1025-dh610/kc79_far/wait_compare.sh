#!/bin/bash
# wait_compare.sh D: for a D that win2's tag g leap and tag i far scout both reach: waits (polling origin every 60 s, cap 12 h) for both states, pins each by blob (fetch_point.sh with TAG=g and TAG=i into D<D>/g/in and D<D>/i/in),
# pushes the pins, then runs lane_compare.sh (no scan: the coordinator's order of 24 Nov).
D=$1; FAR=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_far; F=$FAR/D$D; L=$F/exits_far.txt
PUSH=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/push_folder.sh
mkdir -p $F
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc79_far D $D: $*" | tee -a $L; }
t0=$(date +%s); rg=1; ri=1
while [ $rg != 0 ] || [ $ri != 0 ]; do
  [ $rg = 0 ] || { TAG=l1kc79Lw1025g bash $FAR/fetch_point.sh $D $F/g/in > $F/fetch_g.log 2>&1; rg=$?; }
  [ $ri = 0 ] || { TAG=l1kc79Lw1025i bash $FAR/fetch_point.sh $D $F/i/in > $F/fetch_i.log 2>&1; ri=$?; }
  [ $rg = 0 ] || [ $rg = 1 ] || { say "STOP: fetch_point.sh (tag g) exit $rg: $(tail -n 2 $F/fetch_g.log)"; exit 1; }
  [ $ri = 0 ] || [ $ri = 1 ] || { say "STOP: fetch_point.sh (tag i) exit $ri: $(tail -n 2 $F/fetch_i.log)"; exit 1; }
  [ $rg = 0 ] && [ $ri = 0 ] && break
  [ $(( $(date +%s) - t0 )) -lt 43200 ] || { say "STOP: not both states of D $D are on origin after 12 h (tag g exit $rg, tag i exit $ri)"; exit 1; }
  sleep 60
done
say "both states pinned: tag g: $(cat $F/fetch_g.log); tag i: $(cat $F/fetch_i.log)"
bash $PUSH I1025-dh610/kc79_far/D$D "I1025-dh610/kc79_far/D$D: pins of the g and i states" > $F/push_pins.txt 2>&1
bash $FAR/lane_compare.sh $D
