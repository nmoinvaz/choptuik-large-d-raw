#!/bin/bash
# #948 amendment (coordinator, 2026-11-17 22:33 UTC): the down ladder takes rungs of -10 with one fallback to -5, then -2, and stops at the
# first rung that fails at -2. run948.sh down (unit i948d, -10 rungs, stops at its first failure) was already running, and a running bash
# script is not edited, so this script waits for it, and when it stopped at a failed rung K it continues from the base of K + 10 with steps
# of 5, falling to steps of 2 when a rung fails at 5 (the step stays at what last worked), down to K 200. A failure at 2 stops it, and so
# does a -5 rung that hit its 2 h cap (cap948.sh touches RUNG.capped): the coordinator's order, 2026-11-17 (the polish below about
# ks 240 at D 232 enters #944's crawl).
# Same rung(), flags and threads (4) as run948.sh. Lines "948 ..." go to exits_948.txt.
WT=/home/nathan/Source/choptuik-large-d-935
R=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$R/I948-dh370
REL=I948-dh370
PY=$WT/.venv/bin/python
L=$OUT/exits_948.txt
S0=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D232.0000.npz
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
log() { echo "948 $* $(date -u '+%F %T')" >> "$L"; }
rung() {   # DIR K STATE THREADS
  local dir=$1 K=$2 state=$3 T=$4 t=$(date +%s)
  mkdir -p "$OUT/$dir"
  log "$dir start ks $K from $state threads $T hp $(git -C "$WT" rev-parse --short HEAD) load $(cut -d' ' -f1-3 /proc/loadavg)"
  ( cd "$WT/hp" && nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" "$PY" -u anm_run.py "$R" "$OUT/$dir" --state "$state" $F --threads "$T" \
      --D_max 400 --ks "$K" --keep_plan 0 --steps 0 --save_base 1 ) > "$OUT/$dir.log" 2>&1
  local rc=$?
  "$PY" "$OUT/check948.py" "$OUT/$dir" "$K" > "$OUT/$dir.check" 2>&1
  local ck=$?
  log "$dir exit $rc check $ck wall $(( $(date +%s) - t )) s: $(head -n 1 "$OUT/$dir.check" | cut -c1-200)"
  [ $rc -eq 0 ] && [ $ck -eq 0 ]
}
while systemctl --user is-active --quiet i948d; do sleep 30; done
last=$(grep -E "^948 down stopped at K [0-9]+" "$L" | tail -n 1)
[ -z "$last" ] && { log "down2: the -10 ladder ended without a failed rung, nothing to fall back from"; exit 0; }
P=$(( $(echo "$last" | sed 's/.*stopped at K \([0-9]*\).*/\1/') + 10 ))
if [ $P -eq 240 ]; then prev=$S0; else prev="$REL/$(basename "$(ls -d "$OUT"/down_K${P}_from*/ | head -n 1)")/base_pin3_D232.0000.npz"; fi
K=$P; step=5
log "down2: -10 ladder failed below K $P, falling back from $prev with steps of $step"
while [ $K -gt 200 ]; do
  t=$(( K - step )); [ $t -lt 200 ] && t=200
  if rung down_K${t}_from$K $t "$prev" 4; then prev="$REL/down_K${t}_from$K/base_pin3_D232.0000.npz"; K=$t; continue; fi
  if [ $step -eq 5 ] && [ -e "$OUT/down_K${t}_from$K.capped" ]; then log "down stopped at K $t (the -5 rung hit its cap)"; exit 1; fi
  if [ $step -eq 5 ]; then step=2; log "down2: -5 to K $t failed, trying steps of 2"; continue; fi
  log "down stopped at K $t (-2 failed)"; exit 1
done
log "down2 ladder done"
