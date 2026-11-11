#!/usr/bin/env bash
# #522 part 2: eleven jobs (attempt of a = 0.5 and near_null_eq on its state), four at a time; then the rows_only control at the new state D 221.6312 (must exit nonzero).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I522-win2
cd $R || exit 9
printf '%s\n' 216.1312 217.1312 218.1312 219.1312 220.1312 221.1312 222.1312 223.1312 224.1312 225.1312 226.1312 | xargs -P 4 -I{} bash job_i522.sh {}
cd /d/choptuik-i505/hp || exit 9
N=$(ls $R/att_D221.1312/anm_pin3_D*.npz 2>/dev/null | head -n 1)
if [ -n "$N" ]; then
  Dn=$(basename $N .npz); Dn=${Dn#anm_pin3_}
  echo "control eq_$Dn --mutate=rows_only start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  nice -n 10 "$PY" -u near_null_eq.py $RAW I522-win2/att_D221.1312/anm_pin3_$Dn.npz --threads=2 --plant=7 --mutate=rows_only > $R/eq_${Dn}_ctl_rows_only.log 2>&1
  echo "control eq_$Dn --mutate=rows_only exit $? (must be nonzero) $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
fi
