#!/bin/bash
# #1025 macm3 (t5, hc 25 Nov 01:0x UTC): the in-between states D 22.15625 and D 22.1875 of part b2, one after the other, the chord of D 22.125 (rescan root 0.490845) and D 22.25 (0.442516) as the primary rule
# (slope -0.386632), the below-only extrapolation (slope -0.433096, from D 22.0 and the rescan root) and the -0.33 rule beside it; 4 processes at nice 15; the chain's HOLD.txt stays on.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
for D in 22.15625 22.1875; do
  env SRC=I1025-macm3/kc87_leg2/b2 TAG=l1kc87Lmacm3b2 NP=4 NICE=15 SL2=-0.33 SL3=-0.433096 bash $L/pipeline87.sh $D 22.125 0.490845 -0.386632
  echo "$(date -u '+%F %T') UTC between_22: pipeline87.sh D $D returned $?" >> $L/between_22.log
done
