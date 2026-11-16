#!/bin/bash
# #855: one chain step (#603's anm_run.py command with --steps 1, as I614-dh370/timing614.sh) on the 7e4cfd03 build,
# 12 threads, nice 10, after #608's chains have ended. State: I614-dh370/base/base_pin3_D225.1312.npz, copied to base/.
# Its two saved states are compared with cmp against I614-dh370/chain_b614's (dh370's build of main 3c35f0c).
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I855-dh610
REF=/home/nathan/scratch855/refs
WT=/home/nathan/Source/choptuik-large-d
mkdir -p "$OUT/base" "$OUT/chain_venv" && cp "$REF/I614-dh370/base/base_pin3_D225.1312.npz" "$OUT/base/"
S=I855-dh610/base/base_pin3_D225.1312.npz
cd "$WT/hp" && . ../.venv/bin/activate || exit 1
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1
L=$OUT/timing_venv.log
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC, $(git rev-parse HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" > "$L"
t=$(date +%s)
nice -n 10 python -u anm_run.py $RAW $OUT/chain_venv --state $S --kfreeze 3 --held_fit data/held_fit.json \
   --N 24 --eps 1e-14 --h_max 1.0 --steps 1 --D_max 400 --threads 12 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 \
   --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 >> "$L" 2>&1
echo "exit $? wall $(( $(date +%s) - t )) s $(date -u '+%H:%M:%S') UTC" >> "$L"
for f in anm_pin3_D226.1312.npz pred_pin3_D226.1312.npz; do
  cmp "$OUT/chain_venv/$f" "$REF/I614-dh370/chain_b614/$f" >> "$L" 2>&1 && echo "$f identical to I614-dh370" >> "$L"
done
echo "timing done $(date -u '+%H:%M')" > "$OUT/timing_venv_done.txt"
