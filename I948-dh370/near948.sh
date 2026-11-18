#!/bin/bash
# #948: near_null.py --k=6 --its=16 on every converged rung's base as it lands, within 12 threads in all (the ladders' anm_run.py and my own
# near_null.py runs counted from their --threads), 4 threads each when 4 are free, else 2 (the coordinator's order: start the up rungs'
# reads as each base lands, the down rungs' when the down ladder stops). The ks 240 rung was read early at 2 threads (near_early_*, copied to
# near_up_K240_from240.*). The D 222 reads (ks 230 from win2b's leg 6, ks 160 from dh610's chain) follow the rungs. Lines "948 near_NAME ..."
# go to exits_948.txt. Ends when both ladders and the fallback waiter are done and the queue is empty.
WT=/home/nathan/Source/choptuik-large-d-935
R=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$R/I948-dh370
REL=I948-dh370
PY=$WT/.venv/bin/python
L=$OUT/exits_948.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1
used() { local n; n=$(ps -eo args= | grep -E "^[^ ]*python[^ ]* (-u )?(anm_run|near_null)\.py" | grep -oE -- "--threads[= ][0-9]+" | grep -oE "[0-9]+$" | paste -sd+ | bc); echo "${n:-0}"; }
launch() {   # NAME STATE THREADS
  local name=$1 state=$2 T=$3
  touch "$OUT/near_$name.started"
  ( t=$(date +%s); echo "948 near_$name start $state threads $T $(date -u '+%F %T')" >> "$L"
    ( cd "$WT/hp" && nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" "$PY" -u near_null.py "$R" "$state" --k=6 --its=16 --threads=$T \
        --json="$OUT/near_$name.json" ) > "$OUT/near_$name.log" 2>&1
    echo "948 near_$name exit $? wall $(( $(date +%s) - t )) s $(date -u '+%F %T')" >> "$L" ) &
}
next() {     # prints "NAME STATE" of the next job not yet started, or nothing
  for d in $(ls -d "$OUT"/up_K*_from* "$OUT"/down_K*_from* 2>/dev/null | grep -v '\.' | sort -t_ -k2 -V); do
    n=$(basename "$d"); [ -e "$OUT/near_$n.started" ] && continue
    grep -q ": pass$" "$OUT/$n.check" 2>/dev/null && [ -e "$d/base_pin3_D232.0000.npz" ] && { echo "$n $REL/$n/base_pin3_D232.0000.npz"; return; }
  done
  [ -e "$OUT/near_D222_ks230.started" ] || { echo "D222_ks230 I903-win2/ks_chain/leg06_D212.0000_ks230/anm_pin3_D222.0000.npz"; return; }
  [ -e "$OUT/near_D222_ks160.started" ] || { echo "D222_ks160 I903-dh610/chain_k160/anm_pin3_D222.0000.npz"; return; }
}
while true; do
  free=$(( 12 - $(used) ))
  if [ $free -ge 2 ]; then
    job=$(next)
    if [ -n "$job" ]; then T=2; [ $free -ge 4 ] && T=4; launch $job $T; sleep 5; continue; fi
  fi
  if [ -z "$(next)" ] && [ "$(used)" -eq 0 ] && ! systemctl --user is-active --quiet i948u i948d i948f; then break; fi
  sleep 60
done
echo "948 near queue done $(date -u '+%F %T')" >> "$L"
