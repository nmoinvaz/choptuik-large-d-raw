#!/bin/bash
# #941 on dh370: near_null.py --k=6 --its=16 --threads=4 on eight stored states, three runs at a time (4 threads each, 12 in all),
# nice 10, worktree ~/Source/choptuik-large-d-935 (main 808b1fac, its 4.8.2 .venv), raw clone R = the wt613 worktree.
#   run941.sh ctl    the planted check and its two controls on order 160, D 230.0 (three runs at once):
#                      ctl_planted     --planted=1                      must exit 0 (planted and sigma checks pass)
#                      ctl_planted_mut --planted=1 --mutate=scale_block must exit 1 (the planted check must fail)
#                      ctl_sigma_mut   --mutate=sigma                   must exit 1 (sigma_1 reported 1.05 times too large)
#   run941.sh extra  three runs added after the eight (the coordinator's list had one order-135 state, which gives no fall per unit D):
#                      o240_D232.0000 (the order-240 chain's last state), o135_D229.1312 and o135_D231.1312 (order-135 control)
#   run941.sh extra2 three more order-160 states of dh610's chain, D 232, 233 and 234 (the last stalls at the next step, #944)
#   run941.sh data   the eight states, plain `near_null.py R STATE --k=6 --its=16 --threads=4 --json=...`, three lanes
# Each run writes NAME.log and NAME.json here, and a line "941 NAME exit RC wall S s" to exits_941.txt.
WT=/home/nathan/Source/choptuik-large-d-935
R=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$R/I941-dh370
PY=$WT/.venv/bin/python
L=$OUT/exits_941.txt
W=I903-win2/ks_chain/leg07_D222.0000_ks240
H=I903-dh610/chain_k160
M=I903-macm3/chain_k135
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1

one() {   # NAME STATE [extra flags]
  local name=$1 state=$2; shift 2
  local t=$(date +%s)
  echo "941 $name start $(date -u '+%F %T') hp $(git -C "$WT" rev-parse --short HEAD) $state $*, load $(cut -d' ' -f1-3 /proc/loadavg)" >> "$L"
  ( cd "$WT/hp" && nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" "$PY" -u near_null.py "$R" "$R/$state" --k=6 --its=16 --threads=4 \
      --json="$OUT/$name.json" "$@" ) > "$OUT/$name.log" 2>&1
  local rc=$?
  echo "941 $name exit $rc wall $(( $(date +%s) - t )) s $(date -u '+%F %T')" >> "$L"
}
export -f one
export WT R OUT PY L

case $1 in
  ctl)
    one ctl_planted "$H/anm_pin3_D230.0000.npz" --planted=1 &
    one ctl_planted_mut "$H/anm_pin3_D230.0000.npz" --planted=1 --mutate=scale_block &
    one ctl_sigma_mut "$H/anm_pin3_D230.0000.npz" --mutate=sigma &
    wait ;;
  data)
    # three lanes of 3, 3 and 2 runs, started in this order
    printf '%s\n' \
      "o240_D229.0509 $W/anm_pin3_D229.0509.npz" "o240_D229.9822 $W/anm_pin3_D229.9822.npz" "o240_D230.9281 $W/anm_pin3_D230.9281.npz" \
      "o240_D231.7466 $W/anm_pin3_D231.7466.npz" "o160_D229.0000 $H/anm_pin3_D229.0000.npz" "o160_D230.0000 $H/anm_pin3_D230.0000.npz" \
      "o160_D231.0000 $H/anm_pin3_D231.0000.npz" "o135_D230.1312 $M/anm_pin3_D230.1312.npz" \
      | xargs -P 3 -L 1 bash -c 'one $0 $1' ;;
  extra)
    one o240_D232.0000 "$W/anm_pin3_D232.0000.npz" &
    one o135_D229.1312 "$M/anm_pin3_D229.1312.npz" &
    one o135_D231.1312 "$M/anm_pin3_D231.1312.npz" &
    wait ;;
  extra2)
    one o160_D232.0000 "$H/anm_pin3_D232.0000.npz" &
    one o160_D233.0000 "$H/anm_pin3_D233.0000.npz" &
    one o160_D234.0000 "$H/anm_pin3_D234.0000.npz" &
    wait ;;
  *) echo "usage: run941.sh ctl|data|extra|extra2"; exit 2 ;;
esac
