#!/bin/bash
# #1098 on mm5: ladder_point2.sh (blob 8802fb26) written from the raw clone's origin/main into <ladder>/tools3, then
# every file there checked by its git blob against I1098-mac-a/tools at 04f8e8066 or later; exit 1 on any mismatch
#
#     tools3_check.sh [RAW (~/Source/choptuik-large-d-raw)]
{
R=${1:-$HOME/Source/choptuik-large-d-raw}
T=$R/I1098-mm5/ladder/tools3
git -C $R fetch -q origin || exit 2
git -C $R show 8802fb2699aad3b73a9cab94cea5f4431e830bc2 > $T/ladder_point2.sh || exit 2
bad=0
while read -r b f; do
  h=$(git hash-object --no-filters $T/$f)
  if [ "$h" = "$b" ]; then echo "ok   $f $b"; else echo "BAD  $f $h (want $b)"; bad=1; fi
done <<'EOF'
8802fb2699aad3b73a9cab94cea5f4431e830bc2 ladder_point2.sh
322f0995ace89827d8265882f2c03defafaa7f1a ladder_tail.sh
6d29dfc0225a2eff0be932cb849e656c190a0b6e kstar_stage.sh
e74b4fc7464175341dc0b9a77e60507eeccf4363 kstar_gain.py
8e22d799c3822f57919018f60b63beb59bded157 kstar_summary.py
19b05a5a70e1b6e49f700e176a4d86c265a0ea48 variant_state.py
4de5c3174ad1bad3a5a311f909db9d3ecec64b5b resample_m.py
EOF
exit $bad
}
