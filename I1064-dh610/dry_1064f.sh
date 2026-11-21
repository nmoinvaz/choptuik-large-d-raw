#!/bin/bash
# dry tests of run1064f.sh on the real state (D 237.7132, ks 307), main 276aa1cd: pass path (control ks 307 converges, ks331 and ks347 killed at a 600 s cap) and the control-failed path (control killed at 45 s), in parallel
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
for d in dry_f1 dry_f2; do [ -e $d ] && { echo "$d exists"; exit 1; }; mkdir $d; done
date -u '+%F %T dry runs start'
OUT1064=$PWD/dry_f1 CAP1064=600 bash $PWD/run1064f.sh > dry_f1/stdout.txt 2>&1 &
p1=$!
OUT1064=$PWD/dry_f2 CAP1064=45 bash $PWD/run1064f.sh > dry_f2/stdout.txt 2>&1 &
p2=$!
wait $p1; r1=$?; wait $p2; r2=$?
date -u '+%F %T dry runs end'; echo "dry run exits $r1 $r2"
python3 -I check_dry1064f.py pass dry_f1 600 | tee dry_f1/check_dry1064f.txt; c1=${PIPESTATUS[0]}
python3 -I check_dry1064f.py ctlfail dry_f2 45 | tee dry_f2/check_dry1064f.txt; c2=${PIPESTATUS[0]}
echo "checks $c1 $c2"
[ "$c1$c2" = "00" ] && echo "DRY OK" || echo "DRY FAILED"
exit 0
