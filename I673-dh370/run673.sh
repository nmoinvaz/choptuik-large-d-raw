#!/bin/bash
# #673 on dh370: (1) near_null at the unpolished 0.975 start of #654 and at S (D 252.2497), then the --mutate=sigma control (must fail);
# (2) renode S with --last integrate and --last f64, each with its --mutate sign control (must exit 1), then a three-step base polish (--qd_it 3) of each.
# Worktree choptuik-large-d-654 (main 37c7955c) in the venv of choptuik-large-d-614 (the 3c35f0c build), 12 threads, nice 10.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I673-dh370
S=I603-win2/chain/anm_pin3_D252.2497.npz
cd /home/nathan/Source/choptuik-large-d-654/hp && . /home/nathan/Source/choptuik-large-d-614/.venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
echo "hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD)" > $R/phases.log
run() {  # name, command...
  local name=$1; shift
  local t=$(date +%s)
  echo "== $name $(date -u '+%F %T') UTC: $*" > $R/$name.log
  nice -n 10 "$@" >> $R/$name.log 2>&1
  local rc=$?
  echo "exit $rc wall $(( $(date +%s) - t )) s" >> $R/$name.log
  echo "$name exit $rc $(date -u '+%H:%M:%S')" >> $R/phases.log
}
run nn_0975 python -u near_null.py $RAW I654-dh370/start/start_0975.npz --k=4 --threads=12 --json=$R/nn_0975.json
run nn_070 python -u near_null.py $RAW $S --k=4 --threads=12 --json=$R/nn_070.json
run nn_0975_mutate_sigma python -u near_null.py $RAW I654-dh370/start/start_0975.npz --k=4 --threads=12 --mutate=sigma --json=$R/nn_0975_mutate_sigma.json
for rule in integrate f64; do
  run renode_$rule python -u renode_o.py $RAW $S I673-dh370/start_$rule.npz --nodes 0.3,0.4,0.5,0.6,0.975 --last $rule --threads 12
  run renode_${rule}_ctl_sign python -u renode_o.py $RAW $S I673-dh370/ctl_sign_$rule.npz --nodes 0.3,0.4,0.5,0.6,0.975 --last $rule --threads 12 --mutate sign
  mkdir -p $R/base_$rule
  run polish_$rule python -u anm_run.py $RAW $R/base_$rule --state I673-dh370/start_$rule.npz --steps 0 --save_base 1 --tol 1e-30 --qd_it 3 \
     --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --D_max 400 --threads 12 --corrector od --tol_od 1e-60 \
     --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1
done
echo "all done $(date -u '+%F %T') UTC" >> $R/phases.log
