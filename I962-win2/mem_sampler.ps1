# Samples the build's processes every 30 s until build.done exists.
param([string]$Out)
$names = 'cargo','rustc','maturin','link','lld-link','rust-lld','cl','pip','python','bash','nice'
$log = Join-Path $Out 'mem.log'
while (-not (Test-Path (Join-Path $Out 'build.done'))) {
  $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')
  $os = Get-CimInstance Win32_OperatingSystem
  $free = [math]::Round($os.FreePhysicalMemory/1MB, 2)
  $ps = @(Get-Process -ErrorAction SilentlyContinue | Where-Object { @('cargo','rustc','maturin','link','lld-link','rust-lld') -contains $_.ProcessName })
  $ws = [math]::Round((($ps | Measure-Object WorkingSet64 -Sum).Sum)/1GB, 2)
  $pv = [math]::Round((($ps | Measure-Object PrivateMemorySize64 -Sum).Sum)/1GB, 2)
  $pk = [math]::Round((($ps | Measure-Object PeakWorkingSet64 -Maximum).Maximum)/1GB, 2)
  $rc = ($ps | Where-Object ProcessName -eq 'rustc' | Select-Object -First 1)
  $prio = if ($rc) { $rc.PriorityClass } else { '-' }
  "$ts free_GB=$free build_ws_GB=$ws build_private_GB=$pv max_one_peak_ws_GB=$pk procs=$($ps.Count) rustc_prio=$prio" | Add-Content -Path $log
  Start-Sleep -Seconds 30
}
