#!/bin/bash
# #697 step 1 on dh370: the selftest (planted check and its mutation), then the M = 32 quad-double series to order 300 at D 253.8043, 12 threads, nice 10.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I697-dh370
cd /home/nathan/Source/choptuik-large-d-685/hp && . /home/nathan/Source/choptuik-large-d-614/.venv/bin/activate
export PATH=$HOME/.local/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
echo "hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD)" > $R/phases.log
t=$(date +%s); nice -n 10 python -u horizon_radius.py selftest > $R/selftest.log 2>&1; echo "selftest exit $? wall $(( $(date +%s) - t )) s" >> $R/phases.log
t=$(date +%s); nice -n 10 python -u horizon_radius.py selftest --mutate drop_term > $R/selftest_drop_term.log 2>&1; echo "selftest drop_term exit $? wall $(( $(date +%s) - t )) s" >> $R/phases.log
t=$(date +%s); nice -n 10 python -u horizon_radius.py run $R/long_m32.jsonl $RAW/I603-win2/chain_nat/anm_pin3_D253.8043.npz --kmax 300 --precs qd --threads 12 --coef $R/coef_m32 > $R/long_m32.log 2>&1; echo "run M 32 qd 300 exit $? wall $(( $(date +%s) - t )) s $(date -u '+%F %T')" >> $R/phases.log
