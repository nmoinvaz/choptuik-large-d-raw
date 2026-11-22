# launches run_leap2.sh DA DB H OUTSIDE the calling terminal (cim_start.ps1: Win32_Process.Create, parent chain bash <- cmd <- WmiPrvSE <- svchost; BelowNormal). usage: launch_leap2.ps1 DA DB H
param([string]$DA, [string]$DB, [string]$H)
& "$PSScriptRoot\cim_start.ps1" -Name run_leap2 -Bash "bash run_leap2.sh $DA $DB $H"
