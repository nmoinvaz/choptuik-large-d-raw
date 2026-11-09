#!/bin/bash
# #257: every committed circle record of hp/modecount_circle.py re-run from its evaluation caches (recheck_circles.py),
# #178's two R 0.03 circles first. From the code worktree's root; no determinants.
PY=/Users/nathan/venv-314/bin/python
RAW=/Users/nathan/Source/choptuik-large-d-raw
O=$RAW/I257-mac
S=$O/scripts/recheck_circles.py
OUT=$O/recheck.jsonl
L=$O/logs/recheck.log
r() { echo "### $1" >> $L; nice -n 10 $PY $S hp $OUT "$@" >> $L 2>&1; echo "$1 exit $?" >> $O/logs/recheck_exits.txt; }
r $RAW/I178-macm3/circles_locate.jsonl $RAW/I178-macm3/locate_r2/modecount_D45.0507_M48_kf21_locr2_evals.jsonl \
  $RAW/I178-macm3/locate_r1/modecount_D45.0507_M48_kf21_locr1_evals.jsonl
r $RAW/I178-macm3/circles.jsonl $RAW/I178-macm3/data_kf*/modecount_D45.0507_M48_kf*_circ_evals.jsonl
r $RAW/I190-macm3/circles.jsonl $RAW/I190-macm3/data_kf*/modecount_D45.0507_M48_kf*_circ_evals.jsonl
for x in kf21_C kf21_D kf21_E kf23_A kf23_B; do
  r $RAW/I230-mac/data/circles_$x.jsonl $RAW/I230-mac/data/modecount_D61.0264_M48_${x}_evals.jsonl
done
r $RAW/I231-macm3/D55_M40/data/modecount_circles.jsonl $RAW/I231-macm3/D55_M40/data/modecount_D55.0351_M40_kf23_evals.jsonl
r $RAW/I238-macm3/D54/data/modecount_circles.jsonl $RAW/I238-macm3/D54/data/modecount_D54.0414_M48_kf23_evals.jsonl
r $RAW/I238-macm3/D55/data/modecount_circles.jsonl $RAW/I238-macm3/D55/data/modecount_D55.0351_M48_kf23_evals.jsonl
r $RAW/I250-mac/october/data/modecount_circles.jsonl $RAW/I250-mac/october/data/modecount_D30.0688_M48_october_evals.jsonl
r $RAW/I250-mac/inner015/data/modecount_circles.jsonl $RAW/I250-mac/inner015/data/modecount_D30.0688_M48_inner015_evals.jsonl
# the D 30 M 48 circles (#68, #148, #156 and main): every cache of their tags
for f in $RAW/I68-macm3/hp_data_after_control_fresh/modecount_circles.jsonl \
         $RAW/I68-macm3/hp_data_after_control_replay/modecount_circles.jsonl \
         $RAW/I148-macm3/hp_data_after/modecount_circles.jsonl $RAW/I156-macm3/hp_data_after/modecount_circles.jsonl \
         hp/data/modecount_circles.jsonl; do
  r $f $RAW/I68-macm3/hp_data_after_control_fresh/modecount_D30.0688_M48_evals.jsonl \
    $RAW/I68-macm3/october_inputs/modecount_D30.0688_M48_evals.jsonl \
    $RAW/I156-macm3/hp_data_after/modecount_D30.0688_M48_evals.jsonl \
    $RAW/I156-macm3/october_inputs/modecount_D30.0688_M48_evals.jsonl \
    $RAW/I148-macm3/hp_data_after/modecount_D30.0688_M48_kf13_evals.jsonl \
    $RAW/I148-macm3/october_inputs/modecount_D30.0688_M48_kf13_evals.jsonl \
    hp/data/modecount_D30.0688_M48_evals.jsonl hp/data/modecount_D30.0688_M48_kf13_evals.jsonl
done
