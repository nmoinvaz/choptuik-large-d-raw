#!/bin/bash
# #1079 dh610, the inclusion of one excited zero on Linux (macm3's incl.sh, without the wrappers): theorem_A_sets_M.py --M=3 --cert=<this machine's box> --ray=<this machine's ray.json> and --selftest. usage: bash incl.sh N
{
STAGE=incl; . $(dirname $0)/common.sh
pin_check
cd $W/solver/proof || exit 1
CERT=$W/solver/proof/data/A_M_box_$BOX.json; RAY=$W/solver/proof/lemma6b1_runs_M3_exc${N}_linux/ray.json
[ -f $CERT ] && [ -f $RAY ] || { stopmsg "$CERT or $RAY is missing"; exit 1; }
note "start: python-flint $($PY -c 'import flint; print(flint.__version__, "FLINT", flint.__FLINT_VERSION__)'), $($PY -V 2>&1); cert $CERT; ray $RAY"
run I1079_incl_exc$N theorem_A_sets_M.py --M=3 --cert=$CERT --ray=$RAY; a=$?
run I1079_incl_exc${N}_selftest theorem_A_sets_M.py --M=3 --cert=$CERT --ray=$RAY --selftest; b=$?
[ $a = 0 ] && [ $b = 0 ] || { stopmsg "inclusion exit $a, selftest exit $b"; exit 1; }
note "incl done"
exit 0
}
