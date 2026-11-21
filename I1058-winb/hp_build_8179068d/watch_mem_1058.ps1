# #1058 winb: alert-only memory watcher for the hp build, every 30 s: commit charge and limit, available memory, page file size/use/peak, C: free,
# the biggest rustc's working set and private bytes, the biggest python's working set. It stops nothing. If C: free falls under 10 GB it tells the coordinator by hc
# (first time, again if under 5 GB, then at most every 30 min). It ends when the driver's log says done (or after 16 h).
$dir = "C:\Users\nathan\Source\hp1058_winb"
$csv = Join-Path $dir "mem_1058.csv"
$alog = Join-Path $dir "alerts_1058.log"
$blog = Join-Path $dir "hp1058_build.log"
$hc = "C:\Users\nathan\AppData\Local\Programs\herdr-core\hc.exe"
$coord = "nathans-macbook-air-m5-3/t5"
if (-not (Test-Path $csv)) { Add-Content $csv "utc,commit_gb,limit_gb,avail_gb,pf_alloc_mb,pf_used_mb,pf_peak_mb,c_free_gb,rustc_n,rustc_ws_gb,rustc_priv_gb,rustc_pid,python_ws_gb_top" }
$end = [DateTime]::UtcNow.AddHours(16)
$lastAlert = [DateTime]::MinValue; $lastLevel = 99
while ([DateTime]::UtcNow -lt $end) {
  try {
    $m = Get-CimInstance Win32_PerfFormattedData_PerfOS_Memory
    $pf = Get-CimInstance Win32_PageFileUsage | Select-Object -First 1
    $cfree = (Get-PSDrive C).Free / 1GB
    $r = @(Get-Process rustc -ErrorAction SilentlyContinue | Sort-Object WorkingSet64 -Descending)
    $py = Get-Process python -ErrorAction SilentlyContinue | Sort-Object WorkingSet64 -Descending | Select-Object -First 1
    $rws = 0; $rpr = 0; $rpid = 0
    if ($r.Count -gt 0) { $rws = $r[0].WorkingSet64 / 1GB; $rpr = $r[0].PrivateMemorySize64 / 1GB; $rpid = $r[0].Id }
    $pws = 0; if ($py) { $pws = $py.WorkingSet64 / 1GB }
    $line = "{0},{1:N2},{2:N2},{3:N2},{4},{5},{6},{7:N2},{8},{9:N2},{10:N2},{11},{12:N2}" -f [DateTime]::UtcNow.ToString("yyyy-MM-dd HH:mm:ss"), ($m.CommittedBytes / 1GB), ($m.CommitLimit / 1GB), ($m.AvailableMBytes / 1024), $pf.AllocatedBaseSize, $pf.CurrentUsage, $pf.PeakUsage, $cfree, $r.Count, $rws, $rpr, $rpid, $pws
    Add-Content $csv $line
    $level = if ($cfree -lt 5) { 5 } elseif ($cfree -lt 10) { 10 } else { 99 }
    if ($level -lt 99 -and (($level -lt $lastLevel) -or ([DateTime]::UtcNow - $lastAlert).TotalMinutes -ge 30)) {
      $txt = "winb #1058 hp build: C: free {0:N1} GB at {1} UTC (under {2} GB). Commit {3:N1} of {4:N1} GB, page file {5} MB allocated, {6} MB used. I stop nothing; your call." -f $cfree, [DateTime]::UtcNow.ToString("HH:mm"), $level, ($m.CommittedBytes / 1GB), ($m.CommitLimit / 1GB), $pf.AllocatedBaseSize, $pf.CurrentUsage
      Add-Content $alog ("{0} ALERT {1}" -f [DateTime]::UtcNow.ToString("yyyy-MM-dd HH:mm:ss"), $txt)
      & $hc send $coord $txt | Out-Null
      $lastAlert = [DateTime]::UtcNow; $lastLevel = $level
    } elseif ($level -eq 99) { $lastLevel = 99 }
  } catch { Add-Content $alog ("{0} watcher error: {1}" -f [DateTime]::UtcNow.ToString("yyyy-MM-dd HH:mm:ss"), $_.Exception.Message) }
  if ((Test-Path $blog) -and (Select-String -Path $blog -Pattern 'hp1058 driver done' -Quiet)) { Add-Content $alog ("{0} driver done, watcher stops" -f [DateTime]::UtcNow.ToString("yyyy-MM-dd HH:mm:ss")); break }
  Start-Sleep -Seconds 30
}
