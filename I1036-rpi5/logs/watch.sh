#!/bin/bash
# stop when the driver is done, a run's exit differs from the expected one, or 55 min pass
declare -A EXP=([l2_mode_flat]=0 [l2_mode_check]=0 [l2_mode_check_curv]=1 [l2_mode_first_order]=0 [l2_mode_first_order_print]=0 [l2_c2_forcing]=0 [l2_c2_forcing_p1]=0 [l2_c2_checks_main]=1 [l2_c2_checks_ident]=1 [l2_c2_checks_series]=1 [l2_c2_checks_force]=1 [l2_c2_M1_planted]=0 [l2_c2_M1]=0 [l2_c2_M3]=0 [l2_c2_M5]=0 [l2_c2_M1_G]=0 [l2_c2_M3_G]=0 [l2_c2_M5_G]=0 [l2_c2_M5_mutate_gsign]=1 [l2_c2_summary]=0)
cd "$(dirname "$0")"
for i in $(seq 1 55); do
  grep -q "driver done" driver.log && break
  bad=$(awk '/ exit /{print $4, $6}' driver.log | while read n rc; do [ "${EXP[$n]}" != "$rc" ] && echo "MISMATCH $n exit $rc expected ${EXP[$n]}"; done)
  [ -n "$bad" ] && { echo "$bad"; break; }
  sleep 60
done
date -u '+%F %T UTC'; cat driver.log; cat times.txt; free -m | sed -n 2p
