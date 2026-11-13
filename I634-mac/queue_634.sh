#!/usr/bin/env bash
# #634's queue on the Mac, ordered for a machine loaded 30-70 by other runs (a 24-order octo-double series takes about
# 1.5 h here): after the first reproduction (D 236.63), the variants at D 245.14, its 24-order series, the reduced
# variants at D 236.63 and 243.64, the polish at D 245.14, then 24-order series for the re-expansion check and the
# step-by-step location as time allows
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i634/I634-mac
until grep -q "^done\|Traceback" $R/repro_D236.6312.log; do sleep 15; done
bash $R/run_634.sh variants 245.1366
bash $R/run_634.sh n24 245.1366
bash $R/run_634.sh variants3 236.6312 243.6366
bash $R/run_634.sh polish 245.1366
bash $R/run_634.sh n24 244.6366 243.6366 225.1312 240.1244
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') queue done" >> $R/exits_634.txt
