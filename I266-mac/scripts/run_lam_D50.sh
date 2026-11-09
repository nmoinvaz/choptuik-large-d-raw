#!/bin/bash
# lam on the quad-double solutions at D 50 (rounded to double-double), M 32 on its own plan, M 48 on R's plan; then on
# the double-double R state for comparison. From the worktree root.
RAW=/Users/nathan/Source/choptuik-large-d-raw/I266-mac
S=$RAW/states
bash $RAW/scripts/run_cmd.sh lam_D50_M32_qd lam $RAW/lam.jsonl $S/up8_D50.0075_qd.npz --kf=13
bash $RAW/scripts/run_cmd.sh lam_D50_M48_r2_qd lam $RAW/lam.jsonl $S/up8_D50.0075_M48_r2_qd.npz $S/up8_D50.0075_M48_r2.npz \
  --kf=13 --plan=$S/up8_D50.0075_M48_r2.npz
