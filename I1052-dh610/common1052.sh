# sourced by run1052.sh (PR #1052's A/B on dh610)
REPO=/home/nathan/Source/choptuik-large-d
W=/home/nathan/Source/choptuik-large-d-1052
WB=/home/nathan/Source/choptuik-large-d-1052base
VENV=/home/nathan/Source/venv-i1050
PY=$VENV/bin/python
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I1052-dh610
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH
stamp() { date -u '+%F %T'; }
