#!/bin/bash
# #1025 winb follow-on (hybrid roots at D 17.5 and 17.75, k_c 63): build RAW from git blobs of origin/main (no checkout), each checked
# by git hash-object --no-filters against its pinned blob. Also checks that leap_kc63.log's D 17.75 line equals l1kc63W1025.jsonl's.
set -euo pipefail
P=/c/Users/nathan/Source/p4hi_1025
RAWW=/c/Users/nathan/Source/choptuik-large-d-raw-754
git -C "$RAWW" fetch -q origin
cat <<'PINS' | while read -r b p; do
a402559b5d37661b49da50f07f877af21fd29b3a I1025-mac/p4_hybrid.py
179ea09681b0a75f7cefdff98984b48051b3f085 I1025-mac/signtest.py
7ee33d79eb195a4cbf19c71db799cb93ea92c8d5 I1025-win/out/l1kc63Fw1025.jsonl
d85f7b71c2c1750ca91d941320b9f2cdf57fe029 I1025-win/out/sol_l1kc63Fw1025_D17.5000.npy
94ef7a72ed7ac963b42bb01e6b4fbd718c2f70fe I1025-win/leap_kc63.log
c33039dfa38b495486fb3ef7da77077d43db775a I1025-win/out/l1kc63W1025.jsonl
de9fc3e55aa46bafd4ef62536861f94aed9e3035 I1025-win/out/sol_l1kc63W1025_D17.750000.npy
PINS
  mkdir -p "$P/raw/$(dirname "$p")"
  git -C "$RAWW" show "origin/main:$p" > "$P/raw/$p"
  h=$(git hash-object --no-filters "$P/raw/$p")
  [ "$h" = "$b" ] || { echo "MISMATCH $p: got $h, pinned $b"; exit 1; }
  echo "ok $b $p"
done > "$P/prep_p4hi_inputs_1025.log"
echo "prep ok $(grep -c '^ok ' "$P/prep_p4hi_inputs_1025.log") files"
