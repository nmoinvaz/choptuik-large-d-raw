# launches run_leap3.sh DA DB H OUTSIDE the calling terminal (cim_start.ps1, the headless form: conhost.exe --headless cmd.exe /c; BelowNormal). usage: launch_leap3.ps1 DA DB H
param([string]$DA, [string]$DB, [string]$H)
& "$PSScriptRoot\cim_start.ps1" -Name run_leap3 -Bash "bash run_leap3.sh $DA $DB $H"
