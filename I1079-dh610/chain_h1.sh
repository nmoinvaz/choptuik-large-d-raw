#!/bin/bash
# #1079 dh610, exc1 resumed from H1 (the coordinator's word after the STOP at controls C6: the clean A margin +0.468 is below 0.5, the documented case of A_M.md 6.2; H1, H3 and H2 do not depend on the margins).
# This is chain.sh's part from "# 3. H1" on, with the same command lines, for the box and point that chain.sh made. usage: bash chain_h1.sh N
{
STAGE=chain; . $(dirname $0)/common.sh
pin_check
cd $W/solver/proof || exit 1
mkdir -p logs lemmas_M_runs data
box=data/A_M_box_$BOX.json
[ -f $box ] || { stopmsg "$box is missing"; exit 1; }
PO=$($PY -I -c 'import json, sys; print(",".join(json.load(open(sys.argv[1]))["p_out"]))' data/A_M_refine_M3_$T.json)
XP=$($PY -I -c 'import json, sys; print(",".join(json.load(open(sys.argv[1]))["p"]))' $box)
[ "$XP" = "$PO" ] || { stopmsg "this box's centre p differs from the refine file's p_out"; exit 1; }
note "resume from H1 after the STOP at controls C6 (the coordinator's word): box $BOX, centre p^ = $XP"
# 3. H1
STAGE=h1
run I1079_sector_$BOX lemma6_sector_M.py --M=3 --rp=0.1 --k=20 --box=1e-6 --Z=0.004489 --x=$XP --json=lemmas_M_runs/lemma6_sector_M3_$BOX.json; r1=$?
run I1079_sector_${BOX}_mutate_series lemma6_sector_M.py --M=3 --rp=0.1 --k=20 --box=1e-6 --Z=0.004489 --x=$XP --mutate=series; m1=$?
s1=$(grep -c 'lemma S holds: False (must be False)' logs/I1079_sector_${BOX}_mutate_series.log)
note "H1: exit $r1 (0 wanted; ALL CHECKS PASS: $(grep -c 'ALL CHECKS PASS (M = 3): True' logs/I1079_sector_$BOX.log) of 1), --mutate=series exit $m1 (the script returns 0 for a caught mutation; caught lines $s1 of 1)"
[ $r1 = 0 ] && [ "$s1" = 1 ] && [ "$(grep -c 'ALL CHECKS PASS (M = 3): True' logs/I1079_sector_$BOX.log)" = 1 ] || stopmsg "H1 run exit $r1, series mutation caught lines $s1"
# 4. H3
STAGE=h3
run I1079_export6a_$BOX certify_M.py export6a --box=$box --out=data/A_M_6a_$BOX.json; e=$?
[ $e = 0 ] || { stopmsg "export6a exit $e"; exit 1; }
$PY -I -c '
import json, sys
d = json.load(open(sys.argv[1])); d["x"] = d["p"]
json.dump(d, open(sys.argv[2], "w"))' data/A_M_6a_$BOX.json data/A_M_6a_${BOX}_in.json
run I1079_lemma6a_$BOX lemma6_jump_M.py --M=3 --box=data/A_M_6a_${BOX}_in.json --x=$XP --json=lemmas_M_runs/lemma6a_$BOX.json --save-B=lemmas_M_runs/lemma6a_${BOX}_B.json; a=$?
note "lemma 6a: exit $a (0 wanted); $(grep -E 'rho_6a|lemma S' logs/I1079_lemma6a_$BOX.log | tr '\n' ' ' | cut -c1-300)"
[ $a = 0 ] || { stopmsg "lemma 6a exit $a"; exit 1; }
run I1079_lemma6a_${BOX}_partial lemma6_jump_M.py --M=3 --box=data/A_M_6a_${BOX}_in.json --x=$XP --mutate=partial --load-B=lemmas_M_runs/lemma6a_${BOX}_B.json; p=$?
run I1079_lemma6a_${BOX}_swap lemma6_jump_M.py --M=3 --box=data/A_M_6a_${BOX}_in.json --x=$XP --mutate=swap; s=$?
pc=$(grep -c 'NOT established' logs/I1079_lemma6a_${BOX}_partial.log); sc=$(grep -c 'backward integration failed' logs/I1079_lemma6a_${BOX}_swap.log)
note "lemma 6a controls: --mutate=partial exit $p (caught lines $pc of 1), --mutate=swap exit $s (caught lines $sc of 1); the script returns 0 for a caught mutation"
[ "$pc" -ge 1 ] && [ "$sc" -ge 1 ] || stopmsg "a lemma 6a mutation was not caught (partial lines $pc, swap lines $sc)"
note "chain done"
exit 0
}
