#!/bin/bash
# #1079 macm3b hypotheses (the coordinator's order, hc 2026-11-23 ~16:30 UTC): for a passing box TAG (e.g. M3x2E2_h1e-12_w1e-12) with CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16:
#   stage h0: (H0) start_cover_M2.py --box=<box> --rerun (exit 0 wanted) and --rerun --mutate=overlap (must fail); and, as information, without --rerun (the stored rows are the fundamental's: NOT COVERED, exit 1 expected)
#   stage h3: (H3) certify_M.py export6a --box=<box> --out=data/A_M_6a_TAG.json; the input JSON with x = the box's centre p (the documented practice, A_lemmas_M.md section 7); lemma6_jump_M.py --M=3 --box=<in.json> --x=<p> (lemma S and the flat estimate over p +- 1e-6, then the backward flow and rho_6a);
#     its documented controls --mutate=partial (--load-B) and --mutate=swap (both must fail).
# usage: bash hyp.sh STAGE TAG. From the clean worktree of feat/certify-excited (1addcada), solver/proof; nice 10, 1 thread per BLAS. Records in $P/steps_hyp.txt. Own session under caffeinate -is.
{
P=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3
W=/Users/nathan/Source/choptuik-large-d-1079e
BR=1addcada42157c197ad1193621b988a978bb96f7
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
H=$P/steps_hyp.txt
ST=$1; TAG=$2
stamp() { date -u '+%F %T'; }
note() { echo "hyp $ST $TAG $(stamp) $*" >> $H; }
export CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
[ "$(git -C $W rev-parse HEAD)" = "$BR" ] && [ -z "$(git -C $W status --porcelain --untracked-files=no)" ] || { echo "$(stamp) STOP: hyp $ST $TAG: the worktree is not at $BR or has tracked changes" >> $H; exit 1; }
cd $W/solver/proof || exit 1
[ -f data/A_M_box_$TAG.json ] || { echo "$(stamp) STOP: hyp $ST $TAG: data/A_M_box_$TAG.json is missing" >> $H; exit 1; }
note "start: python-flint $($PY -c 'import flint; print(flint.__version__, "FLINT", flint.__FLINT_VERSION__)'), python $($PY -V 2>&1), CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16; box data/A_M_box_$TAG.json"
run() {   # run NAME CMD...: output to logs/NAME.log, returns the exit code
    local name=$1; shift
    note "$name command: cd $W/solver/proof && nice -n 10 env CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16 $PY $* > logs/$name.log 2>&1"
    nice -n 10 $PY "$@" > logs/$name.log 2>&1; local rc=$?
    note "$name end exit $rc: $(tail -1 logs/$name.log | cut -c1-220)"
    return $rc
}
if [ $ST = h0 ]; then
  run I1079_start_cover_$TAG start_cover_M2.py --box=data/A_M_box_$TAG.json --rerun; a=$?
  run I1079_start_cover_${TAG}_mutate_overlap start_cover_M2.py --box=data/A_M_box_$TAG.json --rerun --mutate=overlap; b=$?
  run I1079_start_cover_${TAG}_stored start_cover_M2.py --box=data/A_M_box_$TAG.json; c=$?
  note "H0: --rerun exit $a (0 wanted), --rerun --mutate=overlap exit $b (nonzero wanted), stored rows exit $c (information; the stored rows are the fundamental's)"
  [ $a = 0 ] && [ $b != 0 ] || echo "$(stamp) STOP: hyp h0 $TAG: --rerun exit $a, --mutate=overlap exit $b" >> $H
  note "h0 done"
elif [ $ST = h3 ]; then
  run I1079_export6a_$TAG certify_M.py export6a --box=data/A_M_box_$TAG.json --out=data/A_M_6a_$TAG.json; e=$?
  [ $e = 0 ] || { echo "$(stamp) STOP: hyp h3 $TAG: export6a exit $e" >> $H; exit 1; }
  XP=$($PY -I -c '
import json, sys
d = json.load(open(sys.argv[1])); d["x"] = d["p"]
json.dump(d, open(sys.argv[2], "w")); print(",".join(d["p"]))' data/A_M_6a_$TAG.json data/A_M_6a_${TAG}_in.json)
  note "input json data/A_M_6a_${TAG}_in.json: the export with x = p = $XP"
  mkdir -p lemmas_M_runs
  run I1079_lemma6a_$TAG lemma6_jump_M.py --M=3 --box=data/A_M_6a_${TAG}_in.json --x=$XP --json=lemmas_M_runs/lemma6a_$TAG.json --save-B=lemmas_M_runs/lemma6a_${TAG}_B.json; r=$?
  note "lemma 6a: exit $r (0 wanted); $(grep -E 'rho_6a|lemma S' logs/I1079_lemma6a_$TAG.log | tr '\n' ' ' | cut -c1-300)"
  [ $r = 0 ] || echo "$(stamp) STOP: hyp h3 $TAG: lemma 6a exit $r (the cause is in logs/I1079_lemma6a_$TAG.log)" >> $H
  if [ $r = 0 ]; then
    run I1079_lemma6a_${TAG}_partial lemma6_jump_M.py --M=3 --box=data/A_M_6a_${TAG}_in.json --x=$XP --mutate=partial --load-B=lemmas_M_runs/lemma6a_${TAG}_B.json; p=$?
    run I1079_lemma6a_${TAG}_swap lemma6_jump_M.py --M=3 --box=data/A_M_6a_${TAG}_in.json --x=$XP --mutate=swap; s=$?
    note "lemma 6a controls: --mutate=partial exit $p, --mutate=swap exit $s (nonzero wanted each)"
    [ $p != 0 ] && [ $s != 0 ] || echo "$(stamp) STOP: hyp h3 $TAG: a lemma 6a mutation exited 0 (partial $p, swap $s)" >> $H
  fi
  note "h3 done"
fi
exit 0
}
