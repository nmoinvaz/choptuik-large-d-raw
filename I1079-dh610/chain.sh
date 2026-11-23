#!/bin/bash
# #1079 dh610, the certificate chain of one excited zero (N = 1: x1, N = 2: x2) on Linux, from macm3's levers.sh (point, one box, krawczyk --point, controls, recheck), hyp1.sh (H1) and hyp.sh h3 (H3),
# without the macOS wrappers. The centre is macm3's refine file (data/A_M_refine_M3_<T>.json, pinned by blob in in_blobs_macm3.txt). No refine, no H0 (not in the order). usage: bash chain.sh N
{
STAGE=chain; . $(dirname $0)/common.sh
pin_check
cd $W/solver/proof || exit 1
mkdir -p logs lemmas_M_runs data
[ "$(git hash-object --no-filters $IN/A_M_refine_M3_$T.json)" = "$(grep " A_M_refine_M3_$T.json" $F/in/in_blobs_macm3.txt | cut -d' ' -f1)" ] || { stopmsg "the refine file is not the pinned blob"; exit 1; }
cp $IN/A_M_refine_M3_$T.json data/A_M_refine_M3_$T.json
PO=$($PY -I -c 'import json, sys; print(",".join(json.load(open(sys.argv[1]))["p_out"]))' data/A_M_refine_M3_$T.json)
note "start: python-flint $($PY -c 'import flint; print(flint.__version__, "FLINT", flint.__FLINT_VERSION__)'), $($PY -V 2>&1), CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16, centre p^ = $PO, box $BOX"
# 1. the point run
run A_M_point_M3${T}_stdout certify_M.py point 3 --p=$PO --out=data/A_M_point_M3$T.json --log=logs/A_M_point_M3$T.log; rc=$?
[ $rc = 0 ] || { stopmsg "point run exit $rc: $(tail -3 logs/A_M_point_M3${T}_stdout.log | tr '\n' ' ' | cut -c1-400)"; exit 1; }
note "point run: $($PY -I -c 'import json, sys; r = json.load(open(sys.argv[1])); print("g_rad %.3e Dg_rad %.3e steps %s sec %.0f" % (r["g_rad"], r["Dg_rad"], r["steps"], r["sec"]))' data/A_M_point_M3$T.json)"
# 2. the box run, krawczyk --point, controls --point, recheck, recheck --mutate
box=data/A_M_box_$BOX.json
run A_M_box_${BOX}_stdout certify_M.py box 3 --centre=data/A_M_refine_M3_$T.json --use_out --h=$H_ --w=$W_ --out=$box --log=logs/A_M_box_$BOX.log; rc=$?
[ $rc = 0 ] || { stopmsg "box run exit $rc: $(tail -3 logs/A_M_box_${BOX}_stdout.log | tr '\n' ' ' | cut -c1-400)"; exit 1; }
run A_M_krawczyk_pt_$BOX certify_M.py krawczyk --box=$box --point=data/A_M_point_M3$T.json; k=$?
note "margins $BOX exit $k (0 wanted): $(head -1 logs/A_M_krawczyk_pt_$BOX.log | cut -c1-200)"
[ $k = 0 ] || { stopmsg "krawczyk --point exit $k"; exit 1; }
run A_M_controls_pt_$BOX certify_M.py controls --box=$box --point=data/A_M_point_M3$T.json; c=$?
run A_M_recheck_pt_$BOX certify_M_recheck.py $box; r=$?
run A_M_recheck_pt_${BOX}_mutate certify_M_recheck.py $box --mutate; m=$?
note "krawczyk exit $k, controls exit $c (0 wanted), recheck exit $r (0 wanted), recheck --mutate exit $m (1 wanted)"
[ $c = 0 ] && [ $r = 0 ] && [ $m = 1 ] || { stopmsg "controls $c, recheck $r, recheck --mutate $m"; exit 1; }
echo "$(stamp) PASS: exc$N box $BOX passes the Krawczyk test (controls exit $c, recheck exit $r, recheck --mutate exit $m)" >> $H
XP=$($PY -I -c 'import json, sys; print(",".join(json.load(open(sys.argv[1]))["p"]))' $box)
[ "$XP" = "$PO" ] || { stopmsg "this box's centre p differs from the refine file's p_out"; exit 1; }
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
