# #597 environment (source it). The two modecount_cx builds and main's hpkernel build, Python 3.14 of venv-314.
# new: the branch wip/i597-subagent (engine mode matrix); old: main 3c35f0c's modecount_cx (its own complex copy).
# Both built with the low-memory recipe (LTO off, 16 codegen units), target-cpu=native, unstripped.
SP=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad
export WT=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a500b5a2432ef3b0b
export RAW=$SP/i597/raw/I597-mac
export STATES=$SP/i597/states
export HPK=$SP/i599/site2
export PY=/Users/nathan/venv-314/bin/python3
new() { PYTHONPATH=$SP/i597/cx_new:$HPK nice -n 10 "$PY" -u "$@"; }
old() { PYTHONPATH=$SP/i597/cx_old:$HPK nice -n 10 "$PY" -u "$@"; }
