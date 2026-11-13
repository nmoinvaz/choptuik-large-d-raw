#!/bin/bash
cd /Users/nathan/Source/choptuik-large-d/hp
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i523/site_c3
{ echo "== $(date -u '+%Y-%m-%d %H:%M:%S') tangent from the dd state up8_D50.0075"; /usr/bin/time -l nice -n 10 /Users/nathan/venv-314/bin/python3 -u scan_qd.py /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i611/I611-mac/diag/qd_diag_dd.jsonl data/states/up8_D50.0075.npz 50.017491 --kfreeze 13 --threads 3 --tag diag_dd --predictor tangent --dD 0.01 2>&1; echo "exit $?"; } > /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i611/I611-mac/diag/diag_dd.stdout 2>&1
