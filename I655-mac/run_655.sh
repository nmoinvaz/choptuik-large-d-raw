#!/usr/bin/env bash
# #655: every run of hp/kantorovich_log.py behind notes/CORRECTOR_BASIN.md. Usage, from the code checkout's hp/:
#   bash run_655.sh IN OUT
# IN holds the inputs, extracted from the raw-data repository with git show:
#   be58c93:I603-win2/chain.log -> I603_chain.log, be58c93:I603-win2/chain/anm_run.jsonl -> I603_anm_run.jsonl,
#   be58c93:I461-win2/crawlJ.log -> I461_crawlJ.log, be58c93:I461-win2/crawlJ/anm_run.jsonl -> I461_crawlJ_anm_run.jsonl,
#   c5ed39b:I603-win2/chain.log -> I603_chain_c5ed39b.log, c5ed39b:I603-win2/chain/anm_run.jsonl -> I603_anm_run_c5ed39b.jsonl.
# OUT gets the logs and exits.txt; the CSV goes to OUT/corrector_attempts.csv (equal to hp/data/corrector_attempts.csv).
IN=$1
OUT=$2
PY=${PY:-python3}
export OPENBLAS_NUM_THREADS=1
: > "$OUT/exits.txt"
nice -n 10 "$PY" kantorovich_log.py selftest --log "$OUT/selftest.log" > /dev/null; echo "selftest exit $?" >> "$OUT/exits.txt"
nice -n 10 "$PY" kantorovich_log.py selftest --mutate F > "$OUT/selftest_mutate_F.log"; echo "selftest --mutate F exit $?" >> "$OUT/exits.txt"
nice -n 10 "$PY" kantorovich_log.py selftest --mutate nofloor > "$OUT/selftest_mutate_nofloor.log"; echo "selftest --mutate nofloor exit $?" >> "$OUT/exits.txt"
nice -n 10 "$PY" kantorovich_log.py parse "$IN/I603_chain.log" --sample I603-win2 --jsonl "$IN/I603_anm_run.jsonl" \
    --csv "$OUT/corrector_attempts.csv" > "$OUT/parse.log"; echo "parse I603 exit $?" >> "$OUT/exits.txt"
nice -n 10 "$PY" kantorovich_log.py parse "$IN/I461_crawlJ.log" --sample I461-win2-crawlJ --jsonl "$IN/I461_crawlJ_anm_run.jsonl" \
    --csv "$OUT/corrector_attempts.csv" --append 1 >> "$OUT/parse.log"; echo "parse crawlJ exit $?" >> "$OUT/exits.txt"
nice -n 10 "$PY" kantorovich_log.py parse "$IN/I603_chain_c5ed39b.log" --sample I603-win2-new --jsonl "$IN/I603_anm_run_c5ed39b.jsonl" \
    --csv "$OUT/corrector_attempts.csv" --append 1 --from_step 38 >> "$OUT/parse.log"; echo "parse I603 new exit $?" >> "$OUT/exits.txt"
nice -n 10 "$PY" kantorovich_log.py analyse "$OUT/corrector_attempts.csv" --train I603-win2 --held I461-win2-crawlJ,I603-win2-new \
    --h_star 0.31 > "$OUT/analyse.log"; echo "analyse exit $?" >> "$OUT/exits.txt"
nice -n 10 "$PY" kantorovich_log.py analyse "$OUT/corrector_attempts.csv" --train I603-win2 --held I461-win2-crawlJ,I603-win2-new \
    --h_star 0.31 --mutate F > "$OUT/analyse_mutate_F.log"; echo "analyse --mutate F exit $?" >> "$OUT/exits.txt"
nice -n 10 "$PY" kantorovich_log.py analyse "$OUT/corrector_attempts.csv" --train I461-win2-crawlJ > "$OUT/analyse_crawlJ_fits.log"
echo "analyse crawlJ fits exit $?" >> "$OUT/exits.txt"
