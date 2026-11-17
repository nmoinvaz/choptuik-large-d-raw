#!/usr/bin/env bash
# #903 q130r (t5, 2026-11-17): the re-planning control at the pilot. ks 130 (the state's own order) with --keep_plan 0
# --steps 0 --save_base 1 from I603-win2/base/base_pin3_D225.1312.npz, chain_nsr's flags with --threads 4 beside the chain,
# nice 10. Worktree choptuik-large-d-xf-903 at main 663e3b2d, venv-314 with the #523 build (i599/site2), as the pilot.
SP=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad
RAW=$SP/raw-wt; O=$SP/i903; PY=/Users/nathan/venv-314/bin/python
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
export PYTHONFAULTHANDLER=1
S=I603-win2/base/base_pin3_D225.1312.npz
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 4 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
cd /Users/nathan/Source/choptuik-large-d-xf-903/hp || exit 9
echo "903 q130r start, main $(git rev-parse --short HEAD) $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $O/exits_903.txt
t=$(date +%s)
nice -n 10 $PY -u anm_run.py $RAW $O/q130r --state $S $F --keep_plan 0 --steps 0 --D_max 226 --save_base 1 --allow_unraw > $O/q130r.log 2>&1
rc=$?
echo "903 q130r exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $O/exits_903.txt
[ -f $O/q130r/base_pin3_D225.1312.npz ] && echo "903 q130r base saved" >> $O/exits_903.txt
