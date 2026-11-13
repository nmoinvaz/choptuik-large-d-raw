#!/usr/bin/env bash
# #634's queue from 08:45 UTC at 2 threads: after the 1e-74 perturbations at D 245.14, the variants at D 236.63 and
# 243.64, the 16-order series at D 245.14 (Delta's series for the location there) and the polish to 1e-80
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i634/I634-mac
until grep -q "variants pert:1e-74:1,pert:1e-74:2 D 245.1366" $R/exits_634.txt 2>/dev/null; do sleep 15; done
bash $R/run_634.sh variants:od,pert:1e-74:1,qd 236.6312
bash $R/run_634.sh variants:od,qd 243.6366
bash $R/run16_634.sh 245.1366
bash $R/run_634.sh polish 245.1366
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') queue2 done" >> $R/exits_634.txt
