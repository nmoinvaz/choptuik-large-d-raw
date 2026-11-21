# #1025 winb, the D 18.5 root: an external sampler (the driver's own sampler thread broke at 10:54 UTC: the "N" number format put a thousands
# separator into cpu seconds above 1000, so its CSV line split into too many fields; the exception is caught and the run is untouched).
# Every 60 s, for every process below the driver's python (pid in $args[0]): cpu seconds, working set and private bytes with their peaks, threads;
# and the laptop's free memory, cpu load and commit. Ends when the driver's python is gone. Read-only, BelowNormal.
param([int]$Drv)
$inv = [cultureinfo]::InvariantCulture
$out = 'C:\Users\nathan\Source\p4hi_1025\I1025-win\p4_highD\rows\d185_samples2.csv'
if (-not (Test-Path $out)) { 'utc,stage,pid,cpu_s,ws_gb,ws_peak_gb,private_gb,private_peak_gb,threads,free_phys_gb,laptop_cpu_pct,commit_gb' | Out-File -FilePath $out -Encoding ascii }
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
    $stage = if ($cl -match 'p4_hybrid') { 'hybrid' } elseif ($cl -match 'ell_ddm.py det\s+\S+\s+\S+\s+\S+\s+(\S+)') { 'dd_' + $Matches[1] } else { 'other' }
    $line = $utc + ',' + $stage + ',' + $pr.Id + ',' + (F '{0:F1}' $pr.CPU) + ',' + (F '{0:F3}' ($pr.WorkingSet64/1GB)) + ',' + (F '{0:F3}' ($pr.PeakWorkingSet64/1GB)) + ',' + (F '{0:F3}' ($pr.PrivateMemorySize64/1GB)) + ',' + (F '{0:F3}' ($pr.PeakPagedMemorySize64/1GB)) + ',' + $pr.Threads.Count + ',' + $sys
    Add-Content -Path $out -Value $line -Encoding ascii
  }
  Start-Sleep -Seconds 60
}
