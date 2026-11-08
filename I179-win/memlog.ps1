# Alert-only sampler, kills nothing. Appends one CSV row every 15 s until mem_stop.flag exists.
$raw = 'C:\Users\nathan\Source\choptuik-large-d-raw\I179-win'
$csv = "$raw\mem_build.csv"
if (-not (Test-Path $csv)) { 'utc,free_gb,commit_used_gb,build_ws_gb,chain_d6_alive,chain_d10_alive' | Set-Content -Encoding ascii $csv }
while (-not (Test-Path "$raw\mem_stop.flag")) {
  $os = Get-CimInstance Win32_OperatingSystem
  $free = $os.FreePhysicalMemory / 1MB
  $commit = ($os.TotalVirtualMemorySize - $os.FreeVirtualMemory) / 1MB
  $ws = (Get-Process -Name rustc,cargo,cl,link,maturin,rust-lld -ErrorAction SilentlyContinue | Measure-Object WorkingSet64 -Sum).Sum / 1GB
  $a = [int]($null -ne (Get-Process -Id 2712 -ErrorAction SilentlyContinue))
  $b = [int]($null -ne (Get-Process -Id 9084 -ErrorAction SilentlyContinue))
  ('{0},{1:N2},{2:N2},{3:N2},{4},{5}' -f [DateTime]::UtcNow.ToString('s'), $free, $commit, $ws, $a, $b) | Add-Content -Encoding ascii $csv
  Start-Sleep -Seconds 15
}
