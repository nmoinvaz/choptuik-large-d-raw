# I1064 alert-only commit and page-file watch (added 17:36 UTC at the coordinator's hc, beside mem_watch.ps1): every 30 s the commit charge, the commit limit, the page file's size and usage,
# the free+zero list and the standby list go to commit.log until all.done exists. A line goes to alerts.log (the same file mem_watch.ps1 uses) when the commit charge is over $CommitAlertGB,
# or when the page file's allocated size grew or its usage rose more than $PfSlackMB over the values at the start. A condition is alerted when it first holds and then every 10 min while it holds.
# It kills nothing and signals nothing to the build or to any other job.
param([string]$Out, [double]$CommitAlertGB = 95.0, [double]$PfSlackMB = 512.0)
$log = Join-Path $Out 'commit.log'
$alerts = Join-Path $Out 'alerts.log'
$pf0 = Get-CimInstance Win32_PageFileUsage | Select-Object -First 1
$base0 = [double]$pf0.AllocatedBaseSize; $use0 = [double]$pf0.CurrentUsage
$last = @{ commit = [datetime]::MinValue; pf = [datetime]::MinValue }
function Alert($key, $text) {
  $now = Get-Date
  if (($now - $last[$key]).TotalMinutes -ge 10) {
    $last[$key] = $now
    "$($now.ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')) ALERT $text" | Add-Content -Path $alerts
  }
}
"$((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')) start: page file allocated $base0 MB, usage $use0 MB; commit alert over $CommitAlertGB GB, page-file slack $PfSlackMB MB" | Add-Content -Path $log
while (-not (Test-Path (Join-Path $Out 'all.done'))) {
  $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')
  $c = (Get-Counter '\Memory\Committed Bytes','\Memory\Commit Limit','\Memory\Available MBytes','\Memory\Free & Zero Page List Bytes','\Memory\Standby Cache Normal Priority Bytes','\Memory\Standby Cache Reserve Bytes','\Memory\Standby Cache Core Bytes').CounterSamples
  $v = @{}; foreach ($s in $c) { $v[($s.Path -replace '^.*\\','')] = $s.CookedValue }
  $commit = [math]::Round($v['committed bytes']/1GB, 2); $limit = [math]::Round($v['commit limit']/1GB, 2)
  $avail = [math]::Round($v['available mbytes']/1024, 2); $fz = [math]::Round($v['free & zero page list bytes']/1GB, 2)
  $sb = [math]::Round(($v['standby cache normal priority bytes'] + $v['standby cache reserve bytes'] + $v['standby cache core bytes'])/1GB, 2)
  $pf = Get-CimInstance Win32_PageFileUsage | Select-Object -First 1
  "$ts commit_GB=$commit limit_GB=$limit pagefile_alloc_MB=$($pf.AllocatedBaseSize) pagefile_use_MB=$($pf.CurrentUsage) pagefile_peak_MB=$($pf.PeakUsage) avail_GB=$avail free_zero_GB=$fz standby_GB=$sb" | Add-Content -Path $log
  if ($commit -gt $CommitAlertGB) { Alert 'commit' "commit charge $commit GB over $CommitAlertGB GB (limit $limit GB, page file $($pf.CurrentUsage) of $($pf.AllocatedBaseSize) MB)" }
  if (([double]$pf.AllocatedBaseSize -gt $base0) -or ([double]$pf.CurrentUsage -gt $use0 + $PfSlackMB)) { Alert 'pf' "page file growing: allocated $($pf.AllocatedBaseSize) MB (start $base0), usage $($pf.CurrentUsage) MB (start $use0), commit $commit GB" }
  Start-Sleep -Seconds 30
}
"$((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')) all.done seen, watch ends" | Add-Content -Path $log
