#!/bin/bash
# Usage: run.sh PROOF_COPY_DIR PYTHON
raw=$(cd "$(dirname "$0")/.." && pwd)
cd "$1" || exit 2
start=$(date -u '+%Y-%m-%d %H:%M:%S')
caffeinate -is nice -n 10 "$2" -u lemma6_jump_M.py --M=5 --box="$raw/I36-macm3/A_M2_6a_M5_sub1e-14.json" --rp=0.08 --k=20 --verbose --save-B="$raw/I371-macm3/B_M5_sub1e-14_verbose.json" --json="$raw/I371-macm3/lemma6a_M5_sub1e-14_verbose.json" > "$raw/I371-macm3/lemma6a_M5_sub1e-14_verbose.log" 2>&1
echo "lemma6a verbose exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> "$raw/I371-macm3/exits.txt"
