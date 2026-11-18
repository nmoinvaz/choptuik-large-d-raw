#!/bin/bash
# #948 on dh370: a ks ladder of base polishes at D 232.0 from win2b's leg-7 end state (ks 240), then near_null.py --k=6 on each rung's base
# and on three states at D 222. Worktree ~/Source/choptuik-large-d-935 (main 808b1fac, its 4.8.2 .venv), raw clone R, nice 10.
#   run948.sh up     6 threads: K = 240 (the control, the state's own order), 250, 260, 270, 280, 300, 320 (the last two by +20, by +10 when
#                    a +20 rung fails). Each rung is `anm_run.py R OUT/up_K<K>_from<P> --state <previous base> --ks K --keep_plan 0 --steps 0
#                    --save_base 1` with I903-win2/run_ks_chain.sh's F (threads changed) and --D_max 400; check948.py judges it
#                    (converged, max|F| <= 1e-60, ks, no file past the base) and a rung that fails stops the direction.
#   run948.sh down   4 threads: K = 230, 220, 210, 200, the first from the state, each from the one before.
#   run948.sh near   near_null.py --k=6 --its=16 --threads=4, three at a time, on every converged rung's base and the D 222 states.
# Lines "948 NAME start|exit ..." go to exits_948.txt.
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

rung() {   # DIR K STATE(relative to R) THREADS -> 0 when the rung converged and wrote only its base
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
base() { echo "$REL/$1/base_pin3_D232.0000.npz"; }

case $1 in
  up)
    prev=$S0; pk=240
    for K in 240 250 260 270 280; do
      rung up_K${K}_from$pk $K "$prev" 6 || { log "up stopped at K $K"; exit 1; }
      prev=$(base up_K${K}_from$pk); pk=$K
    done
    for K in 300 320; do
      if rung up_K${K}_from$pk $K "$prev" 6; then prev=$(base up_K${K}_from$pk); pk=$K; continue; fi
      log "up: +20 to K $K failed, trying +10"
      mid=$((K - 10))
      rung up_K${mid}_from$pk $mid "$prev" 6 || { log "up stopped at K $mid"; exit 1; }
      prev=$(base up_K${mid}_from$pk); pk=$mid
      rung up_K${K}_from$pk $K "$prev" 6 || { log "up stopped at K $K"; exit 1; }
      prev=$(base up_K${K}_from$pk); pk=$K
    done
    log "up ladder done" ;;
  down)
    prev=$S0; pk=240
    for K in 230 220 210 200; do
      rung down_K${K}_from$pk $K "$prev" 4 || { log "down stopped at K $K"; exit 1; }
      prev=$(base down_K${K}_from$pk); pk=$K
    done
    log "down ladder done" ;;
  near)
    one() { local name=$1 state=$2; local t=$(date +%s)
      log "$name start $state"
      ( cd "$WT/hp" && nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" "$PY" -u near_null.py "$R" "$state" --k=6 --its=16 --threads=4 \
          --json="$OUT/$name.json" ) > "$OUT/$name.log" 2>&1
      log "$name exit $? wall $(( $(date +%s) - t )) s"; }
    export -f one log; export WT R OUT PY L REL
    ls -d "$OUT"/up_K*_from*/base_pin3_D232.0000.npz "$OUT"/down_K*_from*/base_pin3_D232.0000.npz 2>/dev/null | while read b; do
      d=$(basename "$(dirname "$b")"); "$PY" "$OUT/check948.py" "$(dirname "$b")" "$(echo "$d" | sed 's/.*_K\([0-9]*\)_from.*/\1/')" >/dev/null 2>&1 && echo "near_$d $REL/$d/base_pin3_D232.0000.npz"
    done > "$OUT/near_list.txt"
    cat >> "$OUT/near_list.txt" <<LIST
near_D222_ks230 I903-win2/ks_chain/leg06_D212.0000_ks230/anm_pin3_D222.0000.npz
near_D222_ks160 I903-dh610/chain_k160/anm_pin3_D222.0000.npz
LIST
    xargs -P 3 -L 1 bash -c 'one $0 $1' < "$OUT/near_list.txt" ;;
  *) echo "usage: run948.sh up|down|near"; exit 2 ;;
esac
