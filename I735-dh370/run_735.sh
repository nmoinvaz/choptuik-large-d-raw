#!/bin/bash
# #735: #603's D 252.2497 state on two other layouts, last node 0.80 and 0.92 (nodes 0.3,0.4,0.5,0.6,L, the convention of
# #543, #553 and #654), each with the renode control, the base polish, and where the polish converges below 1e-60 the
# 24-order series (#712's flags) and its singularity by jet_singularity.py locate, beside the same locate of #685's
# series at the 0.70 layout from the same state. dh370, worktree choptuik-large-d-685 (main f40deb4a, #712's) in the venv
# of choptuik-large-d-614 (the 3c35f0c build), 12 threads, nice 10.
# The polish uses #603's corrector flags with --elim_switch 0 (every point projected), since #654's polish at 0.975 on
# the default switch crawled at lam 1/2 to 3.8e-20, the signature #710 traced to the projection switch.
# usage: run_735.sh 080 092
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I735-dh370
S=I603-win2/chain/anm_pin3_D252.2497.npz
cd /home/nathan/Source/choptuik-large-d-685/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "f40deb4a" ] || { echo "worktree is not at f40deb4a" >&2; exit 9; }
. /home/nathan/Source/choptuik-large-d-614/.venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "$1 $(date -u '+%F %T') UTC" >> $R/exits_735.txt; }
converged() { grep -E "octo-double Newton: [0-9]+ steps" "$1" | tail -n 1 | grep -q ", converged"; }
COM="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --D_max 400 --threads 12 --corrector od --tol_od 1e-60 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred"
mkdir -p $R/start
log "735 hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD)"
nice -n 10 python -u jet_singularity.py locate $RAW/I685-dh370/repro/jet_pin3_D252.2497.npz --json $R/locate_070.json > $R/locate_070.log 2>&1
log "735 locate 070 (#685's series) exit $? (must be 0)"
for L in "$@"; do
  x=0.${L:1}
  nice -n 10 python -u renode_o.py $RAW $S I735-dh370/start/start_$L.npz --nodes 0.3,0.4,0.5,0.6,$x --threads 12 > $R/start/renode_$L.log 2>&1
  log "735 renode $L exit $? (must be 0)"
  nice -n 10 python -u renode_o.py $RAW $S I735-dh370/start/ctl_sign_$L.npz --nodes 0.3,0.4,0.5,0.6,$x --threads 12 --mutate sign > $R/start/ctl_sign_$L.log 2>&1
  log "735 renode $L --mutate sign exit $? (must be 1)"
  [ -f $R/start/start_$L.npz ] || { log "735 $L no start, stops"; continue; }
  mkdir -p $R/base_$L
  nice -n 10 python -u anm_run.py $RAW $R/base_$L --state I735-dh370/start/start_$L.npz --steps 0 --save_base 1 --tol 1e-30 --qd_it 12 $COM --elim_switch 0 > $R/base_$L.log 2>&1
  log "735 polish $L exit $? converged: $(converged $R/base_$L.log && echo yes || echo NO)"
  B=$(ls $R/base_$L/base_pin3_D*.npz 2>/dev/null | head -n 1)
  if ! converged $R/base_$L.log || [ -z "$B" ]; then log "735 $L polish not converged or no base, no series"; continue; fi
  mkdir -p $R/series_$L
  nice -n 10 python -u anm_run.py $RAW $R/series_$L --state I735-dh370/base_$L/$(basename $B) --steps 1 --qd_it 20 $COM --save_jet 2 > $R/series_$L.log 2>&1
  log "735 series $L exit $?"
  J=$(ls $R/series_$L/jet_pin3_D*.npz 2>/dev/null | head -n 1)
  [ -n "$J" ] || { log "735 $L no jet saved"; continue; }
  nice -n 10 python -u jet_singularity.py locate $J --json $R/locate_$L.json > $R/locate_$L.log 2>&1
  log "735 locate $L exit $? (must be 0)"
done
log "735 all done"
