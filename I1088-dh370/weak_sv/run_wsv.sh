#!/bin/bash
{
cd /home/nathan/Source/choptuik-large-d-1088a/work
export OPENBLAS_NUM_THREADS=2
PY=/home/nathan/Source/choptuik-large-d-1082/.venv/bin/python
date -u "+start %Y-%m-%d %H:%M:%S UTC"
for D in 245.5586 254.5903 263.5987; do
  timeout 3600 $PY -u weak_sv.py anm_pin3_D$D.npz 6 13 10 6 > weak_sv_k13_D$D.log 2>&1
done
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
