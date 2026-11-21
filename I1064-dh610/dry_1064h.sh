#!/bin/bash
# dry tests of run1064h.sh on the real state and flags (main 276aa1cd): pass path (ks395 and ks443 killed at a 300 s cap, the ks 307 control base of ho2_D237.7132 reused) and the no-control path (CTL1064H names a missing file), in parallel
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
for d in dry_h1 dry_h2; do [ -e $d ] && { echo "$d exists"; exit 1; }; mkdir $d; done
date -u '+%F %T dry runs start'
OUT1064=$PWD/dry_h1 CAP1064=300 bash $PWD/run1064h.sh > dry_h1/stdout.txt 2>&1 &
p1=$!
OUT1064=$PWD/dry_h2 CAP1064=300 CTL1064H=/nonexistent/base.npz bash $PWD/run1064h.sh > dry_h2/stdout.txt 2>&1 &
p2=$!
wait $p1; r1=$?; wait $p2; r2=$?
date -u '+%F %T dry runs end'; echo "dry run exits $r1 $r2"
python3 -I check_dry1064h.py pass dry_h1 300 | tee dry_h1/check_dry1064h.txt; c1=${PIPESTATUS[0]}
python3 -I check_dry1064h.py nocontrol dry_h2 300 | tee dry_h2/check_dry1064h.txt; c2=${PIPESTATUS[0]}
echo "checks $c1 $c2"
[ "$c1$c2" = "00" ] && echo "DRY OK" || echo "DRY FAILED"
exit 0
