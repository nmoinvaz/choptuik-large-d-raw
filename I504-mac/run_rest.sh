#!/usr/bin/env bash
# #504: what run_all.sh had left after run C. The full run D was stopped after 3 trials (pD_raw_unmoved_stopped.log):
# with S unmoved its raw test halves every step, so 12 steps cost about 24 trials without converging. D is run again
# for one step, which is where its sequence leaves A's. Then the verdict, the 0.3-0.8 polish, the code before
# scale_c and its comparisons. Usage: run_rest.sh WORKTREE_HP OUTRAW STATERAW OLD_OCTO_CORRECTOR
HP=$1
OUT=$2
SR=$3
OLD=$4
R=$OUT/I504-mac
ST=T129-win2/chain/anm_pin3_D180.5246.npz
"$R/run_eq.sh" "$HP" "$OUT" pD_raw_unmoved planted "$SR" "$ST" --test raw --S unmoved --it_max 1 --out "$R/pD_raw_unmoved"
"$R/run_eq.sh" "$HP" "$OUT" verdict verdict "$R/pA_raw" "$R/pB_eq" "$R/pC_eq_unmoved" "$R/pD_raw_unmoved"
"$R/run_polish_eq.sh" "$HP" "$OUT" I489-mac/renode_L1_horizon_D242.3642.npz polish_eq
"$R/run_eq.sh" "$HP" "$OUT" pA_old planted "$SR" "$ST" --test raw --newton_from "$OLD" --out "$R/pA_old"
"$R/run_eq.sh" "$HP" "$OUT" same_A same "$R/pA_raw" "$R/pA_old"
"$R/run_eq.sh" "$HP" "$OUT" same_A_ctl same "$R/pA_raw" "$R/pA_old" --mutate_bit 1
