@echo off
rem T34: supercritical NNLO, waits for the first free thread (a T33 box run or T31b exiting). Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t34\t34_run.py" "%S%\t34-wt\solver\supercrit" "%S%\t33\box_3e-11.exit" "%S%\t33\box_1e-12a.exit" "%S%\t33\box_1e-12b.exit" "%S%\t33\box_1e-13.exit" "%S%\t31-wt\solver\matter\logs\t31b.exit" > "%S%\t34\t34.out" 2>&1
