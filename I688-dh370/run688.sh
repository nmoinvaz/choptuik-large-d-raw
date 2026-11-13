#!/bin/bash
# #688 on dh370: u_1^T r by residual block (uf688.py) at the three 0.975 starts and at S, then the --mutate=shift control, 12 threads, nice 10.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I688-dh370
cd /home/nathan/Source/choptuik-large-d-685/hp && . /home/nathan/Source/choptuik-large-d-614/.venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
echo "hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD)" > $R/phases.log
run() {  # name state extra...
  local name=$1 st=$2; shift 2
  local t=$(date +%s)
  echo "== $name $(date -u '+%F %T') UTC" > $R/$name.log
  nice -n 10 python -u $R/uf688.py $RAW $st --out=$R/$name.json --threads=12 "$@" >> $R/$name.log 2>&1
  echo "$name exit $? wall $(( $(date +%s) - t )) s $(date -u '+%H:%M:%S')" >> $R/phases.log
}
run uf_horizon I654-dh370/start/start_0975.npz
run uf_integrate I673-dh370/start_integrate.npz
run uf_f64 I673-dh370/start_f64.npz
run uf_070 I603-win2/chain/anm_pin3_D252.2497.npz
run uf_horizon_mutate_shift I654-dh370/start/start_0975.npz --mutate=shift
echo "all done $(date -u '+%F %T') UTC" >> $R/phases.log
