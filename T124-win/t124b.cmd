@echo off
rem T124 resumed on the T125 build (multidouble 3.2.0) from its last state, cloud 2026-11-06 05:39 UTC. Below normal, 4 threads.
cd /d C:\Users\nathan\Source\choptuik-t125\hp
set PATH=C:\Users\nathan\Source\venv-t125\Scripts;%PATH%
python.exe -u anm_run.py ..\..\choptuik-large-d-raw ..\..\choptuik-large-d-raw\T124-win\chain --state T124-win/chain/anm_pin3_D153.4309.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.25 --steps 300 --D_max 200 --threads 4 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 >> ..\..\choptuik-large-d-raw\T124-win\chain.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t124\t124b.exit
