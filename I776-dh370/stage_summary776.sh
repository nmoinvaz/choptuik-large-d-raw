#!/bin/bash
# #776: #760's staging with #760's three series and this folder's three added, so that jet_singularity.py summary locates all of them.
# Usage: stage_summary776.sh X   (X an empty directory outside the raw repository)
RAW=/home/nathan/Source/choptuik-large-d-raw
X=$1
mkdir -p $X/I634-mac/repro && ln -s $RAW/I603-win2 $X/I603-win2
for f in $RAW/I634-mac/*; do b=$(basename $f); [ "$b" = repro ] || ln -s $f $X/I634-mac/$b; done
for f in $RAW/I634-mac/repro/*.npz $RAW/I685-dh370/repro/*.npz $RAW/I712-dh370/repro/*.npz $RAW/I760-dh370/repro/*.npz $RAW/I776-dh370/repro/*.npz; do ln -s $f $X/I634-mac/repro/$(basename $f); done
cd /home/nathan/Source/choptuik-large-d-685/hp && . /home/nathan/Source/choptuik-large-d-614/.venv/bin/activate
export PATH=$HOME/.local/bin:$PATH OPENBLAS_NUM_THREADS=1
nice -n 10 python -u jet_singularity.py summary $X --out $RAW/I776-dh370/jet_776.json --D_max 245.5 --D_beyond 260 > $RAW/I776-dh370/summary776.log 2>&1
echo "exit $?" >> $RAW/I776-dh370/summary776.log
PY=/home/nathan/Source/choptuik-large-d-614/.venv/bin/python
$PY -I $RAW/I685-dh370/table685.py $RAW/I776-dh370/jet_776.json --out $RAW/I776-dh370/table776.txt
$PY -I $RAW/I776-dh370/report776.py $RAW/I776-dh370/jet_776.json $RAW/I760-dh370/jet_760.json --out $RAW/I776-dh370/report776.txt
# the series against #603's records (bar 1) and its control, which #712's staging left out
$PY -I $RAW/I776-dh370/repro_check776.py $RAW /home/nathan/scratch776/chain_nsr_records.jsonl > $RAW/I776-dh370/repro_check776.txt 2>&1; echo "exit $?" >> $RAW/I776-dh370/repro_check776.txt
$PY -I $RAW/I776-dh370/repro_check776.py $RAW /home/nathan/scratch776/chain_nsr_records.jsonl --control > $RAW/I776-dh370/repro_check776_control.txt 2>&1; echo "exit $?" >> $RAW/I776-dh370/repro_check776_control.txt
