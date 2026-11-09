#!/bin/bash
# lam on the M 32 states, each on its own plan: D 58's quad-double solution and saved double-double state, and D 50's
# saved double-double state (its quad-double solution is in run_lam_D50.sh). From the worktree root.
RAW=/Users/nathan/Source/choptuik-large-d-raw/I266-mac
S=$RAW/states
bash $RAW/scripts/run_cmd.sh lam_D58_M32 lam $RAW/lam.jsonl $S/up12_D58.0060_qd.npz hp/data/states/up12_D58.0060.npz --kf=13
bash $RAW/scripts/run_cmd.sh lam_D50_M32_dd lam $RAW/lam.jsonl hp/data/states/up8_D50.0075.npz --kf=13
