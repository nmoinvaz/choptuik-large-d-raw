#!/usr/bin/env bash
# #603: the chain_fit chain rerun on main's exact freeze projector from D 225.13 (crawlJ's flags), on the build #600 checked (fat LTO, venv-i600, hpkernel sha256 4ede9afe..., main fc697f3a).
# Start: #595's exact-rows base I595-mac/polish_c2_s225/base_pin3_D225.1312.npz (raw 2b818f6f), copied to I603-win2/base/ because the live clone is not pulled. 9 threads.
# Control: at D 235.13125 the chain's Delta must lie 3.5313e-12 below the table's crawlI row (1.687523233741265 + 2.521580451291125e-17 - 8.82e-34 ...), within 1e-14.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I603-win2
S=I603-win2/base/base_pin3_D225.1312.npz
cd /d/choptuik-i600/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "fc697f3a" ] || { echo "worktree D:/choptuik-i600 is not at fc697f3a" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "603 chain start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits_603.txt
"$PY" -u anm_run.py $RAW $R/chain --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 1.0 --steps 400 --D_max 400 --threads 9 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 > $R/chain.log 2>&1
rc=$?
echo "603 chain anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_603.txt
