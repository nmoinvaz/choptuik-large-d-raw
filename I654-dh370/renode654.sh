#!/bin/bash
# #654 step 1: renode #603's newest converged state (D 252.2497) to the nodes 0.3,0.4,0.5,0.6,0.975, then the --mutate sign control (must exit 1).
# dh370, worktree choptuik-large-d-654 (main 37c7955c) in the venv of choptuik-large-d-614 (the 3c35f0c build), 12 threads, nice 10.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I654-dh370
S=I603-win2/chain/anm_pin3_D252.2497.npz
cd /home/nathan/Source/choptuik-large-d-654/hp && . /home/nathan/Source/choptuik-large-d-614/.venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
echo "hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD)" > $R/start/renode.log
t=$(date +%s)
echo "== renode $(date -u '+%F %T') UTC" >> $R/start/renode.log
nice -n 10 python -u renode_o.py $RAW $S I654-dh370/start/start_0975.npz --nodes 0.3,0.4,0.5,0.6,0.975 --threads 12 >> $R/start/renode.log 2>&1
echo "exit $? wall $(( $(date +%s) - t )) s" >> $R/start/renode.log
t=$(date +%s)
echo "== control --mutate sign $(date -u '+%F %T') UTC" > $R/start/ctl_sign.log
nice -n 10 python -u renode_o.py $RAW $S I654-dh370/start/ctl_sign.npz --nodes 0.3,0.4,0.5,0.6,0.975 --threads 12 --mutate sign >> $R/start/ctl_sign.log 2>&1
echo "exit $? wall $(( $(date +%s) - t )) s" >> $R/start/ctl_sign.log
echo "renode done $(date -u '+%H:%M')" > $R/start/renode_done.txt
