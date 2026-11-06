@echo off
rem T120 (cloud 2026-11-06 03:04 UTC): replay of T118's first step (A) and T118's failing step from 152.93 (B), elimination corrector, one after the other. Below normal, 4 threads.
cd /d C:\Users\nathan\Source\choptuik-t112\hp
set PATH=C:\Users\nathan\Source\venv-t112\Scripts;%PATH%
set R=..\..\choptuik-large-d-raw
python.exe -u anm_run.py %R% %R%\T120-win\stepA --state T117-win/chain/anm_pin3_D152.3059.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.5 --steps 1 --D_max 200 --threads 4 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 > %R%\T120-win\stepA.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t120\stepA.exit
python.exe -u anm_run.py %R% %R%\T120-win\stepB --state T118-win2/chain/anm_pin3_D152.9309.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.5 --steps 1 --D_max 200 --threads 4 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 > %R%\T120-win\stepB.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t120\stepB.exit
