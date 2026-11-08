@echo off
rem Launcher for run_amp_i179.sh at idle priority. Started detached.
set PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\bin;%PATH%
start "amp" /low /wait /b bash C:/Users/nathan/Source/choptuik-large-d-raw/I179-win/run_amp_i179.sh
