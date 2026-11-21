# #1058 winb: the build must run at BelowNormal. Git's `nice -n 2` in hp/build.sh can set another class on maturin and its children, so every 20 s each descendant of the
# driver (python.exe running driver_hp_1058b.py) that is not BelowNormal is set to BelowNormal. Changes only a priority class; ends when the driver's log says done.
$dir = "C:\Users\nathan\Source\hp1058_winb"
$out = Join-Path $dir "prio_hp_1058.log"
$blog = Join-Path $dir "hp1058b_build.log"
$end = [DateTime]::UtcNow.AddHours(16)
$seen = @{}
while ([DateTime]::UtcNow -lt $end) {
  try {
    $all = Get-CimInstance Win32_Process
    $root = $all | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match 'driver_hp_1058b' } | Select-Object -First 1
    if ($root) {
      $ids = @($root.ProcessId); $grow = $true
      while ($grow) {
        $grow = $false
        foreach ($p in $all) { if (($ids -notcontains $p.ProcessId) -and ($ids -contains $p.ParentProcessId)) { $ids += $p.ProcessId; $grow = $true } }
      }
      foreach ($id in $ids) {
        $p = Get-Process -Id $id -ErrorAction SilentlyContinue
        if ($p -and $p.PriorityClass -ne 'BelowNormal') {
          $old = $p.PriorityClass
          try { $p.PriorityClass = 'BelowNormal' } catch { continue }
          Add-Content $out ("{0} pid {1} {2}: {3} -> BelowNormal" -f [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss'), $id, $p.ProcessName, $old)
        }
      }
    }
  } catch { Add-Content $out ("{0} error: {1}" -f [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss'), $_.Exception.Message) }
  if ((Test-Path $blog) -and (Select-String -Path $blog -Pattern 'hp1058b driver done' -Quiet)) { Add-Content $out ("{0} driver done, stopping" -f [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss')); break }
  Start-Sleep -Seconds 20
}
