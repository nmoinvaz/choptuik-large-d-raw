#!/usr/bin/env bash
# #504: the planted runs B, C, D, the bit-identity run of the code before scale_c, then the 0.3-0.8 polish, one after
# the other (one heavy process at a time). Usage: run_all.sh WORKTREE_HP OUTRAW STATERAW OLD_OCTO_CORRECTOR
HP=$1
OUT=$2
SR=$3
OLD=$4
R=$OUT/I504-mac
ST=T129-win2/chain/anm_pin3_D180.5246.npz
J0=$R/J0_D180.5246_start.npz
"$R/run_eq.sh" "$HP" "$OUT" pB_eq planted "$SR" "$ST" --test eq --J0 "$J0" --out "$R/pB_eq"
"$R/run_eq.sh" "$HP" "$OUT" pC_eq_unmoved planted "$SR" "$ST" --test eq --S unmoved --J0 "$J0" --out "$R/pC_eq_unmoved"
"$R/run_eq.sh" "$HP" "$OUT" pD_raw_unmoved planted "$SR" "$ST" --test raw --S unmoved --out "$R/pD_raw_unmoved"
"$R/run_eq.sh" "$HP" "$OUT" verdict verdict "$R/pA_raw" "$R/pB_eq" "$R/pC_eq_unmoved" "$R/pD_raw_unmoved"
"$R/run_eq.sh" "$HP" "$OUT" pA_old planted "$SR" "$ST" --test raw --newton_from "$OLD" --out "$R/pA_old"
"$R/run_eq.sh" "$HP" "$OUT" same_A same "$R/pA_raw" "$R/pA_old"
"$R/run_eq.sh" "$HP" "$OUT" same_A_ctl same "$R/pA_raw" "$R/pA_old" --mutate_bit 1
"$R/run_polish_eq.sh" "$HP" "$OUT" I489-mac/renode_L1_horizon_D242.3642.npz polish_eq
