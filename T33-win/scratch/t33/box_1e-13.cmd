@echo off
rem T33 box run 1e-13 (h 1e-13, w 1e-19,1e-23), one thread. Below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\cert-m5\solver\proof"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u certify_M.py box 5 --centre=data/A_M_refine_M5_d.json --use_out --h=1e-13 --w=1e-19,1e-23 --out=data/A_M_box_M5_1e-13.json --log=logs/A_M_box_M5_1e-13.log > "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t33\box_1e-13.out" 2>&1
echo exit %ERRORLEVEL% >> "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t33\box_1e-13.exit"
