# #1025 winb: the driver's `nice -n 10` makes Windows run the row's python at Idle priority; the coordinator asked for BelowNormal, so lift it for the P4 rows until the driver's log says done
$log = "C:\Users\nathan\Source\p4_1025\I1025-win\p4\p4_w.log"
$out = "C:\Users\nathan\Source\p4_1025\prio_p4_1025.log"
while ($true) {
  Get-CimInstance Win32_Process | Where-Object { $_.Name -match 'python' -and $_.CommandLine -match 'p4_hybrid' } | ForEach-Object {
    $p = Get-Process -Id $_.ProcessId -ErrorAction SilentlyContinue
    if ($p -and $p.PriorityClass -ne 'BelowNormal') {
      $old = $p.PriorityClass; $p.PriorityClass = 'BelowNormal'
      Add-Content $out ("{0} pid {1}: {2} -> BelowNormal" -f [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss'), $p.Id, $old)
    }
  }
  if ((Test-Path $log) -and (Select-String -Path $log -Pattern 'p4_driver_w.sh done' -Quiet)) { Add-Content $out ("{0} driver done, stopping" -f [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss')); break }
  Start-Sleep -Seconds 20
}
