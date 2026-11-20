@echo off
rem #1025 winb: new venv + multidouble 5.1.0, with MSVC's link.exe first on PATH (vcvars64), BelowNormal inherited from the launcher
call "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat" > C:\Users\nathan\Source\md510-1025\vcvars.log 2>&1
set "PATH=%PATH%;C:\Users\nathan\.cargo\bin;C:\Program Files\Git\cmd"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\md510-1025
"C:\Users\nathan\AppData\Local\Programs\Python\Python314\python.exe" -u driver_md510_1025.py > C:\Users\nathan\Source\md510-1025\driver_stdout.log 2>&1
