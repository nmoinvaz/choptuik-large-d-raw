#!/usr/bin/env bash
# The existing lines of a near_null log (the step lines dropped) against a reference log, times masked.
# Usage: cmp_old_lines.sh NEW.log REF.log
norm() { sed -E 's/LU [0-9]+ s/LU s/; s/ \([0-9]+ s\)$/ (s)/'; }
diff <(grep -vE '^  (step|pinned step)|^    ' "$1" | norm) <(norm < "$2") && echo "existing lines identical (times masked)"
