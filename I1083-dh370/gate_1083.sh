#!/bin/bash
# #1083: t5's rule "keep total threads <= 12 with the #1080 walk; if the load stays above 12, run these after the decisive test instead". The load stood at 13.2 to 13.8 (1 min) beside the decisive test (4 threads),
# this chain (6) and the walk's offsets (4 workers). The `four` step (the key one: D_m at the four rates) is allowed to finish; when its line appears in steps_1083.txt this gate stops unit i1083a, so that
# steps 2b to 5b (run_1083b.sh, unit i1083b, already waiting) run after the decisive test ends. Unit i1083g. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1083-dh370
until grep -q ' 2_four: mode_matched' $OUT/steps_1083.txt; do sleep 3; done
systemctl --user stop i1083a
echo "$(date -u '+%F %T') UTC gate: step 2_four ended; unit i1083a stopped ($(systemctl --user is-active i1083a)); part 2 (i1083b) waits for the decisive test" >> $OUT/steps_1083.txt
exit 0
}
