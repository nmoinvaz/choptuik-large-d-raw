@echo off
rem T119 (cloud 2026-11-06 02:18 UTC): plain against elimination corrector at T116's D 149.96 stop, one step each, one after the other. Below normal, 4 threads.
cd /d C:\Users\nathan\Source\choptuik-t112\hp
set PATH=C:\Users\nathan\Source\venv-t112\Scripts;%PATH%
set R=..\..\choptuik-large-d-raw
python.exe -u anm_run.py %R% %R%\T119-win\plain --state T116-win2/chain/anm_pin3_D149.9621.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.5 --steps 1 --D_max 200 --threads 4 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 >> %R%\T119-win\plain.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t119\plain.exit
python.exe -u anm_run.py %R% %R%\T119-win\elim --state T116-win2/chain/anm_pin3_D149.9621.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.5 --steps 1 --D_max 200 --threads 4 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 >> %R%\T119-win\elim.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t119\elim.exit
