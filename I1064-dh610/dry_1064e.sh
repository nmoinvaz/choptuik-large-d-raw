#!/bin/bash
# dry tests of run1064e.sh on the real state (D 262.0099), main 276aa1cd: pass path (control with --elim_switch 1e-9 converges, ks315own and ks315nat killed at a 300 s cap) and the control-failed path (control killed at 45 s), in parallel
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
for d in dry_e1 dry_e2; do [ -e $d ] && { echo "$d exists"; exit 1; }; mkdir $d; done
date -u '+%F %T dry runs start'
OUT1064=$PWD/dry_e1 CAP1064=300 bash $PWD/run1064e.sh > dry_e1/stdout.txt 2>&1 &
p1=$!
OUT1064=$PWD/dry_e2 CAP1064=45 bash $PWD/run1064e.sh > dry_e2/stdout.txt 2>&1 &
p2=$!
wait $p1; r1=$?; wait $p2; r2=$?
date -u '+%F %T dry runs end'; echo "dry run exits $r1 $r2"
python3 -I check_dry1064e.py pass dry_e1 300 | tee dry_e1/check_dry1064e.txt; c1=${PIPESTATUS[0]}
python3 -I check_dry1064e.py ctlfail dry_e2 45 | tee dry_e2/check_dry1064e.txt; c2=${PIPESTATUS[0]}
echo "checks $c1 $c2"
[ "$c1$c2" = "00" ] && echo "DRY OK" || echo "DRY FAILED"
exit 0
