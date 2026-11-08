#!/bin/bash
# I179 amplitude copy on Python 3.14.10 (venv-t179), one process, idle priority beside #13's chains.
# Same arguments as #161/#146/#177: amp_flint_par.py 1.10 15 750 640 --procs 1 --fit phys --mf 6:12
export PATH=/c/Users/nathan/Source/venv-t179/Scripts:$PATH
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-t179 PYTHONFAULTHANDLER=1
RAW=/c/Users/nathan/Source/choptuik-large-d-raw; O=$RAW/I179-win
cd /c/Users/nathan/Source/choptuik-i179/solver/inner_amp
t() { /usr/bin/date -u '+%F %H:%M:%S'; }
echo "start $(t)" > $O/amp_exits.txt
python amp_flint_par.py 1.10 15 750 640 --procs 1 --fit phys --mf 6:12 --out $O/amp_copy1.json > $O/amp_copy1.log 2>&1
echo "amp_copy1 exit $? $(t)" >> $O/amp_exits.txt
echo done >> $O/amp_exits.txt
