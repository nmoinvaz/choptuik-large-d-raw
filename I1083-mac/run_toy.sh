#!/bin/bash
# the planted toy, its shift control and the no-valley case, into the raw folder's toy.log
H=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a984952191346adc9/hp/mode_matched.py
P=/Users/nathan/venv-314/bin/python
O=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/rawc/I1083-mac/toy.log
{
  nice -n 10 "$P" "$H" toy; echo "exit $?"
  nice -n 10 "$P" "$H" toy --mutate=shift; echo "exit $?"
  nice -n 10 "$P" "$H" toy --gap=0.05; echo "exit $?"
} > "$O" 2>&1
cat "$O"
