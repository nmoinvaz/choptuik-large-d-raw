#!/usr/bin/env bash
# #903 hourly: compare the chain's base pivots with #603's, copy the chain's files into raw I903-mac/chain_fixed, commit, push.
# Prints the raw commit, then the comparison's rows (step, D, p_fixed, p_603, ln ratio).
SP=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad
R=$SP/raw-wt
/Users/nathan/venv-314/bin/python $SP/i903/compare_903.py $R $SP/i903/chain_fixed.log > $SP/i903/compare_chain.txt || exit 1
(cd /Users/nathan/Source/choptuik-large-d-xf-903/hp && PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2:. /Users/nathan/venv-314/bin/python $SP/i903/delta_cmp_903.py $R $SP/i903 > $SP/i903/delta_cmp.txt) || exit 1
cd $R || exit 1
cp $SP/i903/delta_cmp.txt $SP/i903/delta_cmp_903.py $SP/i903/hourly_push.sh I903-mac/chain_fixed/
cp $SP/i903/chain_fixed.log $SP/i903/exits_chain.txt $SP/i903/compare_chain.txt I903-mac/chain_fixed/
cp $SP/i903/chain_fixed/anm_pin3_D*.npz $SP/i903/chain_fixed/jet_pin3_D*.npz $SP/i903/chain_fixed/anm_run.jsonl I903-mac/chain_fixed/ 2>/dev/null
D=$(grep -o "^step [0-9]*: D [0-9.]*" $SP/i903/chain_fixed.log | tail -1 | awk '{print $4}')
python3 make_index.py >/dev/null && git add I903-mac INDEX.md && git commit -q -m "I903-mac: the fixed-order chain at base D $D" && git pull -q --rebase origin main && git push -q origin HEAD:main || exit 1
git rev-parse --short HEAD
tail -n +3 $SP/i903/compare_chain.txt
tail -n +2 $SP/i903/delta_cmp.txt
