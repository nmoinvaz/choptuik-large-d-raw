#!/bin/bash
# check (f): check_numbers.py --selftest from the worktree
A=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/octo_agent
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e
/usr/bin/time -p /Users/nathan/Source/choptuik-large-d/.venv/bin/python check_numbers.py --selftest > $A/check_f.log 2>&1
echo "exit $?" >> $A/check_f.log
