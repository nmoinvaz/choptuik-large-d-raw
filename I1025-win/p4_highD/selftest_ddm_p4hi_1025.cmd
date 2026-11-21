@echo off
rem #1025 winb: ell_ddm.py selftest (must PASS) and selftest --mutate=slices (must FAIL) in the new worktree choptuik-i1025d at 48c36355, venv-md510, BelowNormal, 2 threads
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "OPENBLAS_NUM_THREADS=2"
set "OMP_NUM_THREADS=2"
set "MKL_NUM_THREADS=2"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\choptuik-i1025d\solver\matter
start "st1" /belownormal /wait /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u ell_ddm.py selftest > C:\Users\nathan\Source\p4hi_1025\ddB\selftest_ddm.log 2>&1
echo exit %errorlevel% >> C:\Users\nathan\Source\p4hi_1025\ddB\selftest_ddm.log
start "st2" /belownormal /wait /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u ell_ddm.py selftest --mutate=slices > C:\Users\nathan\Source\p4hi_1025\ddB\selftest_ddm_mutate_slices.log 2>&1
echo exit %errorlevel% >> C:\Users\nathan\Source\p4hi_1025\ddB\selftest_ddm_mutate_slices.log
