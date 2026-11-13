#!/usr/bin/env bash
# #634's queue on the Mac at 2 threads (the coordinator's cap from 07:39 UTC). After the variants at D 245.14: the base
# perturbed at its convergence level there (J^-1 r with max|r| 1e-74, whose residual is about 1e-60; at 1e-60 the
# residual was 1.6e-32), two seeds; D 236.63 (od, which must equal the first 8 orders of the 24-order series, the base
# perturbed at 1e-74, the quad-double series); D 243.64 (od and the quad-double series); then the 24-order series at
# D 245.14 and the polish as time allows
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i634/I634-mac
until grep -q "variants od,pert:1e-60:1,qd,inject:1e-80:1 D 245.1366" $R/exits_634.txt 2>/dev/null; do sleep 15; done
bash $R/run_634.sh variants:pert:1e-74:1,pert:1e-74:2 245.1366
bash $R/run_634.sh variants:od,pert:1e-74:1,qd 236.6312
bash $R/run_634.sh variants:od,qd 243.6366
bash $R/run_634.sh n24 245.1366
bash $R/run_634.sh polish 245.1366
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') queue done" >> $R/exits_634.txt
