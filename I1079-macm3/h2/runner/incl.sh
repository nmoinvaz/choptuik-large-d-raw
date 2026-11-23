#!/bin/bash
# #1079 macm3b H2 inclusion (the coordinator's order): theorem_A_sets_M.py --M=3 --cert=<that zero's box JSON> --ray=<the covering's ray.json> and --selftest with the same options (its centre mutation must fail).
# From the worktree ~/Source/choptuik-large-d-1079g (feat/certify-excited c40fbc77, theorem_A_sets_M.py gains --cert and --ray), solver/proof. usage: bash incl.sh N. Records in $P/steps_h2.txt.
{
P=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3
WB=/Users/nathan/Source/choptuik-large-d-1079e
WC=/Users/nathan/Source/choptuik-large-d-1079f
W=/Users/nathan/Source/choptuik-large-d-1079g
BR=c40fbc77d8505d8838c2c0ecc51d3feaa5d7a340
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
H=$P/steps_h2.txt
N=$1
case $N in 1) BOX=M3x1E2_h1e-12_w1e-13 ;; 2) BOX=M3x2E2_h1e-12_w1e-12 ;; *) echo "$(date -u '+%F %T') STOP: incl unknown zero $N" >> $H; exit 1 ;; esac
stamp() { date -u '+%F %T'; }
note() { echo "h2 incl exc$N $(stamp) $*" >> $H; }
[ "$(git -C $W rev-parse HEAD)" = "$BR" ] && [ -z "$(git -C $W status --porcelain --untracked-files=no)" ] || { echo "$(stamp) STOP: incl exc$N: the worktree $W is not at $BR or has tracked changes" >> $H; exit 1; }
CERT=$WB/solver/proof/data/A_M_box_$BOX.json; RAY=$WC/solver/proof/lemma6b1_runs_M3_exc$N/ray.json
[ -f $CERT ] && [ -f $RAY ] || { echo "$(stamp) STOP: incl exc$N: $CERT or $RAY is missing" >> $H; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $W/solver/proof || exit 1
mkdir -p logs
note "start: python-flint $($PY -c 'import flint; print(flint.__version__, "FLINT", flint.__FLINT_VERSION__)'), $($PY -V 2>&1); cert $CERT; ray $RAY"
note "command: cd $W/solver/proof && nice -n 10 $PY theorem_A_sets_M.py --M=3 --cert=$CERT --ray=$RAY > logs/I1079_incl_exc$N.log 2>&1"
nice -n 10 $PY theorem_A_sets_M.py --M=3 --cert=$CERT --ray=$RAY > logs/I1079_incl_exc$N.log 2>&1; a=$?
note "theorem_A_sets_M.py exit $a (0 = HOLD wanted): $(tail -1 logs/I1079_incl_exc$N.log | cut -c1-220)"
nice -n 10 $PY theorem_A_sets_M.py --M=3 --cert=$CERT --ray=$RAY --selftest > logs/I1079_incl_exc${N}_selftest.log 2>&1; b=$?
note "theorem_A_sets_M.py --selftest exit $b (0 wanted): $(tail -1 logs/I1079_incl_exc${N}_selftest.log | cut -c1-220)"
[ $a = 0 ] && [ $b = 0 ] || echo "$(stamp) STOP: incl exc$N: exit $a, selftest exit $b" >> $H
note "incl done"
exit 0
}
