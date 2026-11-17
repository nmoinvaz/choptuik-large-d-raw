#!/usr/bin/env bash
# #927 on the Mac, restarted 2026-11-17 00:20 UTC after the session's interruption killed the first chain during
# probe 2's onset scan (its D 3.04335 case had finished). Probe 2 for the remaining targets, then the pilot's
# references (run_ref.sh, at most 0.5 h of points by lowD_highM.py's own --hours rule).
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/raw927/I927-mac
echo "chain start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/chain_exits.txt
ONSET_TARGETS=3.04325,3.04315 bash $R/run_probe2.sh
mkdir -p $R/ref
HOURS=0.5 bash $R/run_ref.sh
echo "chain done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/chain_exits.txt
