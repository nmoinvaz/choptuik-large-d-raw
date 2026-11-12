#!/bin/bash
# commit 2's kfreeze checks: frozen-row confinement, freeze_round (old and new kernel), Delta after one octo polish
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad
PY=/Users/nathan/venv-314/bin/python
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a1d6c8d73638fe3f8/hp
OUT=$S/raw-i489/I523-mac/c2
B=$S/xs/site_base
C=$S/i523/site_c2
RAW=$S/rawc
NICE=${NICE:-19}
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
mkdir -p "$OUT"
cd "$HP" || exit 1
run() {
  local name=$1 site=$2
  shift 2
  echo "== $name $(date -u '+%H:%M') $*" > "$OUT/$name.log"
  PYTHONPATH=$site:$HP nice -n $NICE "$@" >> "$OUT/$name.log" 2>&1
  echo "exit $?" >> "$OUT/$name.log"
}
for step in "$@"; do
  case $step in
    kfrows)
      run kfrows_base $B $PY $S/i523/kf_rows.py dump $RAW "$OUT/kf_base.npz"
      run kfrows_c2 $C $PY $S/i523/kf_rows.py dump $RAW "$OUT/kf_c2.npz"
      run kfrows $C $PY $S/i523/kf_rows.py cmp "$OUT/kf_base.npz" "$OUT/kf_c2.npz" ;;
    fround)
      run fround_base $B $PY $S/i523/freeze_round.py $RAW I461-win2/crawlJ/anm_pin3_D242.3642.npz --threads=2 --json="$OUT/fround_base.json"
      run fround_c2 $C $PY $S/i523/freeze_round.py $RAW I461-win2/crawlJ/anm_pin3_D242.3642.npz --threads=2 --json="$OUT/fround_c2.json"
      run fround_c2_proj $C $PY $S/i523/freeze_round.py $RAW I461-win2/crawlJ/anm_pin3_D242.3642.npz --threads=2 --mutate=proj ;;
    polish)
      for st in T129-win2/chain/anm_pin3_D180.5246.npz I461-win2/crawlJ/anm_pin3_D242.3642.npz; do
        tag=$(basename $st .npz)
        run polish_c2_$tag $C $PY $S/i523/delta_polish.py "$HP" $RAW $st "$OUT/polish_c2_$tag.json" --threads=2
        run polish_base_$tag $B $PY $S/i523/delta_polish.py "$HP" $RAW $st "$OUT/polish_base_$tag.json" --threads=2
      done ;;
  esac
done
echo "all done $(date -u '+%H:%M')" > "$OUT/done_kf_$(echo "$@" | tr ' ' '_')"
