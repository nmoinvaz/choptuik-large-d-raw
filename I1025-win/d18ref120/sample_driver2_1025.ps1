# #1025 winb: a read-only sampler (BelowNormal) for the processes below a driver's python (pid $Drv): every $Interval s one line per python process of its tree into $Out:
# cpu seconds, working set and private bytes with their peaks, threads; and the laptop's free memory, cpu load and commit. Invariant number format, no thousands separators
# (the first sampler's "N" format put a comma into cpu seconds above 1000 and broke a CSV line). Ends when the driver's python is gone.
param([int]$Drv, [string]$Out, [int]$Interval = 60)
$inv = [cultureinfo]::InvariantCulture
if (-not (Test-Path $Out)) { 'utc,stage,pid,cpu_s,ws_gb,ws_peak_gb,private_gb,private_peak_gb,threads,free_phys_gb,laptop_cpu_pct,commit_gb' | Out-File -FilePath $Out -Encoding ascii }
function F($fmt, $v) { [string]::Format($inv, $fmt, $v) }
while (Get-Process -Id $Drv -ErrorAction SilentlyContinue) {
  $all = Get-CimInstance Win32_Process
  $kids = @{}; $q = New-Object System.Collections.Queue; $q.Enqueue($Drv)
  while ($q.Count -gt 0) { $p = $q.Dequeue(); foreach ($c in ($all | Where-Object { $_.ParentProcessId -eq $p })) { if (-not $kids.ContainsKey($c.ProcessId)) { $kids[$c.ProcessId] = $c; $q.Enqueue($c.ProcessId) } } }
  $os = Get-CimInstance Win32_OperatingSystem
  $cpu = (Get-CimInstance Win32_PerfFormattedData_PerfOS_Processor -Filter "Name='_Total'").PercentProcessorTime
  $mem = Get-CimInstance Win32_PerfFormattedData_PerfOS_Memory
  $sys = (F '{0:F2}' ($os.FreePhysicalMemory/1MB)) + ',' + $cpu + ',' + (F '{0:F2}' ($mem.CommittedBytes/1GB))
  $utc = (Get-Date).ToUniversalTime().ToString('HH:mm:ss')
  foreach ($k in $kids.Values) {
    if ($k.Name -ne 'python.exe') { continue }
    $pr = Get-Process -Id $k.ProcessId -ErrorAction SilentlyContinue
    if (-not $pr) { continue }
    $cl = [string]$k.CommandLine
    $stage = if ($cl -match "ell_ddm\.py det.*_D(\d+\.?\d*)\.npy") { "dd_D" + $Matches[1] } elseif ($cl -match "time.sleep") { "selftest" } else { "other" }
    $line = $utc + ',' + $stage + ',' + $pr.Id + ',' + (F '{0:F1}' $pr.CPU) + ',' + (F '{0:F3}' ($pr.WorkingSet64/1GB)) + ',' + (F '{0:F3}' ($pr.PeakWorkingSet64/1GB)) + ',' + (F '{0:F3}' ($pr.PrivateMemorySize64/1GB)) + ',' + (F '{0:F3}' ($pr.PeakPagedMemorySize64/1GB)) + ',' + $pr.Threads.Count + ',' + $sys
    Add-Content -Path $Out -Value $line -Encoding ascii
  }
  Start-Sleep -Seconds $Interval
}
