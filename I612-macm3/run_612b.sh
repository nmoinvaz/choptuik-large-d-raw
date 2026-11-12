#!/bin/bash
# I612, the coordinator's message of 2026-11-12 22:26 UTC: M 96 at lambda_phys and position 1 in place of M 56 and 72, and M 48 and M 80
# at positions 2 to 8 (cached states of #609's run). Usage: run_612b.sh X|Y|Z (three chains, one process each, nice 10).
# Position 1 at M 48 is rerun too (#609 ran it on a state that predates that run; the M 48 state in hp/data is now the one made in #609's run).
# Worktree ~/Source/choptuik-large-d-b596 at main ef466c7, modecount_cx built from 742bb879's source.
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
out=$raw/I612-macm3
cd /Users/nathan/Source/choptuik-large-d-b596/hp
D30=data/states/up6_D30.0688.npz
PHYS=2.0797477,0
P1=0.055758,1.411769
P2=3.871717,0.105316
P3=4.285793,0.551490
P4=4.656327,1.390362
P5=0.847147,4.333559
P6=1.057045,2.913917
P7=1.978326,3.721021
P8=4.070967,2.532063
run() {  # name state M kf re,im
  caffeinate -is nice -n 10 python3 -u modecount_smooth.py $2 $3 $4 ${5%,*} ${5#*,} --joint > $out/$1.log 2>&1
  echo "$1 exit $? at $(date -u +%FT%TZ)" >> $out/exits.txt
}
case $1 in
  X) run P3_M96_phys $D30 96 none $PHYS
     run P3_M96_pos1 $D30 96 none $P1 ;;
  Y) for i in 2 3 4 5; do eval "pos=\$P$i"; run P3_M80_pos$i $D30 80 none $pos; done ;;
  Z) for i in 6 7 8; do eval "pos=\$P$i"; run P3_M80_pos$i $D30 80 none $pos; done
     for i in 1 2 3 4 5 6 7 8; do eval "pos=\$P$i"; run P3_M48_pos$i $D30 48 none $pos; done ;;
esac
