#!/bin/bash
# #772 on dh610: #688's u_1^T r by residual block (uf688.py, with hp/ taken from HP688) at #735's two re-noded starts,
# the 0.80 and 0.92 layouts, then the --mutate=shift control at 0.80. 4 threads (the #608 chains hold the other 16), nice 10.
# The starts are taken from origin/main into ~/scratch772, so the live raw clone is not pulled.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I772-dh610
B=/home/nathan/scratch772
mkdir -p $B
git -C $RAW fetch -q origin
for f in start_080 start_092; do git -C $RAW show origin/main:I735-dh370/start/$f.npz > $B/$f.npz; done
cd /home/nathan/Source/choptuik-large-d/hp && . /home/nathan/Source/choptuik-large-d/.venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 HP688=/home/nathan/Source/choptuik-large-d/hp
echo "hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD), raw origin/main $(git -C $RAW rev-parse --short=8 origin/main)" > $R/phases.log
run() {  # name state extra...
  local name=$1 st=$2; shift 2
  local t=$(date +%s)
  echo "== $name $(date -u '+%F %T') UTC" > $R/$name.log
  nice -n 10 python -u $R/uf688.py $RAW $st --out=$R/$name.json --threads=4 "$@" >> $R/$name.log 2>&1
  echo "$name exit $? wall $(( $(date +%s) - t )) s $(date -u '+%H:%M:%S')" >> $R/phases.log
}
run uf_080 $B/start_080.npz
run uf_092 $B/start_092.npz
run uf_080_mutate_shift $B/start_080.npz --mutate=shift
echo "all done $(date -u '+%F %T') UTC" >> $R/phases.log
