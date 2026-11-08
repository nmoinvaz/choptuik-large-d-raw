@echo off
rem Launcher for run_i179.sh at idle priority. Started detached.
set PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\bin;%PATH%
start "checks" /low /wait /b bash C:/Users/nathan/Source/choptuik-large-d-raw/I179-win/run_i179.sh
