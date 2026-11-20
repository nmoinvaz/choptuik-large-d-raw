@echo off
rem #1025 winb: the guard that holds the k_c 63 leap at D_end 18 (coordinator's order), detached at BelowNormal
cd /d C:\Users\nathan\Source\choptuik-i1025
start "guard1025" /belownormal /wait /min cmd /c "C:\Users\nathan\Source\venv-choptuik-314\Scripts\python.exe -u guard_leap_1025.py > logs1025\guard_main.log 2>&1"
