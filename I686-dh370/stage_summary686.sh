#!/bin/bash
# #686: the same staging as I685-dh370/stage_summary685.sh, with this folder's new-plan series (newplan/) as the bases.
# Usage: stage_summary686.sh X   (X an empty directory outside the raw repository)
RAW=/home/nathan/Source/choptuik-large-d-raw
X=$1
mkdir -p $X/I634-mac/repro && ln -s $RAW/I603-win2 $X/I603-win2
for f in $RAW/I634-mac/*; do b=$(basename $f); [ "$b" = repro ] || ln -s $f $X/I634-mac/$b; done
for f in $RAW/I686-dh370/newplan/*.npz; do ln -s $f $X/I634-mac/repro/$(basename $f); done
cd /home/nathan/Source/choptuik-large-d-685/hp && . /home/nathan/Source/choptuik-large-d-614/.venv/bin/activate
export PATH=$HOME/.local/bin:$PATH OPENBLAS_NUM_THREADS=1
nice -n 10 python -u jet_singularity.py summary $X --out $RAW/I686-dh370/jet_686.json --D_max 245.5 --D_beyond 254 > $RAW/I686-dh370/summary686.log 2>&1
echo "exit $?" >> $RAW/I686-dh370/summary686.log
/home/nathan/Source/choptuik-large-d-614/.venv/bin/python -I $RAW/I686-dh370/compare686.py $RAW/I685-dh370/jet_685.json $RAW/I686-dh370/jet_686.json --out $RAW/I686-dh370/compare686.txt
