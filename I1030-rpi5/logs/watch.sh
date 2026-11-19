#!/bin/bash
# stop when the driver is done, a run's exit differs from the expected one, or 55 min pass
declare -A EXP=([route3_bound_lemmas]=0 [route3_bound_constants]=0 [route3_bound_constants_J0100]=0 [route3_bound_check]=0 [route3_bound_check_plant]=1 [route3_bound_check_psi]=1 [route3_tuned_7_800]=0 [route3_tuned_7_800_demix]=1 [route3_head_scope]=0 [route3_head_lemmas]=0 [route3_head_check]=0 [route3_head_check_plant]=1 [route3_head_check_gsmall]=1 [route3_head_certify]=0)
cd "$(dirname "$0")"
for i in $(seq 1 55); do
  grep -q "driver done" driver.log && break
  bad=$(awk '/ exit /{print $4, $6}' driver.log | while read n rc; do [ "${EXP[$n]}" != "$rc" ] && echo "MISMATCH $n exit $rc expected ${EXP[$n]}"; done)
  [ -n "$bad" ] && { echo "$bad"; break; }
  sleep 60
done
date -u '+%F %T UTC'; cat driver.log; cat times.txt; free -m | sed -n 2p
