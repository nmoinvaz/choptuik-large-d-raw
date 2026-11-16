#!/usr/bin/env bash
# #903 (the coordinator's comment of 2026-11-16 13:16 UTC): after the D 225.13 ladder, a chain at a fixed horizon order from the
# highest converged rung's saved base toward the fold: anm_run.py with chain_nsr's flags F, 8 threads, nice 10, --ks <rung>
# --steps 400 --D_max 262. The rung is 146 when its polish converged (max|F| <= 1e-60, base saved), else 142. Output to the
# scratchpad (--allow_unraw), copied into raw I903-mac/chain_fixed for commits. Worktree choptuik-large-d-xf-903 at main
# 663e3b2d, venv-314 with the #523 build (i599/site2).
SP=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad
RAW=$SP/raw-wt
O=$SP/i903
PY=/Users/nathan/venv-314/bin/python
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
export PYTHONFAULTHANDLER=1
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 8 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
cd /Users/nathan/Source/choptuik-large-d-xf-903/hp || exit 9
ok_rung() {
  [ -f "$2" ] || return 1
  l=$(grep -E "octo-double Newton: [0-9]+ steps" "$1" | tail -n 1)
  echo "$l" | grep -q ", converged" || return 1
  echo "$l" | grep -q "not converged" && return 1
  f=$(echo "$l" | sed -E 's/.*max\|F\| ([0-9.e+-]+),.*/\1/')
  $PY -c "import sys; sys.exit(0 if float('$f') <= 1e-60 else 1)"
}
if ok_rung $O/ladder/k146_from142.log $O/ladder/k146_from142/base_pin3_D225.1312.npz; then K=146; B=$O/ladder/k146_from142/base_pin3_D225.1312.npz
else K=142; B=$O/ladder/k142_from140/base_pin3_D225.1312.npz; fi
echo "903C chain_fixed start $(date -u '+%Y-%m-%d %H:%M:%S UTC') ks $K from $B, main $(git rev-parse --short HEAD)" >> $O/exits_chain.txt
t=$(date +%s)
nice -n 10 $PY -u anm_run.py $RAW $O/chain_fixed --state $B $F --ks $K --steps 400 --D_max 262 --allow_unraw > $O/chain_fixed.log 2>&1
echo "903C chain_fixed exit $? wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $O/exits_chain.txt
