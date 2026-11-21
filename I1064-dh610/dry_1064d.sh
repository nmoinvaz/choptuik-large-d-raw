#!/bin/bash
# dry tests of run1064d.sh on the real state (D 261.6229), main 276aa1cd: pass path (control with --reseed_base 1 converges, ks294 killed at a 420 s cap) and the control-failed path (control killed at 45 s), in parallel
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
export R_1064D="294"
for d in dry_d1 dry_d2; do [ -e $d ] && { echo "$d exists"; exit 1; }; mkdir $d; done
date -u '+%F %T dry runs start'
OUT1064=$PWD/dry_d1 CAP1064=420 bash $PWD/run1064d.sh > dry_d1/stdout.txt 2>&1 &
p1=$!
OUT1064=$PWD/dry_d2 CAP1064=45 bash $PWD/run1064d.sh > dry_d2/stdout.txt 2>&1 &
p2=$!
wait $p1; r1=$?; wait $p2; r2=$?
date -u '+%F %T dry runs end'; echo "dry run exits $r1 $r2"
python3 -I check_dry1064d.py pass dry_d1 420 | tee dry_d1/check_dry1064d.txt; c1=${PIPESTATUS[0]}
python3 -I check_dry1064d.py ctlfail dry_d2 45 | tee dry_d2/check_dry1064d.txt; c2=${PIPESTATUS[0]}
echo "checks $c1 $c2"
[ "$c1$c2" = "00" ] && echo "DRY OK" || echo "DRY FAILED"
exit 0
