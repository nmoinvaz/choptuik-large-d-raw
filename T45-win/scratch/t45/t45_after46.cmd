@echo off
rem T45 resumes (cloud 02:05) once T46 has ended (t46\t46.exit), with main's fixed lowD_highM.py. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
:wait
if exist "%S%\t46\t46.exit" goto go
timeout /t 30 /nobreak > nul
goto wait
:go
call "%S%\t45\t45_step1.cmd"
