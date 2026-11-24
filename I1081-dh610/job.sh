#!/bin/bash
# job.sh CFG KIND: one run of #1081 (KIND: point | U | s1 .. s6) at configuration CFG (a, b, c), in $F/cfg_<CFG>/, from solver/proof of the pinned worktree, nice 10; /usr/bin/time -v to logs/<KIND>.time
# Exits 255 on a failure (so that xargs stops reading further jobs); refuses an existing output.
. $(dirname $0)/common.sh
C=$1; K=$2; cfg $C || exit 255
D=$F/cfg_$C; mkdir -p $D/logs
cd $W/solver/proof || exit 255
export CERTIFY_M_PREC=$PREC
CEN=$F/in/A_M_refine_M3_x2E2.json
case $K in
  point) OUT=$D/point.json
         PO=$($PY -I -c 'import json, sys; print(",".join(json.load(open(sys.argv[1]))["p_out"]))' $CEN)
         CMD=(certify_M.py point 3 --p=$PO --out=$OUT --log=$D/logs/point.log) ;;
  U)     OUT=$D/box_U.json
         CMD=(certify_M.py box 3 --centre=$CEN --use_out --h=$HH --w=$WW --out=$OUT --log=$D/logs/box_U.log) ;;
  s[1-6]) OUT=$D/box_$K.json
         export REVIEW_PERTURB=qr REVIEW_SEED=${K#s}
         CMD=(review_1079/perturb_box.py box 3 --centre=$CEN --use_out --h=$HH --w=$WW --out=$OUT --log=$D/logs/box_$K.log) ;;
  *) echo "unknown kind $K" >&2; exit 255 ;;
esac
[ ! -e $OUT ] || { echo "$(stamp) refuse $C $K: $OUT exists" >> $H; exit 255; }
echo "$(stamp) start $C $K" >> $H
echo "$(stamp) command $C $K: cd $W/solver/proof && nice -n 10 env CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16 CERTIFY_M_PREC=$PREC ${REVIEW_PERTURB:+REVIEW_PERTURB=$REVIEW_PERTURB REVIEW_SEED=$REVIEW_SEED }$PY ${CMD[*]}" >> $H
t0=$(date +%s)
nice -n 10 /usr/bin/time -v -o $D/logs/$K.time timeout -s TERM 10800 $PY "${CMD[@]}" > $D/logs/${K}_stdout.log 2>&1; rc=$?
echo "$(stamp) end $C $K exit $rc, $(( $(date +%s) - t0 )) s: $(tail -n 1 $D/logs/${K}_stdout.log | cut -c1-200)" >> $H
[ $rc = 0 ] && [ -s $OUT ] || exit 255
exit 0
