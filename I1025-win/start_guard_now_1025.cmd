@echo off
rem #1025 winb: the guard with --now (the leap to D 18 at once, 4 BLAS threads), detached at BelowNormal
cd /d C:\Users\nathan\Source\choptuik-i1025
start "guardnow" /belownormal /wait /min cmd /c "C:\Users\nathan\Source\venv-choptuik-314\Scripts\python.exe -u guard_leap_1025.py --now > logs1025\guard_now_main.log 2>&1"
