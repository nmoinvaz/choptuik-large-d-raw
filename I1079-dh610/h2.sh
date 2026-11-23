#!/bin/bash
# #1079 dh610, H2 of one excited zero on Linux (macm3's h2.sh, without the wrappers): lemma6b1_cover_M.py at the centre p^ of macm3's refine file, M = 3, --h=1e-11, --tag=_exc<N>_linux:
# ray --c1, row --j=11, rows (two processes: --only=0,2,4,6,8,10 and --only=1,3,5,7,9, run one after the other here: 4 processes in all beside the other zero), check --json, c1check, mutate --j=11. usage: bash h2.sh N
{
STAGE=h2; . $(dirname $0)/common.sh
pin_check
cd $W/solver/proof || exit 1
mkdir -p logs lemmas_M_runs
XP=$($PY -I -c 'import json, sys; print(",".join(json.load(open(sys.argv[1]))["p_out"]))' $IN/A_M_refine_M3_$T.json)
TAG=_exc${N}_linux
COM="--M=3 --x=$XP --h=1e-11 --tag=$TAG"
lrun() { local name=$1; shift; local t0=$(date +%s)
  note "$name command: cd $W/solver/proof && nice -n 15 $PY -u lemma6b1_cover_M.py $1 --M=3 --x=<p^ of $BOX> --h=1e-11 --tag=$TAG ${*:2} > logs/$name.log 2>&1"
  nice -n 15 $PY -u lemma6b1_cover_M.py "$1" $COM "${@:2}" >> logs/$name.log 2>&1; local rc=$?
  note "$name end exit $rc, $(( $(date +%s) - t0 )) s: $(tail -1 logs/$name.log | cut -c1-220)"; return $rc; }
note "start: python-flint $($PY -c 'import flint; print(flint.__version__, "FLINT", flint.__FLINT_VERSION__)'), $($PY -V 2>&1); p^ = $XP"
lrun I1079_h2_probe_exc$N probe; pr=$?
lrun I1079_h2_ray_exc$N ray --c1; r=$?
[ $r = 0 ] || { stopmsg "ray --c1 exit $r"; exit 1; }
lrun I1079_h2_row11_exc$N row --j=11; r11=$?
[ $r11 = 0 ] || { stopmsg "row --j=11 exit $r11"; exit 1; }
lrun I1079_h2_rowsA_exc$N rows --only=0,2,4,6,8,10; a=$?
lrun I1079_h2_rowsB_exc$N rows --only=1,3,5,7,9; b=$?
[ $a = 0 ] && [ $b = 0 ] || { stopmsg "rows exit $a, $b"; exit 1; }
lrun I1079_h2_check_exc$N check --json=lemmas_M_runs/lemma6b1_check_M3_exc${N}_linux.json; c=$?
lrun I1079_h2_c1check_exc$N c1check; d=$?
lrun I1079_h2_mutate_exc$N mutate --j=11; m=$?
mc=$(grep -c '0 of 12 discs of row 11 certified (must be 0)' logs/I1079_h2_mutate_exc$N.log)
note "H2: probe exit $pr, check exit $c (0 wanted; PASS lines $(grep -c 'LEMMA 6b_1 CHECK: PASS' logs/I1079_h2_check_exc$N.log) of 1), c1check exit $d (0 wanted; $(tail -1 logs/I1079_h2_c1check_exc$N.log | cut -c1-120)), mutate --j=11 exit $m, caught lines $mc of 1"
[ $c = 0 ] && [ $d = 0 ] && [ "$mc" = 1 ] || { stopmsg "check $c, c1check $d, mutate caught lines $mc"; exit 1; }
note "h2 done"
exit 0
}
