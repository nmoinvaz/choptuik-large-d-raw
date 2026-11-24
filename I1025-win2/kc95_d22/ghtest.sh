#!/bin/bash
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/kc95_d22
gh api repos/nmoinvaz/choptuik-large-d-raw/contents/I1025-macm3/kc87_leg2/b --jq '.[].name' > $OUT/ghtest.out 2> $OUT/ghtest.err
echo "exit $?" >> $OUT/ghtest.out
