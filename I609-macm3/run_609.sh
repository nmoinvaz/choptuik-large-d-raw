#!/bin/bash
# I609: hp/modecount_smooth.py over M and D. Usage: run_609.sh 1|2 (two chains, one process each, nice 10).
# Worktree ~/Source/choptuik-large-d-b596 at main 98ee71b (modecount_cx built from 742bb879's source).
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
out=$raw/I609-macm3
cd /Users/nathan/Source/choptuik-large-d-b596/hp
D30=data/states/up6_D30.0688.npz
S48=$raw/I280-macm3/hp_data_after/modecount_state_D61.0264_M48_kf27.npz
S64=$raw/I252-mac/states/modecount_state_D61.0264_M64_kf23.npz
PHYS=2.0797477,0          # lambda_phys as the issue states it
POS=0.055758,1.411769     # the first of #473's eight extra positions (#607's list)
Q1=1.980000,0.749808      # #584's q1 and s3
S3=0.132000,2.912795
run() {  # name state M kf re,im
  caffeinate -is nice -n 10 python3 -u modecount_smooth.py $2 $3 $4 ${5%,*} ${5#*,} > $out/$1.log 2>&1
  echo "$1 exit $? at $(date -u +%FT%TZ)" >> $out/exits.txt
}
gate() {  # the control: at most 1% of the changed entries non-linear
  awk '/entries changed by one ulp/ {c=$(NF-2)} /entries with/ {b=$NF} END {exit !(c > 0 && b * 100 <= c)}' $out/ctrl_M32_phys.log
}
if [ "$1" = 1 ]; then
  run ctrl_M32_phys $D30 32 none $PHYS
  if gate; then echo "control passes at $(date -u +%FT%TZ)" >> $out/exits.txt
  else echo "CONTROL FAILED at $(date -u +%FT%TZ)" >> $out/exits.txt; exit 1; fi
  run ctrl_M32_physfull $D30 32 none 2.079747703853262,0
  run D30_M32_pos $D30 32 none $POS
  run D30_M40_phys $D30 40 none $PHYS
  run D30_M40_pos $D30 40 none $POS
  run D30_M48_phys $D30 48 none $PHYS
  run D30_M48_pos $D30 48 none $POS
  run D61_M48_q1 $S48 48 27 $Q1
  run D61_M48_s3 $S48 48 27 $S3
else
  while ! grep -q '^control passes\|^CONTROL FAILED' $out/exits.txt 2>/dev/null; do sleep 20; done
  grep -q '^control passes' $out/exits.txt || exit 1
  run D61_M64_s3 $S64 64 23 $S3
  run D61_M64_q1 $S64 64 23 $Q1
  run D30_M64_phys $D30 64 none $PHYS
  run D30_M64_pos $D30 64 none $POS
  run D30_M80_phys $D30 80 none $PHYS
  run D30_M80_pos $D30 80 none $POS
fi
