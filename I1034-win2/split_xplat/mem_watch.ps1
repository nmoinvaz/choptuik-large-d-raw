# I1034 split_xplat alert-only memory watch: every 30 s the free memory and the build's processes' working sets go to mem.log until all.done exists.
# A line goes to alerts.log when the AVAILABLE memory (free + standby) is under $AlertGB. It kills nothing and signals nothing to the build.
param([string]$Out, [double]$AlertGB = 6.0)
$log = Join-Path $Out 'mem.log'
$alerts = Join-Path $Out 'alerts.log'
$names = @('cargo','rustc','maturin','link','lld-link','rust-lld','cl','pip','python','bash')
while (-not (Test-Path (Join-Path $Out 'all.done'))) {
  $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')
  $os = Get-CimInstance Win32_OperatingSystem
  $free = [math]::Round($os.FreePhysicalMemory/1MB, 2)
  $avail = [math]::Round((Get-Counter '\Memory\Available MBytes').CounterSamples[0].CookedValue/1024, 2)   # free + standby: what a build can take before others are trimmed
  $ps = @(Get-Process -ErrorAction SilentlyContinue | Where-Object { @('cargo','rustc','maturin','link','lld-link','rust-lld') -contains $_.ProcessName })
  $ws = [math]::Round((($ps | Measure-Object WorkingSet64 -Sum).Sum)/1GB, 2)
  $pv = [math]::Round((($ps | Measure-Object PrivateMemorySize64 -Sum).Sum)/1GB, 2)
  $pk = [math]::Round((($ps | Measure-Object PeakWorkingSet64 -Maximum).Maximum)/1GB, 2)
  $rc = ($ps | Where-Object ProcessName -eq 'rustc' | Select-Object -First 1)
  $prio = if ($rc) { $rc.PriorityClass } else { '-' }
  "$ts avail_GB=$avail free_GB=$free build_ws_GB=$ws build_private_GB=$pv max_one_peak_ws_GB=$pk procs=$($ps.Count) rustc_prio=$prio" | Add-Content -Path $log
  if ($avail -lt $AlertGB) {
    $top = (Get-Process -ErrorAction SilentlyContinue | Sort-Object WorkingSet64 -Descending | Select-Object -First 4 | ForEach-Object { '{0}({1}) {2:N1} GB' -f $_.ProcessName, $_.Id, ($_.WorkingSet64/1GB) }) -join '; '
    "$ts ALERT available memory $avail GB (free $free GB) < $AlertGB GB; build working set $ws GB; top: $top" | Add-Content -Path $alerts
  }
  Start-Sleep -Seconds 30
}
"$((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')) all.done seen, watch ends" | Add-Content -Path $log
