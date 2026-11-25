#!/bin/bash
# the two-stage hybrid's second stage (#1088; form_s_hybrid.py): the old layout (nodes 0.3 ... 0.7, the Moebius series
# summed at 0.7, ks 1.5 n + 20, kc 250) solved by held Newton from a fine-mesh state's m_h (node 0.7 the series' sum),
# after the release build with path_s (unit i1088a-buildfine); run_hybrid.sh FINE_STATE OUTNAME TC; 10 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
while systemctl --user is-active --quiet i1088a-buildfine; do sleep 30; done
bash $W/update_py.sh > /dev/null
test -s $W/hp/form_s_hybrid.py || exit 1
cd $W/hp || exit 1
mkdir -p $W/out/$2
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $W/out/$2/run.log
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2 $(cat $W/python_path) -u form_s_hybrid.py $1 $W/out/$2 --mob 8 --kc 250 \
  --threads 10 --tc $3 --commit 441afd90 --allow_unraw > $W/out/$2/hybrid.log 2>&1
echo "rc $?" >> $W/out/$2/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $W/out/$2/run.log
exit
}
