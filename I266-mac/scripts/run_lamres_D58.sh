#!/bin/bash
# The root's jitter at D 58 under noise at the double-double rounding level (relative 1e-32), on both quad-double
# solutions, M 48 (R's plan) and M 32: the yardstick for lam(48) - lam(32) there. From the worktree root.
RAW=/Users/nathan/Source/choptuik-large-d-raw/I266-mac
S=$RAW/states
bash $RAW/scripts/run_cmd.sh lamres_D58_M48_qd lamres $RAW/lamres.jsonl $S/up12_D58.0060_M48_r2_qd.npz \
  --base=2.0455297614778805 --h=2e-13 --eps=1e-32 --n=3 --seed=1 --kf=13 --plan=$S/up12_D58.0060_M48_r2.npz
bash $RAW/scripts/run_cmd.sh lamres_D58_M32_qd_1e-32 lamres $RAW/lamres.jsonl $S/up12_D58.0060_qd.npz \
  --base=2.045529761477791 --h=2e-13 --eps=1e-32 --n=3 --seed=1 --kf=13
