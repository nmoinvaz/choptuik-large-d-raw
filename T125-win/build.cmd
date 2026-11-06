@echo off
set VIRTUAL_ENV=C:\Users\nathan\Source\venv-t125
set PATH=C:\Users\nathan\Source\venv-t125\Scripts;C:\Program Files\Git\bin;C:\Program Files\Git\usr\bin;%PATH%
set CARGO_BUILD_JOBS=4
set RAW=C:\Users\nathan\Source\choptuik-large-d-raw\T125-win
cd /d C:\Users\nathan\Source\choptuik-t125
echo start %date% %time% > %RAW%\build_time.txt
bash hp/build.sh > %RAW%\build.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t125\build.exit
echo end %date% %time% >> %RAW%\build_time.txt
