#!/bin/bash
# form S jumps on this machine (#1088): run_jump.sh D DMAX DEG JUNK LS THREADS TAG [extra jump options]
# the guess from the chain states with D 226 .. DMAX in raw/, kfreeze 13, ks by the sigma rule, plan 1e-40, octo-double
{
W=/home/nathan/Source/choptuik-large-d-1088a
D=$1; DMAX=$2; DEG=$3; JUNK=$4; LS=$5; THR=$6; TAG=$7; shift 7
cd $W/hp || exit 1
PY=$(cat $W/python_path)
export PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2
OUT=$W/out/j${D}_$TAG
mkdir -p $OUT
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $OUT/run.log
echo "run_jump.sh $D $DMAX $DEG $JUNK $LS $THR $TAG $*" >> $OUT/run.log
$PY -u form_s.py jump $OUT --D $D --states "$W/raw/I903-macm3/chain_k135/anm_pin3_D*.npz,$W/raw/I966-dh370/ks_chain3b/*/anm_pin3_D*.npz" \
  --Dmin 226 --Dmax $DMAX --deg $DEG --kfreeze 13 --plan_tol 1e-40 --ks sigma --tol 1e-40 --it_max 12 --threads $THR \
  --junk $JUNK --ls $LS "$@" --allow_unraw > $OUT/jump.log 2>&1
echo "rc $?" >> $OUT/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $OUT/run.log
exit
}
