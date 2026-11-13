#!/bin/bash
# #712: the staging of I685-dh370/stage_summary685.sh with this folder's three series added to #685's five and I634-mac's, so that jet_singularity.py summary locates all of them.
# Usage: stage_summary712.sh X   (X an empty directory outside the raw repository)
RAW=/home/nathan/Source/choptuik-large-d-raw
X=$1
mkdir -p $X/I634-mac/repro && ln -s $RAW/I603-win2 $X/I603-win2
for f in $RAW/I634-mac/*; do b=$(basename $f); [ "$b" = repro ] || ln -s $f $X/I634-mac/$b; done
for f in $RAW/I634-mac/repro/*.npz $RAW/I685-dh370/repro/*.npz $RAW/I712-dh370/repro/*.npz; do ln -s $f $X/I634-mac/repro/$(basename $f); done
cd /home/nathan/Source/choptuik-large-d-685/hp && . /home/nathan/Source/choptuik-large-d-614/.venv/bin/activate
export PATH=$HOME/.local/bin:$PATH OPENBLAS_NUM_THREADS=1
nice -n 10 python -u jet_singularity.py summary $X --out $RAW/I712-dh370/jet_712.json --D_max 245.5 --D_beyond 257 > $RAW/I712-dh370/summary712.log 2>&1
echo "exit $?" >> $RAW/I712-dh370/summary712.log
PY=/home/nathan/Source/choptuik-large-d-614/.venv/bin/python
$PY -I $RAW/I685-dh370/table685.py $RAW/I712-dh370/jet_712.json --out $RAW/I712-dh370/table712.txt
$PY -I $RAW/I712-dh370/report712.py $RAW/I712-dh370/jet_712.json $RAW/I685-dh370/jet_685.json --out $RAW/I712-dh370/report712.txt
