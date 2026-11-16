#!/bin/bash
# #903 grip: state.sh TAG STATE [K...] [--mutks] reads STATE (a path in choptuik-large-d-raw) from origin/main into the
# inputs root IN (git show in the push worktree, which changes no checkout), records its blob, then runs near_null.py
# at the state's own order and at each K (default 200), one run at a time, and last lift.py over the folder.
# TAG names the chain (k142: xfkappa's I903-mac/chain_fixed; k160: dh610's I903-dh610/chain_k160; ctl: #902's D 60).
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad
P=$S/raw828push
IN=$S/raw903in
O=$(cd "$(dirname "$0")" && pwd)
PY=/Users/nathan/venv-314/bin/python3
tag=$1; st=$2; shift 2
mut=0; Ks=()
for a in "$@"; do if [ "$a" = --mutks ]; then mut=1; else Ks+=("$a"); fi; done
[ ${#Ks[@]} -eq 0 ] && Ks=(200)
mkdir -p "$IN/$(dirname "$st")"
if [ ! -f "$IN/$st" ]; then
  git -C "$P" fetch -q origin && git -C "$P" show "origin/main:$st" > "$IN/$st" || exit 8
fi
echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC $tag $st blob $(git -C "$P" rev-parse "origin/main:$st" 2>/dev/null || echo local) raw $(git -C "$P" rev-parse --short=8 origin/main)" >> "$O/inputs.txt"
own=$("$PY" -I -c "import json,sys,numpy as np; print(json.loads(str(np.load(sys.argv[1])['meta']))['ks'])" "$IN/$st")
[ "$tag" = ctl ] && own=142
d=$(basename "$st" .npz); d=${d##*_D}
nn() { K=$1; sfx=$2; shift 2; "$O/run.sh" nn_${tag}_D${d}_ks$K$sfx near_null.py "$IN" "$st" --k=6 --its=32 --threads=3 \
  --ks=$K --jv=od --json="$O/nn_${tag}_D${d}_ks$K$sfx.json" "$@"; }
nn "$own" "" --save_v="$O/V_${tag}_D${d}_ks$own.npy"
for K in "${Ks[@]}"; do nn "$K" "" --save_v="$O/V_${tag}_D${d}_ks$K.npy"; done
[ $mut = 1 ] && nn 200 _mutks --mutate=ks
{ echo "== lift $(date -u '+%Y-%m-%d %H:%M:%S') UTC"; "$PY" "$O/lift.py" "$O"; echo "exit $?"; } > "$O/lift.log" 2>&1
echo "$tag $d done $(date -u '+%H:%M')"
