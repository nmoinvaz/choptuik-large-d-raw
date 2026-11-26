# session_check_1025.ps1 LABEL ROOTPID [ROOTPID ...]: the Windows counterpart of macm3's session_check_1025.py (raw I1025-macm3/kc79_d1925): from one Win32_Process snapshot, the parent chain of each given pid and of
# every descendant of the given pids (a child older than its parent is a reused parent pid and is left out), up to the first parent that is not running (pid ppid session start-UTC name and command), written to session_check_LABEL.txt next to this script's OUT folder.
# Exit 1 if 'claude' is in any chain (the run would be tied to the claude.exe session); the Windows Terminal / OpenConsole handoff win2 found is reported beside it (WindowsTerminal, OpenConsole,
# wt.exe in a chain, and a conhost started with --headless). The checker's own chain is listed for comparison.
param([string]$Label, [int[]]$Pids)
$out = 'C:\Users\nathan\Source\kc95d22875s_1025\I1025-win\kc95_d22875_secant'
$T = @{}
Get-CimInstance Win32_Process | ForEach-Object { $T[[int]$_.ProcessId] = $_ }
# Windows reuses pids: a process whose recorded parent pid now names a process that started AFTER it was not started by it. A child counts only if it is not older than its parent.
function Kids($p) { $k = @($T.Values | Where-Object { [int]$_.ParentProcessId -eq $p -and [int]$_.ProcessId -ne $p -and $_.CreationDate -ge $T[$p].CreationDate } | ForEach-Object { [int]$_.ProcessId }); $k + @($k | ForEach-Object { Kids $_ }) }
function Chain($p) { $c = @(); $seen = @{}; while ($T.ContainsKey($p) -and -not $seen[$p]) { $seen[$p] = $true; $c += $T[$p]; $q = [int]$T[$p].ParentProcessId; if ($T.ContainsKey($q) -and $T[$q].CreationDate -gt $T[$p].CreationDate) { break }; $p = $q }; $c }
$todo = @(); foreach ($p in $Pids) { foreach ($q in @($p) + @(Kids $p)) { if ($todo -notcontains $q) { $todo += $q } } }
$L = @("# session check, $((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')) UTC: parent chain of each pid (the given ones and their descendants) up to the first parent that is not running (pid ppid session start-UTC command); fails if 'claude' is in a chain")
$claude = $false; $wt = $false; $headless = $false
foreach ($p in $todo) {
  if (-not $T.ContainsKey($p)) { $L += ""; $L += "pid ${p}: not running"; continue }
  $ch = Chain $p
  $L += ""; $L += "pid ${p} ($($T[$p].Name)):"
  foreach ($r in $ch) {
    $cmd = if ($r.CommandLine) { $r.CommandLine.Substring(0, [Math]::Min(110, $r.CommandLine.Length)) } else { '' }
    $L += ("  {0,6} ppid {1,6} sess {2} {3:HH:mm:ss}  {4}  {5}" -f $r.ProcessId, $r.ParentProcessId, $r.SessionId, $r.CreationDate.ToUniversalTime(), $r.Name, $cmd)
    if ($r.Name -match 'claude') { $claude = $true }
    if ($r.Name -match 'WindowsTerminal|OpenConsole|^wt\.exe') { $wt = $true }
    if ($r.Name -eq 'conhost.exe' -and $r.CommandLine -match '--headless') { $headless = $true }
  }
  $top = $ch[-1]; $L += "  chain ends at pid $($top.ProcessId) ($($top.Name)), parent $($top.ParentProcessId) not running or not listed, $($ch.Count) processes"
}
$me = Chain $PID; $L += ""; $L += "for comparison, this checker's own chain: " + (($me | Select-Object -First 7 | ForEach-Object { "$($_.ProcessId):$($_.Name)" }) -join ' <- ') + ' ...'
$L += "claude in any chain of the run: $claude; Windows Terminal / OpenConsole / wt in any chain: $wt; a headless conhost in a chain: $headless"
$L | Set-Content -Path "$out\session_check_$Label.txt" -Encoding UTF8
$L
if ($claude) { exit 1 } else { exit 0 }
