#!/usr/bin/env bash
# #927: the M 48 pilot after the references (run_chain.sh) end: step 1, the three controls, and step 2 when
# lowD_highM.py reached its second point (its --hours rule may stop it after the first).
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/raw927/I927-mac
while pgrep -f run_chain.sh > /dev/null; do sleep 15; done
echo "pilot chain start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/chain_exits.txt
bash $R/run_pilot.sh step1
bash $R/run_pilot.sh controls
if [ -f $R/ref48/states/lowD927_D3.6900_M48.npz ]; then bash $R/run_pilot.sh step2; fi
echo "pilot chain done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/chain_exits.txt
