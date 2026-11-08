#!/bin/zsh
# the review's 6a runs: clean at both centres, and the mutations in the review and in the original
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad
RAW=/Users/nathan/Source/choptuik-large-d-raw
O=$RAW/I39-mac
B=$RAW/I103-macm3/B_M5_sub1e-18.json
BX=$RAW/I103-macm3/A_M2_6a_M5_sub1e-18.json
FL=$O/flat_6a_M5.json
PROOF=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-ab6ec531e45efaac2/solver/proof
$S/run6a.sh --B=$B --box=$BX --flat=$FL --centre=xhat --json=$O/check_6a_I103_xhat.json > $O/check_6a_I103_xhat.log 2>&1
for m in coords partial Bscale; do
  $S/run6a.sh --B=$B --box=$BX --flat=$FL --centre=xhat --mutate=$m --write_B=$O/B_M5_sub1e-18_$m.json --json=$O/check_6a_mut_$m.json > $O/check_6a_mut_$m.log 2>&1
done
# the original on the review's Bscale B (post-processing only, as its partial and coords controls)
[ -n "$PAUSE" ] && kill -STOP $PAUSE
cd $PROOF && nice -n 10 /Users/nathan/venv-qd/bin/python -u lemma6_jump_M.py --M=5 --box=$BX --rp=0.08 --k=20 --load-B=$O/B_M5_sub1e-18_Bscale.json > $O/orig_6a_mut_Bscale.log 2>&1
echo "orig Bscale exit $?" >> $O/orig_6a_mut_Bscale.log
# the original on the review's re-encoding of the clean B (the encoding must not change rho_6a)
cd $PROOF && nice -n 10 /Users/nathan/venv-qd/bin/python -u lemma6_jump_M.py --M=5 --box=$BX --rp=0.08 --k=20 --load-B=$O/B_M5_sub1e-18_coords.json > $O/orig_6a_reencoded_clean.log 2>&1
echo "orig reencoded exit $?" >> $O/orig_6a_reencoded_clean.log
[ -n "$PAUSE" ] && kill -CONT $PAUSE
