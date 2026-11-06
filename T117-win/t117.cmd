@echo off
rem T117 (cloud 2026-11-06 01:17 UTC): the elimination corrector from T116's 149.56 state, pilot of 6 steps. Below normal, 4 threads. After an interruption check the cloud's entry (>> keeps the log).
cd /d C:\Users\nathan\Source\choptuik-t112\hp
set PATH=C:\Users\nathan\Source\venv-t112\Scripts;%PATH%
python.exe -u anm_run.py ..\..\choptuik-large-d-raw ..\..\choptuik-large-d-raw\T117-win\chain --state T116-win2/chain/anm_pin3_D149.5559.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.5 --steps 6 --D_max 200 --threads 4 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 >> ..\..\choptuik-large-d-raw\T117-win\chain.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t117\t117.exit
