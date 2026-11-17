#!/bin/bash
# #928: the pilot, two points past D 11 at each coupling with their rates
J=$(cd "$(dirname "$0")" && pwd)
S=$J/seeds
bash "$J/seg.sh" 0.3 11 11.125 "$S/sm_eta0.3_D11_polish_M32.npz" "$S/sm_eta0.3_D10.9375_polish_M32.npz" \
    10.75:2.988055281843062,11.0:2.967495609277564
bash "$J/seg.sh" 1 11 11.125 "$S/sm_eta1_D11_M32.npz" "$S/sm_eta1_D10.9375_polish_M32.npz" \
    10.75:2.881573902797974,11.0:2.863317651983317
echo "$(date -u '+%F %T') UTC run_pilot done" >> "$J/out/runs.log"
