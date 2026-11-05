@echo off
rem T113 (cloud 2026-11-05 14:46 UTC, restarted 20:21 UTC from the original start): large-D chain with the prediction in quad-double, T112 build. Below normal, 4 threads. After an interruption check the cloud's entry, then rerun this command (>> keeps the log).
cd /d C:\Users\nathan\Source\choptuik-t112\hp
set PATH=C:\Users\nathan\Source\venv-t112\Scripts;%PATH%
python.exe -u anm_run.py ..\..\choptuik-large-d-raw ..\..\choptuik-large-d-raw\T113-win\chain --state anm-mac/pred_q/A2/anm_pin3_D128.5559.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 1 --steps 300 --D_max 200 --threads 4 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 >> ..\..\choptuik-large-d-raw\T113-win\chain.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t113\t113.exit
