#!/usr/bin/env bash
# wakes when leg 7's base polish ends (the 'base I966-dh370' line) or after N seconds ($1, default 1800), or on a Traceback/attempt stopped line
LG=ks_chain3b/leg07_D252.8861_ks293/anm_run.log
t0=$(date +%s)
while sleep 15; do
  grep -q '^base I966' $LG && { echo "BASE POLISH ENDED"; grep -n '^base I966\|^step 0:\|a_rule reseed\|elim projections\|octo-double Newton' $LG | cut -c1-230 | tail -n 8; exit 0; }
  grep -qE '^Traceback|attempt stopped|stopping \(stalled\)|no trial step accepted' $LG && { echo "TRIGGER in leg 7 log"; tail -n 6 $LG | cut -c1-200; exit 0; }
  [ $(( $(date +%s) - t0 )) -ge ${1:-1800} ] && { echo "TIMEOUT, no base line yet"; tail -n 4 $LG | cut -c1-200; exit 0; }
done
