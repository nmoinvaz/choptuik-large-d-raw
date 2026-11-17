#!/bin/bash
# #903 p_min question: one.sh TAG STATE K runs near_null.py once on STATE (a path in choptuik-large-d-raw, read from
# origin/main into IN by git show as state.sh does, its blob logged in inputs.txt) at ks K, with the six weakest vectors
# saved (V_TAG_D<d>_ksK.npy), as state.sh's runs (--k=6 --its=32 --threads=3 --jv=od).
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad
P=$S/raw828push
IN=$S/raw903in
O=$(cd "$(dirname "$0")" && pwd)
tag=$1; st=$2; K=$3
mkdir -p "$IN/$(dirname "$st")"
if [ ! -f "$IN/$st" ]; then
  git -C "$P" fetch -q origin && git -C "$P" show "origin/main:$st" > "$IN/$st" || exit 8
fi
echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC $tag $st blob $(git -C "$P" rev-parse "origin/main:$st" 2>/dev/null || echo local) raw $(git -C "$P" rev-parse --short=8 origin/main)" >> "$O/inputs.txt"
d=$(basename "$st" .npz); d=${d##*_D}
"$O/run.sh" nn_${tag}_D${d}_ks$K near_null.py "$IN" "$st" --k=6 --its=32 --threads=3 --ks=$K --jv=od \
  --json="$O/nn_${tag}_D${d}_ks$K.json" --save_v="$O/V_${tag}_D${d}_ks$K.npy"
