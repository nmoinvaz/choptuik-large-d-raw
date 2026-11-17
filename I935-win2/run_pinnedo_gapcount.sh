#!/bin/bash
# the gap-class tally of pinnedo_gapcount.py on the 4.8.2 package (venv-md482), BelowNormal, 5 threads
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
OUT=/d/choptuik-i935-raw/I935-win2
cd "$OUT" || exit 1
C:/Users/nathan/Source/venv-md482/Scripts/python.exe -u pinnedo_gapcount.py D:/choptuik-i935/hp D:/choptuik-i935-raw > pinnedo_gapcount.log 2>&1
echo "exit $?" >> pinnedo_gapcount.log
