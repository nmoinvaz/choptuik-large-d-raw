# I1040 load sampler (alert-free, kills nothing): every 5 s the machine's total CPU % (Win32_PerfFormattedData_PerfOS_Processor _Total), the same as busy threads of 20, the available memory, and the three busiest
# processes by CPU % (name, pid, %), into load.log until the done file exists. Started by run_1040.sh.
param([string]$Out, [string]$DoneFile, [int]$Every = 5)
$log = Join-Path $Out 'load.log'
while (-not (Test-Path $DoneFile)) {
  $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')
  $tot = (Get-CimInstance Win32_PerfFormattedData_PerfOS_Processor -Filter "Name='_Total'").PercentProcessorTime
  $avail = [math]::Round((Get-Counter '\Memory\Available MBytes').CounterSamples[0].CookedValue/1024, 1)
  $top = Get-CimInstance Win32_PerfFormattedData_PerfProc_Process | Where-Object { $_.Name -ne '_Total' -and $_.Name -ne 'Idle' } | Sort-Object PercentProcessorTime -Descending | Select-Object -First 3 | ForEach-Object { "{0}({1}) {2}%" -f $_.Name, $_.IDProcess, $_.PercentProcessorTime }
  Add-Content -Path $log -Value ("{0} total_cpu_pct={1} busy_threads_of_20={2:N1} avail_GB={3} top: {4}" -f $ts, $tot, ($tot * 0.2), $avail, ($top -join '; '))
  Start-Sleep -Seconds $Every
}
Add-Content -Path $log -Value ("{0} done file seen, sampler ends" -f (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss'))
