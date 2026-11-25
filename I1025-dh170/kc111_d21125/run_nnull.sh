#!/bin/bash
# #1025 kc111_d21125, t5's hc: n_null of the k_c 103 and k_c 111 states at D 21.125 (nnull_count.py, one process of 1 thread, nice 10). Output nnull_k103.json, nnull_k111.json, nnull.log.
{
ROOT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc111_d21125
WTM=/home/nathan/Source/choptuik-large-d-1025k79/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
cd $ROOT || exit 9
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1
stamp() { date -u '+%F %T'; }
[ "$(git hash-object --no-filters nnull_count.py | cut -c1-8)" = "$(grep ' nnull_count.py' in_blobs.txt | cut -c1-8)" ] || { echo "nnull_count.py is not the pinned blob"; exit 1; }
for k in 103 111; do
  if [ $k = 103 ]; then REC=$ROOT/in/l1kc103dh170g.jsonl; ST=$ROOT/in/sol_l1kc103dh170g_D21.1250.npy; else REC=$ROOT/l1kc111dh170h.jsonl; ST=$ROOT/sol_l1kc111dh170h_D21.1250.npy; fi
  echo "$(stamp) UTC n_null k_c $k starts (state $(git hash-object --no-filters $ST | cut -c1-8))" | tee -a $ROOT/steps.txt
  /usr/bin/time -v nice -n 10 $PY -I -u nnull_count.py $REC $ST 21.125 $WTM k_c$k > nnull_k$k.json 2> nnull_k$k.err; rc=$?
  echo "$(stamp) UTC n_null k_c $k exit $rc: $(cut -c1-330 nnull_k$k.json)" | tee -a $ROOT/steps.txt
  grep -E 'Maximum resident|Elapsed' nnull_k$k.err | tee -a $ROOT/steps.txt
done
echo "NNULL DONE $(stamp) UTC" > $ROOT/NNULL_DONE.txt
exit 0
}
