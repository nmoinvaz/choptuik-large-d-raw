# glue (read only): free physical memory in GiB, then for each given root pid the summed working set in GiB of its process tree and its process count: "free ws1 n1 ws2 n2"
param([int]$Root1, [int]$Root2)
$all = Get-CimInstance Win32_Process
function Tree($root) {
  $ids = New-Object System.Collections.Generic.HashSet[int]
  if ($all | Where-Object { [int]$_.ProcessId -eq $root }) { [void]$ids.Add($root) }
  do { $n = $ids.Count; foreach ($p in $all) { if ($ids.Contains([int]$p.ParentProcessId)) { [void]$ids.Add([int]$p.ProcessId) } } } while ($ids.Count -gt $n)
  $ws = 0; $c = 0
  foreach ($p in $all) { if ($ids.Contains([int]$p.ProcessId)) { $ws += [int64]$p.WorkingSetSize; $c++ } }
  '{0:N2} {1}' -f ($ws / 1GB), $c
}
$free = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB
'{0:N1} {1} {2}' -f $free, (Tree $Root1), (Tree $Root2)
