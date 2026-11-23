#!/bin/bash
# #1079 macm3b H1 (the coordinator's order, hc 2026-11-23 ~16:50 UTC): lemma S(3), the old sector lemma and the flat estimate over p^ +- 1e-6 at an excited zero, with the documented rp/k of M = 3 (A_lemmas_M.md section 10):
# lemma6_sector_M.py --M=3 --rp=0.1 --k=20 --box=1e-6 --Z=0.004489 --x=<p^> --json=..., and its control --mutate=series (lemma S must fail). Code: worktree ~/Source/choptuik-large-d-1079f at 89553c6b (lemma6_sector_M.py gains --x).
# usage: bash hyp1.sh TAG (the certified box whose centre p is the zero's p^, from the levers' worktree). Records in $P/steps_hyp1.txt. Own session under caffeinate -is.
{
P=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3
WB=/Users/nathan/Source/choptuik-large-d-1079e      # the boxes (feat/certify-excited 1addcada)
W=/Users/nathan/Source/choptuik-large-d-1079f       # the code (feat/certify-excited 89553c6b)
BR=89553c6b1645c1a5711a4d17fb71306963b963a7
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
H=$P/steps_hyp1.txt
TAG=$1
stamp() { date -u '+%F %T'; }
note() { echo "hyp1 $TAG $(stamp) $*" >> $H; }
[ "$(git -C $W rev-parse HEAD)" = "$BR" ] && [ -z "$(git -C $W status --porcelain --untracked-files=no)" ] || { echo "$(stamp) STOP: hyp1 $TAG: the worktree $W is not at $BR or has tracked changes" >> $H; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
XP=$($PY -I -c 'import json, sys; print(",".join(json.load(open(sys.argv[1]))["p"]))' $WB/solver/proof/data/A_M_box_$TAG.json) || { echo "$(stamp) STOP: hyp1 $TAG: cannot read the box" >> $H; exit 1; }
cd $W/solver/proof || exit 1
mkdir -p logs lemmas_M_runs
note "start: python-flint $($PY -c 'import flint; print(flint.__version__, "FLINT", flint.__FLINT_VERSION__)'), python $($PY -V 2>&1); centre p^ = $XP"
note "command: cd $W/solver/proof && nice -n 10 $PY lemma6_sector_M.py --M=3 --rp=0.1 --k=20 --box=1e-6 --Z=0.004489 --x=<p^> --json=lemmas_M_runs/lemma6_sector_M3_$TAG.json > logs/I1079_sector_$TAG.log 2>&1"
nice -n 10 $PY lemma6_sector_M.py --M=3 --rp=0.1 --k=20 --box=1e-6 --Z=0.004489 --x=$XP --json=lemmas_M_runs/lemma6_sector_M3_$TAG.json > logs/I1079_sector_$TAG.log 2>&1; r=$?
note "lemma6_sector_M.py exit $r (0 wanted): $(tail -1 logs/I1079_sector_$TAG.log | cut -c1-200)"
note "command: ... --mutate=series (same options, no json) > logs/I1079_sector_${TAG}_mutate_series.log"
nice -n 10 $PY lemma6_sector_M.py --M=3 --rp=0.1 --k=20 --box=1e-6 --Z=0.004489 --x=$XP --mutate=series > logs/I1079_sector_${TAG}_mutate_series.log 2>&1; m=$?
note "--mutate=series exit $m (nonzero wanted): $(tail -1 logs/I1079_sector_${TAG}_mutate_series.log | cut -c1-200)"
[ $r = 0 ] && [ $m != 0 ] || echo "$(stamp) STOP: hyp1 $TAG: sector run exit $r, series mutation exit $m" >> $H
note "h1 done"
exit 0
}
