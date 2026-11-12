#!/bin/bash
# I624: hp/modecount_smooth.py --joint at q1 and s3 of #584 on D 61 states at M 40 and M 80 resampled from I252-mac's M 64 kf 23 state,
# with #612's M 32 D 30 control. Usage: run_624.sh C|P|Q|R (C = the control, then P, Q, R, one process each, nice 10).
# Worktree ~/Source/choptuik-large-d-b596 at main ef466c7 (the invocation of #612, only state and M changed).
# R is an addition to the issue: M 48 resampled from the same kf 23 state (#609's M 48 used I280-macm3's kf 27 state).
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
out=$raw/I624-macm3
cd /Users/nathan/Source/choptuik-large-d-b596/hp
D30=data/states/up6_D30.0688.npz
S64=$raw/I252-mac/states/modecount_state_D61.0264_M64_kf23.npz
Q1=1.980000,0.749808
S3=0.132000,2.912795
run() {  # name state M kf re,im
  caffeinate -is nice -n 10 python3 -u modecount_smooth.py $2 $3 $4 ${5%,*} ${5#*,} --joint > $out/$1.log 2>&1
  echo "$1 exit $? at $(date -u +%FT%TZ)" >> $out/exits.txt
}
gate() {  # #612's control: the one entry at block (0, 0), row 8, column 29, field p
  grep -q "^  entries with .*: 1$" $out/ctrl_M32_phys.log && grep -q "largest: row 8, col 29:" $out/ctrl_M32_phys.log &&
  grep -q "rows by field (p, m, a, c): \[1 0 0 0\]" $out/ctrl_M32_phys.log &&
  awk '/counts, 1 in all/ {getline; if ($1 == 1) ok = 1} END {exit !ok}' $out/ctrl_M32_phys.log
}
if [ "$1" = C ]; then
  while ! grep -q '^up12_D58.0060 b5 exit' $raw/I615-macm3/exits.txt 2>/dev/null; do sleep 20; done   # after #615's runs
  run ctrl_M32_phys $D30 32 none 2.0797477,0
  if gate; then echo "control passes at $(date -u +%FT%TZ)" >> $out/exits.txt
  else echo "CONTROL FAILED at $(date -u +%FT%TZ)" >> $out/exits.txt; fi
else
  while ! grep -q '^control passes\|^CONTROL FAILED' $out/exits.txt 2>/dev/null; do sleep 20; done
  grep -q '^control passes' $out/exits.txt || exit 1
  case $1 in
    P) run M40_q1 $S64 40 23 $Q1; run M40_s3 $S64 40 23 $S3 ;;
    Q) run M80_q1 $S64 80 23 $Q1; run M80_s3 $S64 80 23 $S3 ;;
    R) run M48kf23_q1 $S64 48 23 $Q1; run M48kf23_s3 $S64 48 23 $S3 ;;
  esac
fi
