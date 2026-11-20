#!/bin/bash
# #966 on dh170: the near_null read of the D 253.3365 ks_chain3b state and the two planted controls, at once, 2 threads each, nice 10 (run949.sh's invocation).
HERE=/home/nathan/Source/choptuik-large-d-raw/I966-dh170
WT=/home/nathan/Source/choptuik-large-d-935
R=/home/nathan/scratch949
PY=$WT/.venv/bin/python
L=$HERE/exits_966.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1
run() {   # name state flags...
  name=$1; state=$2; shift 2; t=$(date +%s)
  echo "966 $name start $(date -u '+%F %T') hp $(git -C $WT rev-parse --short HEAD) $state $*, load $(cut -d' ' -f1-3 /proc/loadavg)" >> $L
  ( cd $WT/hp && nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" $PY -u near_null.py $R $state --k=6 --its=16 --threads=2 --json=$HERE/$name.json "$@" ) > $HERE/$name.log 2>&1
  echo "966 $name exit $? wall $(( $(date +%s) - t )) s $(date -u '+%F %T')" >> $L
}
run c3b_ks293_D253.3365 I966-dh370/ks_chain3b/leg07_D252.8861_ks293/anm_pin3_D253.3365.npz --its=32 &
run ctl_planted I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz --planted=1 &
run ctl_planted_mut I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz --planted=1 --mutate=scale_block &
wait
