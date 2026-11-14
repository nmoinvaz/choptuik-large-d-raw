#!/bin/bash
# #786 on dh610: uf786.py (I772-dh610's uf688.py with --rows) at #735's 0.80 and 0.92 starts, listing the rows of the
# n3>n4 block that carry r, 4 threads, nice 10, in #772's build (main a879ccc3, hp/ from HP688).
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I786-dh610
B=/home/nathan/scratch786
mkdir -p $B
git -C $RAW fetch -q origin
for f in start_080 start_092; do git -C $RAW show origin/main:I735-dh370/start/$f.npz > $B/$f.npz; done
cd /home/nathan/Source/choptuik-large-d/hp && . /home/nathan/Source/choptuik-large-d/.venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 HP688=/home/nathan/Source/choptuik-large-d/hp
echo "hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD), raw origin/main $(git -C $RAW rev-parse --short=8 origin/main)" > $R/phases.log
for L in 080 092; do
  t=$(date +%s)
  echo "== rows_$L $(date -u '+%F %T') UTC" > $R/rows_$L.log
  nice -n 10 python -u $R/uf786.py $RAW $B/start_$L.npz --out=$R/rows_$L.json --threads=4 '--rows=n3>n4' >> $R/rows_$L.log 2>&1
  echo "rows_$L exit $? wall $(( $(date +%s) - t )) s $(date -u '+%H:%M:%S')" >> $R/phases.log
done
echo "all done $(date -u '+%F %T') UTC" >> $R/phases.log
