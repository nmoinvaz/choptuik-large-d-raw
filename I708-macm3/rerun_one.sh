#!/bin/bash
# #708 (coordinator's message 1794619159598-0): a kf 35 left circle rerun on its stored evals for the zero positions, with
# modecount_circle.py of main 989e103c (WMAX = 4). Usage: rerun_one.sh NAME CENTRE_RE,CENTRE_IM   e.g. c_2.85_p0.25 2.85,0.25
# The original record stays in kf35/NAME/data. The rerun works on a copy of its evals cache in rerun/NAME/data and
# must add no determinant: the cache's line count after the run is compared with the one before.
# From hp/ of the main checkout (989e103c, modecount_cx built there by modecount_build.sh), nice 10, caffeinate -is.
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw-641/I708-macm3
NAME=$1
CIRCLE=$2,0.36
TAG=D61.0264_M48_kf35_ball320
D=$R/rerun/$NAME/data
mkdir -p $D
cp $R/kf35/$NAME/data/modecount_${TAG}_evals.jsonl $D/
cd /Users/nathan/Source/choptuik-large-d/hp
echo "rerun $NAME start $(date -u '+%Y-%m-%d %H:%M:%S UTC') main $(git rev-parse --short=8 HEAD) cache lines before $(wc -l < $D/modecount_${TAG}_evals.jsonl)" >> $R/rerun/exits_rerun.txt
caffeinate -is nice -n 10 python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz $CIRCLE --M=48 --kf=35 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf35 --ball=320 --threads=1 --data=$D > $R/rerun/$NAME/run.log 2>&1
echo "rerun $NAME exit $? at $(date -u '+%Y-%m-%d %H:%M:%S UTC') cache lines after $(wc -l < $D/modecount_${TAG}_evals.jsonl)" >> $R/rerun/exits_rerun.txt
