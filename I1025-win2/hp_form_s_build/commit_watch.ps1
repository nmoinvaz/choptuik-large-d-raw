# commit_watch.ps1 OUTDIR: alert-only sampler of the commit charge and of this task's processes, every 30 s; never kills anything.
# commit.log: one line per sample (UTC time, commit used/limit/headroom GB, free physical GB, the build's processes (cargo, rustc, maturin, link) working set and private sum, the precision jobs' sums);
# alerts.txt: a line when the headroom falls below 8 GB ("ALERT") and again at each further 2 GB, and when it is back above 12 GB ("CLEAR"). Stops when OUTDIR\commit_watch.stop exists.
param([string]$Out)
$log = Join-Path $Out 'commit.log'; $alerts = Join-Path $Out 'alerts.txt'; $stop = Join-Path $Out 'commit_watch.stop'
$lastAlert = 1e9; $alerted = $false
$peakBuildWs = 0.0; $peakBuildPriv = 0.0; $peakCommit = 0.0; $minHead = 1e9
while (-not (Test-Path $stop)) {
  $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')
  $os = Get-CimInstance Win32_OperatingSystem
  $lim = $os.TotalVirtualMemorySize / 1MB; $used = ($os.TotalVirtualMemorySize - $os.FreeVirtualMemory) / 1MB; $head = $lim - $used
  $free = $os.FreePhysicalMemory / 1MB
  $pr = Get-CimInstance Win32_Process
  $b = @($pr | Where-Object { $_.Name -match '^(cargo|rustc|maturin|link|lld-link|rust-lld)\.exe$' })
  $bws = (($b | Measure-Object WorkingSetSize -Sum).Sum) / 1GB; $bpv = (($b | Measure-Object PrivatePageCount -Sum).Sum) / 1GB
  $p = @($pr | Where-Object { $_.Name -match '^python\.exe$' -and $_.CommandLine -match 'd18_hybsign_prec\.py' })
  $pws = (($p | Measure-Object WorkingSetSize -Sum).Sum) / 1GB; $ppv = (($p | Measure-Object PrivatePageCount -Sum).Sum) / 1GB
  if ($bws -gt $peakBuildWs) { $peakBuildWs = $bws }; if ($bpv -gt $peakBuildPriv) { $peakBuildPriv = $bpv }
  if ($used -gt $peakCommit) { $peakCommit = $used }; if ($head -lt $minHead) { $minHead = $head }
  "{0} commit_used_GB={1:N1} limit_GB={2:N1} headroom_GB={3:N1} free_phys_GB={4:N1} build_n={5} build_ws_GB={6:N2} build_priv_GB={7:N2} prec_n={8} prec_ws_GB={9:N2} prec_priv_GB={10:N2} peak_build_ws_GB={11:N2} peak_build_priv_GB={12:N2} peak_commit_GB={13:N1} min_headroom_GB={14:N1}" -f $ts, $used, $lim, $head, $free, $b.Count, $bws, $bpv, $p.Count, $pws, $ppv, $peakBuildWs, $peakBuildPriv, $peakCommit, $minHead | Add-Content -Path $log
  if ($head -lt 8 -and $head -lt ($lastAlert - 2)) { "$ts ALERT commit headroom {0:N1} GB (used {1:N1} of {2:N1}); build {3:N1} GB private, precision {4:N1} GB. Alert only: nothing is killed." -f $head, $used, $lim, $bpv, $ppv | Add-Content -Path $alerts; $lastAlert = $head; $alerted = $true }
  if ($alerted -and $head -gt 12) { "$ts CLEAR commit headroom back to {0:N1} GB" -f $head | Add-Content -Path $alerts; $lastAlert = 1e9; $alerted = $false }
  Start-Sleep -Seconds 30
}
"$((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')) stopped; peak_build_ws_GB=$peakBuildWs peak_build_priv_GB=$peakBuildPriv peak_commit_GB=$peakCommit min_headroom_GB=$minHead" | Add-Content -Path $log
