#!/usr/bin/env bash
# #644 step 4 (the coordinator, message 1794555309173-0): the weak directions of the two starts the `own` run saves, from the same worktree (D:/choptuik-i644, origin/main 5b9059ec) and venv-i600, 9 threads.
# pred_pin3_D249.3927.npz is the a 0.763 prediction (refused in #603), pred_pin3_D249.0113.npz the a 0.3815 one (accepted). Report sigma_1..4 and, for each start's "pinned step", |dz|, max|dz| and its share on V.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I644-win2
cd /d/choptuik-i644/hp || exit 9
export OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
for f in 0763:D249.3927 0381:D249.0113; do
  tag=${f%%:*}; D=${f##*:}
  src=I644-win2/own/pred_pin3_$D.npz
  [ -f $RAW/$src ] || { echo "missing $src (the own run saves it); use the prediction it saved for its a 0.3815 attempt" >> $R/exits_644.txt; continue; }
  echo "near_null $tag start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_644.txt
  nice -n 5 "$PY" -u near_null.py $RAW $src --k=4 --threads=9 --json=$R/near_null_pred_$tag.json > $R/near_null_pred_$tag.log 2>&1
  echo "near_null $tag exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_644.txt
done
