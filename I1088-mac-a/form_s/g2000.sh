#!/bin/bash
# the D 2000 guess's residual per block with the Moebius horizon (a 8, ks 1.5 n + 20, kc 250) for two fits: A the 50
# chain states (D 226-252.5) at degree 2 in 1/n, B those and the form-S states at D 250 (held), 300 (released) and 400
# (held) at degree 2; jump with --it_max 0 (no Newton), on this Mac's opt-1 build, 2 threads
{
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i1088a/raw
O=/Users/nathan/Source/choptuik-large-d-raw-1088a
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp || exit 1
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i1088a/site_m OPENBLAS_NUM_THREADS=2
SS="$O/I1088-mac-a/form_s/j250_held/jump_s_D250.0000.npz,$O/I1088-dh610/out/rls300/release_ls_h13_D300.0000.npz,$O/I1088-dh610/j400_held/jump_s_D400.0000.npz"
for v in B A; do
  if [ $v = B ]; then X="--states_s $SS"; else X=""; fi
  nice -n 10 /Users/nathan/venv-314/bin/python -u form_s.py jump $O/I1088-mac-a/form_s/g2000_$v --D 2000 \
    --states "$R/I903-macm3/chain_k135/anm_pin3_D*.npz,$R/I966-dh370/ks_chain3b/*/anm_pin3_D*.npz" --Dmin 226 --Dmax 252.5 \
    --deg 2 --kfreeze 13 --plan_tol 1e-40 --ks sigma --kc 250 --mob 8 --it_max 0 --threads 2 --delta 1.649074313886 \
    $X > $O/I1088-mac-a/form_s/g2000_$v.log 2>&1
done
exit
}
