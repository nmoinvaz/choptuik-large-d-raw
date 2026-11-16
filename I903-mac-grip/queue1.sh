#!/bin/bash
# #903 grip, queue 1: the D 60 control, then the order-142 chain's first base at D >= 229 with the mutation control.
O=$(cd "$(dirname "$0")" && pwd)
"$O/state.sh" ctl I611-win/kf13_D60_D60.001952.npz
st=$("$O/next.sh" I903-mac/chain_fixed 229)
echo "first base: $st $(date -u '+%H:%M')"
"$O/state.sh" k142 "$st" 200 --mutks
