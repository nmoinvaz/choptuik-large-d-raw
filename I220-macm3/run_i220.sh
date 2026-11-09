#!/bin/bash
# I220-macm3: win2's B of lemma 6a(5) at p-hat loaded on macm3, with controls.
cd ~/Source/choptuik-large-d/solver/proof
PY=/Users/nathan/Source/venv-macm3-314/bin/python
R=../../../choptuik-large-d-raw/I220-macm3
BOX=../../../choptuik-large-d-raw/I103-macm3/A_M2_6a_M5_sub1e-18.json
BW=../../../choptuik-large-d-raw/I196-win2/B_M5_sub1e-18_phat.json
PHAT=$(python3 -c "import json; print(','.join(json.load(open('$BOX'))['p']))")
echo "$PHAT" > $R/centre_passed.txt
date -u '+start %Y-%m-%d %H:%M:%S UTC' >> $R/driver.txt

caffeinate -is nice -n 10 $PY -u lemma6_jump_M.py --M=5 --box=$BOX --x=$PHAT --rp=0.08 --k=20 --load-B=$BW --json=$R/lemma6a_loadB_win2_phat.json > $R/lemma6a_loadB_win2_phat.log 2>&1
echo "loadB win2 exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
caffeinate -is nice -n 10 $PY -u lemma6_jump_M.py --M=5 --box=$BOX --x=$PHAT --rp=0.08 --k=20 --load-B=$BW --mutate=partial > $R/lemma6a_loadB_win2_phat_partial.log 2>&1
echo "partial exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
caffeinate -is nice -n 10 $PY -u lemma6_jump_M.py --M=5 --box=$BOX --x=$PHAT --rp=0.08 --k=20 --load-B=$BW --mutate=coords > $R/lemma6a_loadB_win2_phat_coords.log 2>&1
echo "coords exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
caffeinate -is nice -n 10 $PY -u review_39/b_float.py --B=$BW --box=$BOX > $R/b_float_win2B.log 2>&1
echo "b_float exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
caffeinate -is nice -n 10 $PY -u review_39/b_float.py --B=$BW --box=$BOX --mutate=w > $R/b_float_win2B_mutate_w.log 2>&1
echo "b_float mutate=w exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
date -u '+end %Y-%m-%d %H:%M:%S UTC' >> $R/driver.txt
