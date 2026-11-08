@echo off
rem #82 relaunch (run 2): one node per call, %1 = omega/omega_inf. Normal priority, threads pinned to 1.
cd /d "C:\Users\nathan\Source\choptuik-t126\solver\inner_amp"
set VIRTUAL_ENV=C:\Users\nathan\Source\venv-t126
set PATH=C:\Users\nathan\Source\venv-t126\Scripts;%PATH%
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set RAYON_NUM_THREADS=1
set OUT=C:\Users\nathan\Source\choptuik-large-d-raw\I82-win2
python -u amp_flint_par.py %1 45 1500 1280 --procs 3 --fit phys --mf 6:12 --fit-step 1 --out %OUT%\sigF_w%1_K45_J1500_p1280.json >> %OUT%\w%1.log 2>&1
echo === w%1 exit %ERRORLEVEL% === >> "%OUT%\w%1_done.txt"
