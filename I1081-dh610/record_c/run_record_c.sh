#!/bin/bash
# #1081 dh610 record_c: configuration c as the second excited zero's certificate of record (controls, recheck, H3 = lemma 6a with its mutations, the inclusion). usage: bash run_record_c.sh [selftest [--mutate]]
# Every decision is judge LABEL GOT WANT: a mismatch sets FAIL and the chain stops after the step. selftest: planted exit codes through judge (all as wanted: no FAIL; one wrong: FAIL); --mutate makes judge accept every value, so the wrong one passes: exit 1.
{
set -u
HERE=$(cd $(dirname $0) && pwd)
FAIL=0; MUT=0
judge() { local ok=0; [ "$2" = "$3" ] && ok=1; [ $MUT = 1 ] && ok=1; [ $ok = 1 ] || FAIL=1; local l="judge $1: got $2, wanted $3: $([ $ok = 1 ] && echo ok || echo FAIL)"; echo "$l"; [ -z "${H:-}" ] || echo "$(date -u '+%F %T') $l" >> $H; }
if [ "${1:-}" = selftest ]; then
  [ "${2:-}" = "--mutate" ] && MUT=1
  FAIL=0; judge planted_controls 0 0 > /dev/null; judge planted_mutation 1 1 > /dev/null; [ $FAIL = 0 ] || { echo "selftest: a planted right value failed"; exit 1; }
  judge planted_wrong_exit 1 0; [ $FAIL = 1 ] && { echo "selftest" $([ $MUT = 1 ] && echo --mutate) "PASS (a wrong value is caught)"; exit 0; }
  echo "selftest" $([ $MUT = 1 ] && echo --mutate) "FAIL (a wrong value passed)"; exit 1
fi
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1081-dh610; R=$F/record_c
W=/home/nathan/Source/choptuik-large-d-1081; BR=9676d7c11fa61af808031839b106a4d50fa69547; PY=/home/nathan/Source/venv-i1058/bin/python; H=$R/steps.txt
export CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16 CERTIFY_M_PREC=256 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
unset CERTIFY_M_XI1 REVIEW_PERTURB REVIEW_SEED
stamp() { date -u '+%F %T'; }
note() { echo "$(stamp) $*" >> $H; echo "$(stamp) $*"; }
BOX=$R/A_M_box_M3x2E2_h1e-13_w1e-13.json; PT=$R/A_M_point_M3x2E2.json; RAY=$R/in/ray_exc2_linux.json; B6=$R/A_M_6a_M3x2E2_h1e-13_w1e-13.json; B6I=$R/A_M_6a_M3x2E2_h1e-13_w1e-13_in.json
L6=$R/lemma6a_M3x2E2_h1e-13_w1e-13.json; B=$R/lemma6a_M3x2E2_h1e-13_w1e-13_B.json
[ "$(git -C $W rev-parse HEAD)" = "$BR" ] && [ -z "$(git -C $W status --porcelain)" ] || { note "refuse: $W is not at $BR or is not clean"; exit 1; }
( cd $R && sha256sum -c in/sha256_start.txt --ignore-missing 2>&1 | grep -v "^/" | grep -q FAILED ) && { note "refuse: a file of record differs from in/sha256_start.txt"; exit 1; }
bash $R/run_record_c.sh selftest > $R/selftest_judge.txt 2>&1; s1=$?; bash $R/run_record_c.sh selftest --mutate > $R/selftest_judge_mutate.txt 2>&1; s2=$?
[ $s1 = 0 ] && [ $s2 = 1 ] || { note "STOP: judge selftest $s1 (0 wanted), --mutate $s2 (1 wanted)"; exit 1; }
cd $W/solver/proof || exit 1
run() { local n=$1; shift; note "command $n: cd $W/solver/proof && nice -n 10 env CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16 CERTIFY_M_PREC=256 $PY $*"; local t0=$(date +%s); nice -n 10 $PY "$@" > $R/logs/$n.log 2>&1; rc=$?; note "end $n exit $rc, $(( $(date +%s) - t0 )) s: $(tail -n 1 $R/logs/$n.log | cut -c1-220)"; }
note "start: python-flint $($PY -c 'import flint; print(flint.__version__, "FLINT", flint.__FLINT_VERSION__)'), $($PY -V 2>&1), worktree $BR clean; judge selftest $s1 and --mutate $s2 (0 1 wanted)"
# 1. the record's margins, controls, recheck
run krawczyk certify_M.py krawczyk --point=$PT --box=$BOX; k=$?
judge krawczyk_exit $rc 0; note "krawczyk: $(head -n 1 $R/logs/krawczyk.log | cut -c1-200)"
run controls certify_M.py controls --point=$PT --box=$BOX; judge controls_exit $rc 0; judge controls_all_as_expected $(grep -c 'CONTROLS ALL AS EXPECTED' $R/logs/controls.log) 1
run recheck certify_M_recheck.py $BOX; judge recheck_exit $rc 0
run recheck_mutate certify_M_recheck.py $BOX --mutate; judge recheck_mutate_exit $rc 1; note "recheck --mutate: control FIRED (exit $rc)" | tee -a $H
[ $FAIL = 0 ] || { note "STOP: step 1 as not wanted (see judge lines)"; exit 1; }
note "step 1 as wanted"
# 2. H3: export6a, lemma 6a, the two mutations
run export6a certify_M.py export6a --box=$BOX --out=$B6; judge export6a_exit $rc 0
$PY -I -c '
import json, sys
d = json.load(open(sys.argv[1])); d["x"] = d["p"]
json.dump(d, open(sys.argv[2], "w"))' $B6 $B6I
XP=$($PY -I -c 'import json, sys; print(",".join(json.load(open(sys.argv[1]))["p"]))' $BOX)
judge centre_is_p_out "$XP" "$($PY -I -c 'import json, sys; print(",".join(json.load(open(sys.argv[1]))["p_out"]))' $F/in/A_M_refine_M3_x2E2.json)" | tee -a $H
[ $FAIL = 0 ] || { note "STOP: export6a or the centre as not wanted"; exit 1; }
run lemma6a lemma6_jump_M.py --M=3 --box=$B6I --x=$XP --json=$L6 --save-B=$B; judge lemma6a_exit $rc 0
judge lemma6a_rho_below_1 $(grep -c 'rho_6a = .* < 1: True' $R/logs/lemma6a.log) 1; note "lemma 6a: $(grep -E 'rho_6a|lemma S' $R/logs/lemma6a.log | tr '\n' ' ' | cut -c1-300)"
run lemma6a_partial lemma6_jump_M.py --M=3 --box=$B6I --x=$XP --mutate=partial --load-B=$B; judge partial_exit $rc 0
judge partial_caught $(grep -c 'NOT established' $R/logs/lemma6a_partial.log) 1
run lemma6a_swap lemma6_jump_M.py --M=3 --box=$B6I --x=$XP --mutate=swap; judge swap_exit $rc 0
judge swap_caught $(grep -c 'backward integration failed' $R/logs/lemma6a_swap.log) 1
[ $FAIL = 0 ] || { note "STOP: step 2 as not wanted (see judge lines)"; exit 1; }
note "step 2 as wanted: the script returns 0 for a caught mutation; caught lines partial and swap 1 of 1 each"
# 3. the inclusion
run incl theorem_A_sets_M.py --M=3 --cert=$BOX --ray=$RAY; judge incl_exit $rc 0; judge incl_hold $(grep -c 'THEOREM A SETS (M = 3, mutation None): HOLD' $R/logs/incl.log) 1
run incl_selftest theorem_A_sets_M.py --M=3 --cert=$BOX --ray=$RAY --selftest; judge incl_selftest_exit $rc 0; judge incl_selftest_pass $(grep -c 'SELFTEST (M = 3): PASS' $R/logs/incl_selftest.log) 1
[ $FAIL = 0 ] || { note "STOP: step 3 as not wanted (see judge lines)"; exit 1; }
note "step 3 as wanted"
[ -z "$(git -C $W status --porcelain)" ] || note "WARNING: the worktree is no longer clean: $(git -C $W status --porcelain | head -n 3 | tr '\n' ' ')"
note "record_c done: all steps as wanted"
exit 0
}
