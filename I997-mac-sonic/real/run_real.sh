#!/bin/bash
{
# #997 (b) real test: hp's D 3.045 M 320 state, band 0.01 -> 0.02 warped (eps0 2e-3), chord from one LU, down to D 3.04
cd /Users/nathan/Source/choptuik-lowd-sonic/solver/lowd_sonic
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1043/site
OUT=/Users/nathan/Source/raw-i997-live/I997-mac-sonic/real
date -u '+start %Y-%m-%d %H:%M:%S UTC'
nice -n 10 /Users/nathan/venv-314/bin/python hybrid.py $OUT/real.jsonl --state /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/sonic/states/lowDhm_x0.000157-0.975_D3.0450_M320.npz \
  --history /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/sonic/states/lowDhm_x0.000157-0.975_D3.0438_M320.npz,/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/sonic/states/lowD343_D3.0436_M320.npz,/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/sonic/states/lowD343_D3.043350_M320.npz,/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/sonic/states/lowD343_D3.043150_M320.npz \
  --drop_nodes 0.000313,0.16,0.3,0.5,0.7,0.9 --Ds 3.045,3.04375,3.04335,3.04315,3.0430,3.0428,3.0425,3.042,3.041,3.040 \
  --warp design --eps0 2e-3 --kappa 1.0 --tol 1e-12 --it_max 60 --threads 4 --jac wood --aa_m 4 --split 2 --split_near 4 --band_jac $OUT/states/band_jac_D3.045_M320.npy --save $OUT/states --time_cap 14400 \
  --expect 3.045:2.4464747274661773:1e-8,3.04375:2.436459113272686:1e-8,3.04335:2.4332179889888024:1e-8,3.04315:2.431590741783993:1e-8
echo "exit $?"
date -u '+end %Y-%m-%d %H:%M:%S UTC'
exit
}
