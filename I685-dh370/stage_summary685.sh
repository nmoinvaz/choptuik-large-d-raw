#!/bin/bash
# #685: jet_singularity.py summary reads only RAW/I634-mac/repro (and RAW/I603-win2/chain), so a scratch root X holds links to I634-mac's files
# (its series at D 236.63 among them) and to this folder's repro/ series, and summary is pointed at X. No code was changed.
# Usage: stage_summary685.sh X   (X an empty directory outside the raw repository)
RAW=/home/nathan/Source/choptuik-large-d-raw
X=$1
mkdir -p $X/I634-mac/repro && ln -s $RAW/I603-win2 $X/I603-win2
for f in $RAW/I634-mac/*; do b=$(basename $f); [ "$b" = repro ] || ln -s $f $X/I634-mac/$b; done
for f in $RAW/I634-mac/repro/*.npz $RAW/I685-dh370/repro/*.npz; do ln -s $f $X/I634-mac/repro/$(basename $f); done
cd /home/nathan/Source/choptuik-large-d-685/hp && . /home/nathan/Source/choptuik-large-d-614/.venv/bin/activate
export PATH=$HOME/.local/bin:$PATH OPENBLAS_NUM_THREADS=1
nice -n 10 python -u jet_singularity.py summary $X --out $RAW/I685-dh370/jet_685.json --D_max 245.5 --D_beyond 254 > $RAW/I685-dh370/summary685.log 2>&1
echo "exit $?" >> $RAW/I685-dh370/summary685.log
/home/nathan/Source/choptuik-large-d-614/.venv/bin/python -I $RAW/I685-dh370/table685.py $RAW/I685-dh370/jet_685.json --out $RAW/I685-dh370/table685.txt
