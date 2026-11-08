#!/bin/bash
# I184-macm3: lemma 6a(5) at p^ (the issue's commands), then the controls and #39's float control of B.
cd ~/Source/choptuik-large-d/solver/proof
PY=/Users/nathan/Source/venv-macm3/bin/python
R=../../../choptuik-large-d-raw/I184-macm3
BOX=../../../choptuik-large-d-raw/I103-macm3/A_M2_6a_M5_sub1e-18.json
PHAT=$(python3 -c "import json; print(','.join(json.load(open('$BOX'))['p']))")
echo "$PHAT" > $R/centre_passed.txt
date -u '+start %Y-%m-%d %H:%M:%S UTC' >> $R/driver.txt

echo "--x=$PHAT" > $R/cmd_run.txt
caffeinate -is nice -n 10 $PY -u lemma6_jump_M.py --M=5 --box=$BOX --x=$PHAT --rp=0.08 --k=20 --save-B=$R/B_M5_sub1e-18_phat.json --json=$R/lemma6a_M5_sub1e-18_phat.json > $R/lemma6a_M5_phat.log 2>&1
echo "run exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
if [ ! -s $R/B_M5_sub1e-18_phat.json ]
then
  echo "no B saved, controls not run" >> $R/exits.txt
  exit 1
fi

caffeinate -is nice -n 10 $PY -u lemma6_jump_M.py --M=5 --box=$BOX --x=$PHAT --rp=0.08 --k=20 --load-B=$R/B_M5_sub1e-18_phat.json --mutate=partial > $R/lemma6a_M5_phat_partial.log 2>&1
echo "partial exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
caffeinate -is nice -n 10 $PY -u lemma6_jump_M.py --M=5 --box=$BOX --x=$PHAT --rp=0.08 --k=20 --load-B=$R/B_M5_sub1e-18_phat.json --mutate=coords > $R/lemma6a_M5_phat_coords.log 2>&1
echo "coords exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
caffeinate -is nice -n 10 $PY -u lemma6_jump_M.py --M=5 --box=$BOX --x=$PHAT --rp=0.08 --k=20 --mutate=swap > $R/lemma6a_M5_phat_swap.log 2>&1
echo "swap exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt

caffeinate -is nice -n 10 $PY -u review_39/b_float.py --B=$R/B_M5_sub1e-18_phat.json --box=$BOX > $R/b_float_new.log 2>&1
echo "b_float exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
caffeinate -is nice -n 10 $PY -u review_39/b_float.py --B=$R/B_M5_sub1e-18_phat.json --box=$BOX --mutate=w > $R/b_float_new_mutate_w.log 2>&1
echo "b_float mutate=w exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
date -u '+end %Y-%m-%d %H:%M:%S UTC' >> $R/driver.txt
