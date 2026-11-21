@echo off
start "mem1058" /min powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\nathan\Source\hp1058_winb\watch_mem_1058.ps1
start "prio1058" /min powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\nathan\Source\hp1058_winb\prio_hp_1058.ps1
