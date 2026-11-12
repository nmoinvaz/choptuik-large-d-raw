#!/bin/bash
# I612: hp/modecount_smooth.py --joint (part 1) and D 30 between M 48 and M 80, and the other #473 positions (part 2).
# Usage: run_612.sh 1|2 (two chains, one process each, nice 10). Worktree ~/Source/choptuik-large-d-b596 at main ef466c7
# (modecount_cx built from 742bb879's source).
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
out=$raw/I612-macm3
cd /Users/nathan/Source/choptuik-large-d-b596/hp
D30=data/states/up6_D30.0688.npz
S64=$raw/I252-mac/states/modecount_state_D61.0264_M64_kf23.npz
PHYS=2.0797477,0
P1=0.055758,1.411769   # #473's eight upper-half positions, in #607's order
P2=3.871717,0.105316
P3=4.285793,0.551490
P4=4.656327,1.390362
P5=0.847147,4.333559
P6=1.057045,2.913917
P7=1.978326,3.721021
P8=4.070967,2.532063
S3=0.132000,2.912795
run() {  # name state M kf re,im
  caffeinate -is nice -n 10 python3 -u modecount_smooth.py $2 $3 $4 ${5%,*} ${5#*,} --joint > $out/$1.log 2>&1
  echo "$1 exit $? at $(date -u +%FT%TZ)" >> $out/exits.txt
}
gate() {  # the control: the one entry at block (0, 0), row 8, column 29, field p; at most 1% of the changed entries
  grep -q "^  entries with .*: 1$" $out/ctrl_M32_phys.log && grep -q "largest: row 8, col 29:" $out/ctrl_M32_phys.log &&
  grep -q "rows by field (p, m, a, c): \[1 0 0 0\]" $out/ctrl_M32_phys.log && awk '/counts, 1 in all/ {getline; if ($1 == 1) ok = 1} END {exit !ok}' $out/ctrl_M32_phys.log
}
if [ "$1" = 1 ]; then
  run ctrl_M32_phys $D30 32 none $PHYS
  if gate; then echo "control passes at $(date -u +%FT%TZ)" >> $out/exits.txt
  else echo "CONTROL FAILED at $(date -u +%FT%TZ)" >> $out/exits.txt; exit 1; fi
  run P1_D61_M64_s3 $S64 64 23 $S3
  run P1_D30_M80_phys $D30 80 none $PHYS
  run P2_M56_phys $D30 56 none $PHYS
  run P2_M56_pos1 $D30 56 none $P1
  run P2_M72_phys $D30 72 none $PHYS
  run P2_M72_pos1 $D30 72 none $P1
else
  while ! grep -q '^control passes\|^CONTROL FAILED' $out/exits.txt 2>/dev/null; do sleep 20; done
  grep -q '^control passes' $out/exits.txt || exit 1
  for i in 1 2 3 4 5 6 7 8; do eval "pos=\$P$i"; run P2_M64_pos$i $D30 64 none $pos; done
fi
