@echo off
rem T123 (cloud 2026-11-06 03:48 UTC): the fixed chain from T118's 152.93 state, 4 steps. Below normal, 4 threads.
cd /d C:\Users\nathan\Source\choptuik-t112\hp
set PATH=C:\Users\nathan\Source\venv-t112\Scripts;%PATH%
python.exe -u anm_run.py ..\..\choptuik-large-d-raw ..\..\choptuik-large-d-raw\T123-win\chain --state T118-win2/chain/anm_pin3_D152.9309.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.5 --steps 4 --D_max 200 --threads 4 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 > ..\..\choptuik-large-d-raw\T123-win\chain.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t123\t123.exit
