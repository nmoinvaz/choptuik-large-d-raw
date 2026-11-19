#!/bin/bash
# the D 253 context runs after the first: split 1 at ks 130, then split 2 and split 1 at ks 240 (6 orders, one run each)
cd /Users/nathan/Source/choptuik-large-d-1034/hp
while pgrep -f "hptest_v1 split_file" >/dev/null; do sleep 5; done
for cfg in "130 1" "240 2" "240 1"; do
  set -- $cfg
  ks=$1; sp=$2
  kenv=""; [ "$ks" != 130 ] && kenv="KS=$ks"
  { date -u '+start %H:%M'; time env FILE=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i6data/ctx_D253.3382.bin JET=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i6data/jet_D253.3382.bin NORD=6 SPLIT=$sp REPS=1 $kenv nice -n 10 /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/hptest_v1 split_file --ignored --nocapture; date -u '+end %H:%M'; } > /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/split_file_D253_ks${ks}_N6_s${sp}.log 2>&1
done
echo QUEUE-DONE
