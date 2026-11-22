# chain.ps1 PID [PID ...]: prints each pid's ParentProcessId chain (name, pid, start time, priority class) up to the first missing parent, and whether any ancestor is claude.exe.
param([int[]]$Pids)
foreach ($p0 in $Pids) {
  $p = $p0; $seen = @(); $line = @(); $claude = $false
  while ($p -and $p -ne 0 -and $seen -notcontains $p) {
    $seen += $p
    $c = Get-CimInstance Win32_Process -Filter "ProcessId=$p" -ErrorAction SilentlyContinue
    if (-not $c) { $line += "$p (gone)"; break }
    if ($c.Name -ieq 'claude.exe') { $claude = $true }
    $pr = try { (Get-Process -Id $p -ErrorAction Stop).PriorityClass } catch { '?' }
    $line += "$($c.Name)[$p,$pr]"
    $p = $c.ParentProcessId
  }
  "{0}: {1}  => descends from claude.exe: {2}" -f $p0, ($line -join ' <- '), $claude
}
