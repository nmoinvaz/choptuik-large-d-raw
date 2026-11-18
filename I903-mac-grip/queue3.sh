#!/bin/bash
# #903 grip, the coordinator's pick (2026-11-18): queue3.sh PART runs state.sh one base at a time, at the base's own
# order and ks 200. Part a: macm3b's order 135 at D 254.7003 and order 142's last base, D 250.2455. Part b: order 135 at
# order 142's own bases, D 249.1312, 244.1312, 239.1312 and 229.1312.
O=$(cd "$(dirname "$0")" && pwd)
case "$1" in
  a) L=("k135 I903-macm3/chain_k135/anm_pin3_D254.7003.npz" "k142 I903-mac/chain_fixed/anm_pin3_D250.2455.npz") ;;
  b) L=("k135 I903-macm3/chain_k135/anm_pin3_D249.1312.npz" "k135 I903-macm3/chain_k135/anm_pin3_D244.1312.npz"
        "k135 I903-macm3/chain_k135/anm_pin3_D239.1312.npz" "k135 I903-macm3/chain_k135/anm_pin3_D229.1312.npz") ;;
  *) echo "usage: queue3.sh a|b"; exit 2 ;;
esac
for x in "${L[@]}"; do
  read -r tag st <<< "$x"
  echo "queue3 $1: $tag $st $(date -u '+%H:%M')"
  gtimeout 3h "$O/state.sh" "$tag" "$st" 200 || echo "state.sh exit $? for $tag $st"
done
