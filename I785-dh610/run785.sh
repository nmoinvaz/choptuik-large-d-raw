#!/bin/bash
# #785 on dh610: #688's uf688.py (I772-dh610's copy, hp/ from HP688) at #688's 0.975 start, 4 threads, nice 10, in the
# build of #772 (main a879ccc3), then share785.py over this log and #772's two.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I785-dh610
B=/home/nathan/scratch785
mkdir -p $B
git -C $RAW fetch -q origin
git -C $RAW show origin/main:I654-dh370/start/start_0975.npz > $B/start_0975.npz
for f in uf_080.log uf_092.log; do git -C $RAW show origin/main:I772-dh610/$f > $B/$f; done
git -C $RAW show origin/main:I688-dh370/uf_horizon.log > $B/uf_horizon_688.log
cd /home/nathan/Source/choptuik-large-d/hp && . /home/nathan/Source/choptuik-large-d/.venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 HP688=/home/nathan/Source/choptuik-large-d/hp
echo "hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD), raw origin/main $(git -C $RAW rev-parse --short=8 origin/main)" > $R/phases.log
git -C $RAW show origin/main:I772-dh610/uf688.py > $B/uf688.py
t=$(date +%s)
echo "== uf_0975 $(date -u '+%F %T') UTC" > $R/uf_0975.log
nice -n 10 python -u $B/uf688.py $RAW $B/start_0975.npz --out=$R/uf_0975.json --threads=4 >> $R/uf_0975.log 2>&1
echo "uf_0975 exit $? wall $(( $(date +%s) - t )) s $(date -u '+%H:%M:%S')" >> $R/phases.log
python -I $R/share785.py $R/uf_0975.log $B/uf_080.log $B/uf_092.log --ref688 $B/uf_horizon_688.log > $R/share785.txt 2>&1
echo "share exit $?" >> $R/phases.log
echo "all done $(date -u '+%F %T') UTC" >> $R/phases.log
